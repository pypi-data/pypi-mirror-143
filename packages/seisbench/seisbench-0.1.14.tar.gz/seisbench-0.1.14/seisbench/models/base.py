import seisbench
import seisbench.util as util

from abc import abstractmethod, ABC
from pathlib import Path
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from collections import defaultdict
from queue import PriorityQueue
import json
import math
import numpy as np
import obspy
import warnings
from obspy.signal.trigger import trigger_onset
import asyncio
import nest_asyncio
from packaging import version


class SeisBenchModel(nn.Module):
    """
    Base SeisBench model interface for processing waveforms.

    :param citation: Citation reference, defaults to None.
    :type citation: str, optional
    """

    def __init__(self, citation=None):
        super().__init__()
        self._citation = citation
        self._weights_docstring = None
        self._weights_metadata = None

    def __str__(self):
        return f"SeisBench model\t\t{self.name}\n\n{super().__str__()}"

    @property
    def name(self):
        return self._name_internal()

    @classmethod
    def _name_internal(cls):
        return cls.__name__

    @property
    def citation(self):
        return self._citation

    @property
    def weights_docstring(self):
        return self._weights_docstring

    @classmethod
    def _model_path(cls):
        return Path(seisbench.cache_root, "models", cls._name_internal().lower())

    @classmethod
    def _remote_path(cls):
        return "/".join((seisbench.remote_root, "models", cls._name_internal().lower()))

    @classmethod
    def _pretrained_path(cls, name):
        weight_path = cls._model_path() / f"{name}.pt"
        metadata_path = cls._model_path() / f"{name}.json"

        return weight_path, metadata_path

    @classmethod
    def from_pretrained(cls, name, force=False, wait_for_file=False):
        """
        Load pretrained model with weights.

        A pretrained model weights consists of two files. A weights file [name].pt and a [name].json config file.
        The config file is not mandatory, but strongly recommended. The config file can (and should) contain the
        following entries, even though all arguments are optional:

        - "docstring": A string documenting the pipeline. Usually also contains information on the author.
        - "model_args": Argument dictionary passed to the init function of the pipeline.
        - "seisbench_requirement": The minimal version of SeisBench required to use the weights file.
        - "default_args": Default args for the :py:func:`annotate`/:py:func:`classify` functions.
          These arguments will supersede any potential constructor settings.

        :param name: Model name prefix.
        :type name: str
        :param force: Force execution of download callback, defaults to False
        :type force: bool, optional
        :param wait_for_file: Whether to wait on partially downloaded files, defaults to False
        :type wait_for_file: bool, optional
        :return: Model instance
        :rtype: SeisBenchModel
        """
        weight_path, metadata_path = cls._pretrained_path(name)

        def download_weights_callback(weight_path):
            seisbench.logger.info(f"Weight file {name} not in cache. Downloading...")
            weight_path.parent.mkdir(exist_ok=True, parents=True)

            remote_weight_path = f"{cls._remote_path()}/{name}.pt"
            util.download_http(remote_weight_path, weight_path)

        def download_metadata_callback(metadata_path):
            remote_metadata_path = f"{cls._remote_path()}/{name}.json"
            try:
                util.download_http(
                    remote_metadata_path, metadata_path, progress_bar=False
                )
            except ValueError:
                # A missing metadata file does not lead to a crash
                pass

        seisbench.util.callback_if_uncached(
            weight_path,
            download_weights_callback,
            force=force,
            wait_for_file=wait_for_file,
        )
        seisbench.util.callback_if_uncached(
            metadata_path,
            download_metadata_callback,
            force=force,
            wait_for_file=wait_for_file,
        )

        if metadata_path.is_file():
            with open(metadata_path, "r") as f:
                weights_metadata = json.load(f)
        else:
            weights_metadata = {}

        model_args = weights_metadata.get("model_args", {})
        model = cls(**model_args)

        model._weights_metadata = weights_metadata
        model._parse_metadata()

        model.load_state_dict(torch.load(weight_path))

        return model

    @classmethod
    def list_pretrained(cls, details=False):
        """
        Returns list of available pretrained weights and optionally their docstrings.

        :param details: If true, instead of a returning only a list, also return their docstrings.
                        Note that this requires to download the json files for each model in the background
                        and is therefore slower. Defaults to false.
        :type details: bool
        :return: List of available weights or dict of weights and their docstrings
        :rtype: list or dict
        """
        remote_path = cls._remote_path()

        weights = [
            x[:-3] for x in seisbench.util.ls_webdav(remote_path) if x.endswith(".pt")
        ]

        if details:
            detail_weights = {}

            for weight in weights:

                def download_metadata_callback(metadata_path):
                    remote_metadata_path = os.path.join(
                        cls._remote_path(), f"{weight}.json"
                    )
                    try:
                        util.download_http(
                            remote_metadata_path, metadata_path, progress_bar=False
                        )
                    except ValueError:
                        # A missing metadata file does not lead to a crash
                        pass

                _, metadata_path = cls._pretrained_path(weight)

                seisbench.util.callback_if_uncached(
                    metadata_path, download_metadata_callback
                )

                if metadata_path.is_file():
                    with open(metadata_path, "r") as f:
                        config = json.load(f)
                    detail_weights[weight] = config.get("docstring", None)
                else:
                    detail_weights[weight] = None

            weights = detail_weights

        return weights

    def _parse_metadata(self):
        # Load docstring
        self._weights_docstring = self._weights_metadata.get("docstring", "")

        # Check version requirement
        seisbench_requirement = self._weights_metadata.get(
            "seisbench_requirement", None
        )
        if seisbench_requirement is not None:
            if version.parse(seisbench_requirement) > version.parse(
                seisbench.__version__
            ):
                raise ValueError(
                    f"Weights require seisbench version at least {seisbench_requirement}, "
                    f"but the installed version is {seisbench.__version__}."
                )

        # Parse default args - Config default_args supersede constructor args
        default_args = self._weights_metadata.get("default_args", {})
        self.default_args.update(default_args)


class WaveformModel(SeisBenchModel, ABC):
    """
    Abstract interface for models processing waveforms.
    Based on the properties specified by inheriting models, WaveformModel automatically provides the respective
    :py:func:`annotate`/:py:func:`classify` functions.
    Both functions take obspy streams as input.
    The :py:func:`annotate` function has a rather strictly defined output, i.e.,
    it always outputs obspy streams with the annotations.
    These can for example be functions of pick probability over time.
    In contrast, the :py:func:`classify` function can tailor it's output to the model type.
    For example, a picking model might output picks, while a magnitude estimation model might only output
    a scalar magnitude.
    Internally, :py:func:`classify` will usually rely on :py:func:`annotate` and simply add steps to it's output.

    For details see the documentation of these functions.

    :param component_order: Specify component order (e.g. ['ZNE']), defaults to None.
    :type component_order: list, optional
    :param sampling_rate: Sampling rate of the model, defaults to None.
                          If sampling rate is not None, the annotate and classify functions will automatically resample
                          incoming traces and validate correct sampling rate if the model overwrites
                          :py:func:`annotate_stream_pre`.
    :type sampling_rate: float
    :param output_type: The type of output from the model. Current options are:

                        - "point" for a point prediction, i.e., the probability of containing a pick in the window
                          or of a pick at a certain location. This will provide an :py:func:`annotate` function.
                          If an :py:func:`classify_aggregate` function is provided by the inheriting model,
                          this will also provide a :py:func:`classify` function.
                        - "array" for prediction curves, i.e., probabilities over time for the arrival of certain wave
                          types. This will provide an :py:func:`annotate` function.
                          If an :py:func:`classify_aggregate` function is provided by the inheriting model,
                          this will also provide a :py:func:`classify` function.
                        - "regression" for a regression value, i.e., the sample of the arrival within a window.
                          This will only provide a :py:func:`classify` function.

    :type output_type: str
    :param default_args: Default arguments to use in annotate and classify functions
    :type default_args: dict[str, any]
    :param in_samples: Number of input samples in time
    :type in_samples: int
    :param pred_sample: For a "point" prediction: sample number of the sample in a window for which the prediction is
                        valid. For an "array" prediction: a tuple of first and last sample defining the prediction
                        range. Note that the number of output samples and input samples within the given range are
                        not required to agree.
    :type pred_sample: int, tuple
    :param labels: Labels for the different predictions in the output, e.g., Noise, P, S. If a function is passed,
                   it will be called for every label generation and be provided with the stats of the trace that was
                   annotated.
    :type labels: list or string or callable
    :param filter_args: Arguments to be passed to :py:func:`obspy.filter` in :py:func:`annotate_stream_pre`
    :type filter_args: tuple
    :param filter_kwargs: Keyword arguments to be passed to :py:func:`obspy.filter` in :py:func:`annotate_stream_pre`
    :type filter_kwargs: dict
    :param grouping: Level of grouping for annotating streams. Supports "instrument" and "channel".
    :type grouping: str
    :param kwargs: Kwargs are passed to the superclass
    """

    def __init__(
        self,
        component_order=None,
        sampling_rate=None,
        output_type=None,
        default_args=None,
        in_samples=None,
        pred_sample=0,
        labels=None,
        filter_args=None,
        filter_kwargs=None,
        grouping="instrument",
        **kwargs,
    ):
        super().__init__(**kwargs)

        if component_order is None:
            self._component_order = seisbench.config["component_order"]
        else:
            self._component_order = component_order

        self.sampling_rate = sampling_rate
        self.output_type = output_type
        if default_args is None:
            self.default_args = {}
        else:
            self.default_args = default_args
        self.in_samples = in_samples
        self.pred_sample = pred_sample
        self.filter_args = filter_args
        self.filter_kwargs = filter_kwargs
        self._grouping = grouping

        if grouping == "channel":
            if component_order is not None:
                seisbench.logger.warning(
                    "Grouping is 'channel' but component_order is given. "
                    "component_order will be ignored, as every channel is treated separately."
                )
            self._component_order = None

        # Validate pred sample
        if output_type == "point" and not isinstance(pred_sample, (int, float)):
            raise TypeError(
                "For output type 'point', pred_sample needs to be a scalar."
            )
        if output_type == "array":
            if not isinstance(pred_sample, (list, tuple)) or not len(pred_sample) == 2:
                raise TypeError(
                    "For output type 'array', pred_sample needs to be a tuple of length 2."
                )
            if pred_sample[0] < 0 or pred_sample[1] < 0:
                raise ValueError(
                    "For output type 'array', both entries of pred_sample need to be non-negative."
                )

        self.labels = labels

        self._annotate_function_mapping = {
            "point": (self._cut_fragments_point, self._reassemble_blocks_point),
            "array": (self._cut_fragments_array, self._reassemble_blocks_array),
        }

        self._annotate_functions = self._annotate_function_mapping.get(
            output_type, None
        )

    def __str__(self):
        return f"Component order:\t{self.component_order}\n{super().__str__()}"

    @property
    def device(self):
        return next(self.parameters()).device

    @property
    def component_order(self):
        return self._component_order

    def annotate(
        self, stream, strict=True, flexible_horizontal_components=True, **kwargs
    ):
        """
        Annotates an obspy stream using the model based on the configuration of the WaveformModel superclass.
        For example, for a picking model, annotate will give a characteristic function/probability function for picks
        over time.
        The annotate function contains multiple subfunction, which can be overwritten individually by inheriting
        models to accommodate their requirements. These functions are:

        - :py:func:`annotate_stream_pre`
        - :py:func:`annotate_stream_validate`
        - :py:func:`annotate_window_pre`
        - :py:func:`annotate_window_post`

        Please see the respective documentation for details on their functionality, inputs and outputs.

        :param stream: Obspy stream to annotate
        :type stream: obspy.core.Stream
        :param strict: If true, only annotate if recordings for all components are available,
                       otherwise impute missing data with zeros.
        :type strict: bool
        :param flexible_horizontal_components: If true, accepts traces with Z12 components as ZNE and vice versa.
                                               This is usually acceptable for rotationally invariant models,
                                               e.g., most picking models.
        :type flexible_horizontal_components: bool
        :param kwargs:
        :return: Obspy stream of annotations
        """
        nest_asyncio.apply()
        call = self._annotate_async(
            stream, strict, flexible_horizontal_components, **kwargs
        )
        return asyncio.run(call)

    async def _annotate_async(
        self, stream, strict=True, flexible_horizontal_components=True, **kwargs
    ):
        """
        Wrapper for the annotate function that can be called using asyncio.run.
        Parameters as for :py:func:`annotate`.

        :param stream:
        :param strict:
        :param flexible_horizontal_components:
        :param kwargs:
        :return:
        """
        if self._annotate_functions is None:
            raise NotImplementedError(
                "This model has no annotate function implemented."
            )

        cut_fragments, reassemble_blocks = self._annotate_functions

        # Kwargs overwrite default args
        argdict = self.default_args.copy()
        argdict.update(kwargs)

        stream = stream.copy()
        stream.merge(-1)

        output = obspy.Stream()
        if len(stream) == 0:
            return output

        # Preprocess stream, e.g., filter/resample
        self.annotate_stream_pre(stream, argdict)

        # Validate stream
        self.annotate_stream_validate(stream, argdict)

        # Group stream
        groups = self.group_stream(stream)

        # Sampling rate of the data. Equal to self.sampling_rate is this is not None
        argdict["sampling_rate"] = groups[0][0].stats.sampling_rate

        # Queues for multiprocessing
        batch_size = argdict.get("batch_size", 64)
        queue_groups = asyncio.Queue()  # Waveform groups
        queue_raw_blocks = (
            asyncio.Queue()
        )  # Waveforms as blocks of arrays and their metadata
        queue_raw_fragments = asyncio.Queue(
            4 * batch_size
        )  # Raw waveform fragments with the correct input size
        queue_preprocessed_fragments = asyncio.Queue(
            4 * batch_size
        )  # Preprocessed input fragments
        queue_raw_pred = asyncio.Queue()  # Queue for raw (but unbatched) predictions
        queue_postprocessed_pred = (
            asyncio.Queue()
        )  # Queue for raw (but unbatched) predictions
        queue_pred_blocks = asyncio.Queue()  # Queue for blocks of predictions
        queue_results = asyncio.Queue()  # Results streams

        # TODO: Enable multiprocessing by starting multiple workers for some tasks
        #       Also requires to send multiple None values to the queues for stopping
        process_streams_to_arrays = asyncio.create_task(
            self._process_streams_to_arrays(
                queue_groups, queue_raw_blocks, strict, flexible_horizontal_components
            )
        )
        process_cut_fragments = asyncio.create_task(
            cut_fragments(queue_raw_blocks, queue_raw_fragments, argdict)
        )
        process_annotate_window_pre = asyncio.create_task(
            self._process_annotate_window_pre(
                queue_raw_fragments, queue_preprocessed_fragments, argdict
            )
        )
        process_predict = asyncio.create_task(
            self._process_predict(queue_preprocessed_fragments, queue_raw_pred, argdict)
        )
        process_annotate_window_post = asyncio.create_task(
            self._process_annotate_window_post(
                queue_raw_pred, queue_postprocessed_pred, argdict
            )
        )
        process_reassemble_blocks = asyncio.create_task(
            reassemble_blocks(queue_postprocessed_pred, queue_pred_blocks, argdict)
        )
        process_predictions_to_streams = asyncio.create_task(
            self._process_predictions_to_streams(queue_pred_blocks, queue_results)
        )

        for group in groups:
            await queue_groups.put(group)
        await queue_groups.put(None)

        await process_streams_to_arrays
        await queue_raw_blocks.put(None)
        await process_cut_fragments
        await queue_raw_fragments.put(None)
        await process_annotate_window_pre
        await queue_preprocessed_fragments.put(None)
        await process_predict
        await queue_raw_pred.put(None)
        await process_annotate_window_post
        await queue_postprocessed_pred.put(None)
        await process_reassemble_blocks
        await queue_pred_blocks.put(None)
        await process_predictions_to_streams

        while True:
            try:
                output += queue_results.get_nowait()
            except asyncio.QueueEmpty:
                break

        return output

    async def _process_streams_to_arrays(
        self, queue_in, queue_out, strict, flexible_horizontal_components
    ):
        """
        Wrapper around :py:func:`stream_to_arrays`, adding the functionality to read from and write to queues.

        :param queue_in: Input queue
        :param queue_out: Output queue
        :param strict: See :py:func:`stream_to_arrays`
        :param flexible_horizontal_components: See :py:func:`stream_to_arrays`
        :return: None
        """
        group = await queue_in.get()
        while group is not None:
            times, data = self.stream_to_arrays(
                group,
                strict=strict,
                flexible_horizontal_components=flexible_horizontal_components,
            )
            for t0, block in zip(times, data):
                await queue_out.put((t0, block, group[0].stats))
            group = await queue_in.get()

    async def _cut_fragments_point(self, queue_in, queue_out, argdict):
        """
        Cuts numpy arrays into fragments for point prediction models.

        :param queue_in: Input queue
        :param queue_out: Output queue
        :param argdict: Dictionary of arguments
        :return: None
        """
        stride = argdict.get("stride", 1)

        elem = await queue_in.get()
        while elem is not None:
            t0, block, trace_stats = elem

            starts = np.arange(0, block.shape[1] - self.in_samples + 1, stride)
            if len(starts) == 0:
                seisbench.logger.warning(
                    "Parts of the input stream consist of fragments shorter than the number "
                    "of input samples. Output might be empty."
                )
                elem = await queue_in.get()
                continue

            # Generate windows and preprocess
            for s in starts:
                window = block[:, s : s + self.in_samples]
                # The combination of trace_stats and t0 is a unique identifier
                # s can be used to reassemble the block, len(starts) allows to identify if the block is complete yet
                metadata = (t0, s, len(starts), trace_stats)
                await queue_out.put((window, metadata))

            elem = await queue_in.get()

    async def _reassemble_blocks_point(self, queue_in, queue_out, argdict):
        """
        Reassembles point predictions into numpy arrays.

        :param queue_in: Input queue
        :param queue_out: Output queue
        :param argdict: Dictionary of arguments
        :return: None
        """
        stride = argdict.get("stride", 1)
        buffer = defaultdict(list)  # Buffers predictions until a block is complete

        elem = await queue_in.get()
        while elem is not None:
            window, metadata = elem
            t0, s, len_starts, trace_stats = metadata
            key = f"{t0}_{trace_stats.network}.{trace_stats.station}.{trace_stats.station}.{trace_stats.channel[:-1]}"

            buffer[key].append(elem)
            if len(buffer[key]) == len_starts:
                preds = [(s, window) for window, (_, s, _, _) in buffer[key]]
                preds = sorted(preds)  # Sort by start
                preds = [window for s, window in preds]
                preds = np.stack(preds, axis=0)
                if preds.ndim == 1:
                    preds = preds.reshape(-1, 1)
                pred_time = t0 + self.pred_sample / argdict["sampling_rate"]
                pred_rate = argdict["sampling_rate"] / stride

                await queue_out.put(((pred_rate, pred_time, preds), trace_stats))

                del buffer[key]

            elem = await queue_in.get()

    async def _cut_fragments_array(self, queue_in, queue_out, argdict):
        """
        Cuts numpy arrays into fragments for array prediction models.

        :param queue_in: Input queue
        :param queue_out: Output queue
        :param argdict: Dictionary of arguments
        :return: None
        """
        overlap = argdict.get("overlap", 0)

        elem = await queue_in.get()
        while elem is not None:
            t0, block, trace_stats = elem

            if self._grouping == "channel":
                # Add fake channel dimension
                block = block.reshape((-1,) + block.shape)

            starts = np.arange(
                0, block.shape[1] - self.in_samples + 1, self.in_samples - overlap
            )
            if len(starts) == 0:
                seisbench.logger.warning(
                    "Parts of the input stream consist of fragments shorter than the number "
                    "of input samples. Output might be empty."
                )
                elem = await queue_in.get()
                continue

            # Add one more trace to the end
            if starts[-1] + self.in_samples < block.shape[1]:
                starts = np.concatenate([starts, [block.shape[1] - self.in_samples]])

            # Generate windows and preprocess
            for s in starts:
                window = block[:, s : s + self.in_samples]
                if self._grouping == "channel":
                    # Remove fake channel dimension
                    window = window[0]
                # The combination of trace_stats and t0 is a unique identifier
                # s can be used to reassemble the block, len(starts) allows to identify if the block is complete yet
                metadata = (t0, s, len(starts), trace_stats)
                await queue_out.put((window, metadata))

            elem = await queue_in.get()

    async def _reassemble_blocks_array(self, queue_in, queue_out, argdict):
        """
        Reassembles array predictions into numpy arrays.

        :param queue_in: Input queue
        :param queue_out: Output queue
        :param argdict: Dictionary of arguments
        :return: None
        """
        overlap = argdict.get("overlap", 0)
        buffer = defaultdict(list)  # Buffers predictions until a block is complete

        elem = await queue_in.get()
        while elem is not None:
            window, metadata = elem
            t0, s, len_starts, trace_stats = metadata
            key = f"{t0}_{trace_stats.network}.{trace_stats.station}.{trace_stats.station}.{trace_stats.channel[:-1]}"

            buffer[key].append(elem)
            if len(buffer[key]) == len_starts:
                preds = [(s, window) for window, (_, s, _, _) in buffer[key]]
                preds = sorted(preds)  # Sort by start
                starts = [s for s, window in preds]
                preds = [window for s, window in preds]
                preds = np.stack(preds, axis=0)

                # Number of prediction samples per input sample
                prediction_sample_factor = preds[0].shape[0] / (
                    self.pred_sample[1] - self.pred_sample[0]
                )

                # Maximum number of predictions covering a point
                coverage = int(
                    np.ceil(self.in_samples / (self.in_samples - overlap) + 1)
                )

                pred_length = int(
                    np.ceil(
                        (np.max(starts) + self.in_samples) * prediction_sample_factor
                    )
                )
                pred_merge = (
                    np.zeros_like(
                        preds[0], shape=(pred_length, preds[0].shape[1], coverage)
                    )
                    * np.nan
                )
                for i, (pred, start) in enumerate(zip(preds, starts)):
                    pred_start = int(start * prediction_sample_factor)
                    pred_merge[
                        pred_start : pred_start + pred.shape[0], :, i % coverage
                    ] = pred

                with warnings.catch_warnings():
                    warnings.filterwarnings(
                        action="ignore", message="Mean of empty slice"
                    )
                    preds = np.nanmean(pred_merge, axis=-1)

                pred_time = t0 + self.pred_sample[0] / argdict["sampling_rate"]
                pred_rate = argdict["sampling_rate"] * prediction_sample_factor

                await queue_out.put(((pred_rate, pred_time, preds), trace_stats))

                del buffer[key]

            elem = await queue_in.get()

    async def _process_annotate_window_pre(self, queue_in, queue_out, argdict):
        """
        Wrapper with queue IO functionality around :py:func:`annotate_window_pre`

        :param queue_in: Input queue
        :param queue_out: Output queue
        :param argdict: Dictionary of arguments
        :return: None
        """
        elem = await queue_in.get()
        while elem is not None:
            window, metadata = elem
            preprocessed = self.annotate_window_pre(window, argdict)
            if isinstance(preprocessed, tuple):  # Contains piggyback information
                assert len(preprocessed) == 2
                await queue_out.put(preprocessed + (metadata,))
            else:  # No piggyback information, add none as piggyback
                await queue_out.put((preprocessed, None, metadata))
            elem = await queue_in.get()

    async def _process_predict(self, queue_in, queue_out, argdict):
        """
        Prediction function, gathering predictions until a batch is full and handing them to :py:func:`_predict_buffer`.

        :param queue_in: Input queue
        :param queue_out: Output queue
        :param argdict: Dictionary of arguments
        :return: None
        """
        buffer = []
        batch_size = argdict.get("batch_size", 64)

        elem = await queue_in.get()
        while True:
            if elem is not None:
                buffer.append(elem)

            if len(buffer) == batch_size or (elem is None and len(buffer) > 0):
                pred = self._predict_buffer([window for window, _, _ in buffer])
                for pred_window, (_, piggyback, metadata) in zip(pred, buffer):
                    await queue_out.put((pred_window, piggyback, metadata))
                buffer = []

            if elem is None:
                break

            elem = await queue_in.get()

    def _predict_buffer(self, buffer):
        """
        Batches model inputs, runs prediction, and unbatches output

        :param buffer: List of inputs to the model
        :return: Unpacked predictions
        """
        fragments = np.stack(buffer)
        fragments = np.stack(fragments, axis=0)
        fragments = torch.tensor(fragments, device=self.device, dtype=torch.float32)

        train_mode = self.training
        try:
            self.eval()
            with torch.no_grad():
                preds = self(fragments)
        finally:
            if train_mode:
                self.train()
        preds = self._recursive_torch_to_numpy(preds)
        # Unbatch window predictions
        reshaped_preds = [pred for pred in self._recursive_slice_pred(preds)]
        return reshaped_preds

    async def _process_annotate_window_post(self, queue_in, queue_out, argdict):
        """
        Wrapper with queue IO functionality around :py:func:`annotate_window_post`

        :param queue_in: Input queue
        :param queue_out: Output queue
        :param argdict: Dictionary of arguments
        :return: None
        """
        elem = await queue_in.get()
        while elem is not None:
            window, piggyback, metadata = elem
            await queue_out.put(
                (
                    self.annotate_window_post(window, piggyback, argdict=argdict),
                    metadata,
                )
            )
            elem = await queue_in.get()

    async def _process_predictions_to_streams(self, queue_in, queue_out):
        """
        Wrapper with queue IO functionality around :py:func:`_predictions_to_stream`

        :param queue_in: Input queue
        :param queue_out: Output queue
        :return: None
        """
        elem = await queue_in.get()
        while elem is not None:
            (pred_rate, pred_time, preds), trace_stats = elem
            await queue_out.put(
                self._predictions_to_stream(pred_rate, pred_time, preds, trace_stats)
            )
            elem = await queue_in.get()

    def _predictions_to_stream(self, pred_rate, pred_time, pred, trace_stats):
        """
        Converts a set of predictions to obspy streams

        :param pred_rates: Sampling rates of the prediction arrays
        :param pred_times: Start time of each prediction array
        :param preds: The prediction arrays, each with shape (samples, channels)
        :param trace_stats: A source trace.stats object to extract trace naming from
        :return: Obspy stream of predictions
        """
        output = obspy.Stream()

        # Define and store default labels
        if self.labels is None:
            self.labels = list(range(pred.shape[1]))

        for i in range(pred.shape[1]):
            if callable(self.labels):
                label = self.labels(trace_stats)
            else:
                label = self.labels[i]

            trimmed_pred, f, _ = self._trim_nan(pred[:, i])
            trimmed_start = pred_time + f / pred_rate
            output.append(
                obspy.Trace(
                    trimmed_pred,
                    {
                        "starttime": trimmed_start,
                        "sampling_rate": pred_rate,
                        "network": trace_stats.network,
                        "station": trace_stats.station,
                        "location": trace_stats.location,
                        "channel": f"{self.__class__.__name__}_{label}",
                    },
                )
            )

        return output

    def annotate_stream_pre(self, stream, argdict):
        """
        Runs preprocessing on stream level for the annotate function, e.g., filtering or resampling.
        By default, this function will resample all traces if a sampling rate for the model is provided.
        Furthermore, if a filter is specified in the class, the filter will be executed.
        As annotate create a copy of the input stream, this function can safely modify the stream inplace.
        Inheriting classes should overwrite this function if necessary.
        To keep the default functionality, a call to the overwritten method can be included.

        :param stream: Input stream
        :type stream: obspy.Stream
        :param argdict: Dictionary of arguments
        :return: Preprocessed stream
        """
        if self.filter_args is not None or self.filter_kwargs is not None:
            if self.filter_args is None:
                filter_args = ()
            else:
                filter_args = self.filter_args

            if self.filter_kwargs is None:
                filter_kwargs = {}
            else:
                filter_kwargs = self.filter_kwargs

            stream.filter(*filter_args, **filter_kwargs)

        if self.sampling_rate is not None:
            self.resample(stream, self.sampling_rate)
        return stream

    def annotate_stream_validate(self, stream, argdict):
        """
        Validates stream for the annotate function.
        This function should raise an exception if the stream is invalid.
        By default, this function will check if the sampling rate fits the provided one, unless it is None,
        and check for mismatching traces, i.e., traces covering the same time range on the same instrument with
        different values.
        Inheriting classes should overwrite this function if necessary.
        To keep the default functionality, a call to the overwritten method can be included.

        :param stream: Input stream
        :type stream: obspy.Stream
        :param argdict: Dictionary of arguments
        :return: None
        """
        if self.sampling_rate is not None:
            if any(trace.stats.sampling_rate != self.sampling_rate for trace in stream):
                raise ValueError(
                    f"Detected traces with mismatching sampling rate. "
                    f"Expected {self.sampling_rate} Hz for all traces."
                )

        if self.has_mismatching_records(stream):
            raise ValueError(
                "Detected multiple records for the same time and component that did not agree."
            )

    def annotate_window_pre(self, window, argdict):
        """
        Runs preprocessing on window level for the annotate function, e.g., normalization.
        By default returns the input window.
        Can alternatively return a tuple of the input window and piggyback information that is returned at
        :py:func:`annotate_window_post`.
        This can for example be used to transfer normalization information.
        Inheriting classes should overwrite this function if necessary.

        :param window: Input window
        :type window: numpy.array
        :param argdict: Dictionary of arguments
        :return: Preprocessed window and optionally piggyback information that is passed to annotate window post
        """
        return window

    def annotate_window_post(self, pred, piggyback=None, argdict=None):
        """
        Runs postprocessing on the predictions of a window for the annotate function, e.g., reformatting them.
        By default returns the original prediction.
        Inheriting classes should overwrite this function if necessary.

        :param pred: Predictions for one window. The data type depends on the model.
        :param argdict: Dictionary of arguments
        :param piggyback: Piggyback information, by default None.
        :return: Postprocessed predictions
        """
        return pred

    @staticmethod
    def _trim_nan(x):
        """
        Removes all starting and trailing nan values from a 1D array and returns the new array and the number of NaNs
        removed per side.
        """
        mask_forward = np.cumprod(np.isnan(x)).astype(
            bool
        )  # cumprod will be one until the first non-Nan value
        x = x[~mask_forward]
        mask_backward = np.cumprod(np.isnan(x)[::-1])[::-1].astype(
            bool
        )  # Double reverse for a backwards cumprod
        x = x[~mask_backward]

        return x, np.sum(mask_forward.astype(int)), np.sum(mask_backward.astype(int))

    def _recursive_torch_to_numpy(self, x):
        """
        Recursively converts torch.Tensor objects to numpy arrays while preserving any overarching tuple
        or list structure.
        :param x:
        :return:
        """
        if isinstance(x, torch.Tensor):
            return x.cpu().numpy()
        elif isinstance(x, list):
            return [self._recursive_torch_to_numpy(y) for y in x]
        elif isinstance(x, tuple):
            return tuple([self._recursive_torch_to_numpy(y) for y in x])
        elif isinstance(x, np.ndarray):
            return x
        else:
            raise ValueError(f"Can't unpack object of type {type(x)}.")

    def _recursive_slice_pred(self, x):
        """
        Converts batched predictions into a list of single predictions, assuming batch axis is first in all cases.
        Preserves overarching tuple and list structures
        :param x:
        :return:
        """
        if isinstance(x, np.ndarray):
            return list(y for y in x)
        elif isinstance(x, list):
            return [
                list(entry)
                for entry in zip(*[self._recursive_slice_pred(y) for y in x])
            ]
        elif isinstance(x, tuple):
            return [entry for entry in zip(*[self._recursive_slice_pred(y) for y in x])]
        else:
            raise ValueError(f"Can't unpack object of type {type(x)}.")

    def classify(self, stream, **kwargs):
        """
        Classifies the stream. The classification

        :param stream: Obspy stream to classify
        :type stream: obspy.core.Stream
        :param kwargs:
        :return: A classification for the full stream, e.g., a list of picks or the source magnitude.
        """
        argdict = self.default_args.copy()
        argdict.update(kwargs)

        stream = self.classify_stream_pre(stream, argdict)
        annotations = self.annotate(stream, **argdict)
        return self.classify_aggregate(annotations, argdict)

    def classify_stream_pre(self, stream, argdict):
        """
        Runs preprocessing on stream level for the classify function, e.g., subselecting traces.
        By default, this function will simply return the input stream.
        In contrast to :py:func:`annotate_stream_pre`, this function operates on the original input stream.
        The stream should therefore not be modified in place.
        Note that :py:func:`annotate_stream_pre` will be executed on the output of this stream
        within the :py:func:`classify` function.

        :param stream: Input stream
        :type stream: obspy.Stream
        :param argdict: Dictionary of arguments
        :return: Preprocessed stream
        """
        return stream

    def classify_aggregate(self, annotations, argdict):
        """
        An aggregation function that converts the annotation streams returned by :py:func:`annotate` into
        a classification. A classification may be an arbitrary object. However, when implementing a model which already
        exists in similar form, we recommend using the same output format. For example, all pick outputs should have
        the same format.

        :param annotations: Annotations returned from :py:func:`annotate`
        :param argdict: Dictionary of arguments
        :return: Classification object
        """
        return annotations

    @staticmethod
    def resample(stream, sampling_rate):
        """
        Perform inplace resampling of stream to a given sampling rate.

        :param stream: Input stream
        :type stream: obspy.core.Stream
        :param sampling_rate: Sampling rate (sps) to resample to
        :type sampling_rate: float
        """
        del_list = []
        for i, trace in enumerate(stream):
            if trace.stats.sampling_rate == sampling_rate:
                continue
            if trace.stats.sampling_rate % sampling_rate == 0:
                trace.filter("lowpass", freq=sampling_rate * 0.5, zerophase=True)
                trace.decimate(
                    int(trace.stats.sampling_rate / sampling_rate), no_filter=True
                )
            else:
                # This exception handling is required because very short traces in obspy can cause a crash during resampling.
                # For details see: https://github.com/obspy/obspy/pull/2885
                # TODO: Remove the try except block and bump obspy version requirement to a version without this issue.
                try:
                    trace.resample(sampling_rate, no_filter=True)
                except ZeroDivisionError:
                    del_list.append(i)

        for i in del_list:
            del stream[i]

    def group_stream(self, stream, by="instrument"):
        """
        Perform grouping of input stream, by instrument or channel.

        :param stream: Input stream
        :type stream: obspy.core.Stream
        :return: List of traces grouped by instrument.
        :rtype: list
        """
        groups = defaultdict(list)
        for trace in stream:
            if self._grouping == "instrument":
                groups[trace.id[:-1]].append(trace)
            elif self._grouping == "channel":
                groups[trace.id].append(trace)
            else:
                raise ValueError(f"Unknown grouping parameter '{by}'.")

        return list(groups.values())

    @staticmethod
    def has_mismatching_records(stream):
        """
        Detects if for any id the stream contains overlapping traces that do not match.

        :param stream: Input stream
        :type stream: obspy.core.Stream
        :return: Flag whether there are mismatching records
        :rtype: bool
        """
        stream.merge(-1)  # Ensures overlapping matching traces are merged

        ids = defaultdict(list)
        for trace in stream:
            ids[trace.id].append(trace)

        for traces in ids.values():
            starttimes = sorted(
                [(trace.stats.starttime, i) for i, trace in enumerate(traces)],
                key=lambda x: x[0],
            )
            endtimes = sorted(
                [(trace.stats.endtime, i) for i, trace in enumerate(traces)],
                key=lambda x: x[0],
            )

            for i, _ in enumerate(starttimes):
                if starttimes[i][1] != endtimes[i][1]:
                    return True
                if i > 0 and starttimes[i] < endtimes[i - 1]:
                    return True

        return False

    def stream_to_arrays(
        self, stream, strict=True, flexible_horizontal_components=True
    ):
        """
        Converts streams into a list of start times and numpy arrays.
        Assumes:

        - All traces in the stream are from the same instrument and only differ in the components
        - No overlapping traces of the same component exist
        - All traces have the same sampling rate

        :param stream: Input stream
        :type stream: obspy.core.Stream
        :param strict: If true, only if recordings for all components are available, otherwise impute missing
                       data with zeros.
        :type strict: bool, default True
        :param flexible_horizontal_components: If true, accepts traces with Z12 components as ZNE and vice versa.
                                               This is usually acceptable for rotationally invariant models,
                                               e.g., most picking models.
        :type flexible_horizontal_components: bool
        :return: output_times: Start times for each array
        :return: output_data: Arrays with waveforms
        """

        # Obspy raises an error when trying to compare traces.
        # The seqnum hack guarantees that no two tuples reach comparison of the traces.
        seqnum = 0
        if len(stream) == 0:
            return [], []

        sampling_rate = stream[0].stats.sampling_rate

        if self._grouping == "channel":
            # Use the provided component
            component_order = stream[0].id[-1]
        else:
            component_order = self._component_order

        comp_dict = {c: i for i, c in enumerate(component_order)}

        matches = [
            ("1", "N"),
            ("2", "E"),
        ]  # Component regarded as identical if flexible_horizontal_components is True.
        if flexible_horizontal_components:
            for a, b in matches:
                if a in comp_dict:
                    comp_dict[b] = comp_dict[a]
                elif b in comp_dict:
                    comp_dict[a] = comp_dict[b]

        # Maps traces to the components existing. Allows to warn for mixed use of ZNE and Z12.
        existing_trace_components = defaultdict(list)

        start_sorted = PriorityQueue()
        for trace in stream:
            if trace.id[-1] in comp_dict and len(trace.data) > 0:
                start_sorted.put((trace.stats.starttime, seqnum, trace))
                seqnum += 1
                existing_trace_components[trace.id[:-1]].append(trace.id[-1])

        if flexible_horizontal_components:
            for trace, components in existing_trace_components.items():
                for a, b in matches:
                    if a in components and b in components:
                        seisbench.logger.warning(
                            f"Station {trace} has both {a} and {b} components. "
                            f"This might lead to undefined behavior. "
                            f"Please preselect the relevant components "
                            f"or set flexible_horizontal_components=False."
                        )

        active = (
            PriorityQueue()
        )  # Traces with starttime before the current time, but endtime after
        to_write = (
            []
        )  # Traces that are not active any more, but need to be written in the next array. Irrelevant for strict mode

        output_times = []
        output_data = []
        while True:
            if not start_sorted.empty():
                start_element = start_sorted.get()
            else:
                start_element = None
                if strict:
                    # In the strict case, all data would already have been written
                    break

            if not active.empty():
                end_element = active.get()
            else:
                end_element = None

            if start_element is None and end_element is None:
                # Processed all data
                break
            elif start_element is not None and end_element is None:
                active.put(
                    (start_element[2].stats.endtime, start_element[1], start_element[2])
                )
            elif start_element is None and end_element is not None:
                to_write.append(end_element[2])
            else:
                # both start_element and end_element are active
                if end_element[0] < start_element[0] or (
                    strict and end_element[0] == start_element[0]
                ):
                    to_write.append(end_element[2])
                    start_sorted.put(start_element)
                else:
                    active.put(
                        (
                            start_element[2].stats.endtime,
                            start_element[1],
                            start_element[2],
                        )
                    )
                    active.put(end_element)

            if not strict and active.qsize() == 0 and len(to_write) != 0:
                t0 = min(trace.stats.starttime for trace in to_write)
                t1 = max(trace.stats.endtime for trace in to_write)

                data = np.zeros(
                    (len(component_order), int((t1 - t0) * sampling_rate + 2))
                )  # +2 avoids fractional errors

                for trace in to_write:
                    p = int((trace.stats.starttime - t0) * sampling_rate)
                    cidx = comp_dict[trace.id[-1]]
                    data[cidx, p : p + len(trace.data)] = trace.data

                data = data[:, :-1]  # Remove fractional error +1

                output_times.append(t0)
                output_data.append(data)

                to_write = []

            if strict and active.qsize() == len(component_order):
                traces = []
                while not active.empty():
                    traces.append(active.get()[2])

                t0 = max(trace.stats.starttime for trace in traces)
                t1 = min(trace.stats.endtime for trace in traces)

                short_traces = [trace.slice(t0, t1) for trace in traces]
                data = np.zeros(
                    (len(component_order), len(short_traces[0].data) + 2)
                )  # +2 avoids fractional errors
                for trace in short_traces:
                    cidx = comp_dict[trace.id[-1]]
                    data[cidx, : len(trace.data)] = trace.data

                data = data[:, :-2]  # Remove fractional error +2

                output_times.append(t0)
                output_data.append(data)

                for trace in traces:
                    if t1 < trace.stats.endtime:
                        start_sorted.put((t1, seqnum, trace.slice(starttime=t1)))
                        seqnum += 1

        if self._grouping == "channel":
            # Remove channel dimension
            output_data = [data[0] for data in output_data]

        return output_times, output_data

    @staticmethod
    def picks_from_annotations(annotations, threshold, phase):
        """
        Converts the annotations streams for a single phase to discrete picks using a classical trigger on/off.
        The lower threshold is set to half the higher threshold.
        Picks are represented by :py:class:`~seisbench.util.annotations.Pick` objects.
        The pick start_time and end_time are set to the trigger on and off times.

        :param annotations: Stream of annotations
        :param threshold: Higher threshold for trigger
        :param phase: Phase to label, only relevant for output phase labelling
        :return: List of picks
        """
        picks = []
        for trace in annotations:
            trace_id = (
                f"{trace.stats.network}.{trace.stats.station}.{trace.stats.location}"
            )
            triggers = trigger_onset(trace.data, threshold, threshold / 2)
            times = trace.times()
            for s0, s1 in triggers:
                t0 = trace.stats.starttime + times[s0]
                t1 = trace.stats.starttime + times[s1]

                peak_value = np.max(trace.data[s0 : s1 + 1])
                s_peak = s0 + np.argmax(trace.data[s0 : s1 + 1])
                t_peak = trace.stats.starttime + times[s_peak]

                pick = util.Pick(
                    trace_id=trace_id,
                    start_time=t0,
                    end_time=t1,
                    peak_time=t_peak,
                    peak_value=peak_value,
                    phase=phase,
                )
                picks.append(pick)

        return picks

    @staticmethod
    def detections_from_annotations(annotations, threshold):
        """
        Converts the annotations streams for a single phase to discrete detections using a classical trigger on/off.
        The lower threshold is set to half the higher threshold.
        Detections are represented by :py:class:`~seisbench.util.annotations.Detection` objects.
        The detection start_time and end_time are set to the trigger on and off times.

        :param annotations: Stream of annotations
        :param threshold: Higher threshold for trigger
        :return: List of detections
        """
        detections = []
        for trace in annotations:
            trace_id = (
                f"{trace.stats.network}.{trace.stats.station}.{trace.stats.location}"
            )
            triggers = trigger_onset(trace.data, threshold, threshold / 2)
            times = trace.times()
            for s0, s1 in triggers:
                t0 = trace.stats.starttime + times[s0]
                t1 = trace.stats.starttime + times[s1]
                peak_value = np.max(trace.data[s0 : s1 + 1])

                detection = util.Detection(
                    trace_id=trace_id, start_time=t0, end_time=t1, peak_value=peak_value
                )
                detections.append(detection)

        return detections


class WaveformPipeline(ABC):
    """
    A waveform pipeline is a collection of models that together expose an :py:func:`annotate` and
    a :py:func:`classify` function. Examples of waveform pipelines would be multi-step picking models,
    conducting first a detection with one model and then a pick identification with a second model.
    This could also easily be extended by adding further models, e.g., estimating magnitude for each detection.

    In contrast to :py:class:`WaveformModel`, a waveform pipeline is not a pytorch module and has no forward function.
    This also means, that all components of a pipeline will usually be trained separately. As a rule of thumb,
    if the pipeline can be trained end to end, it should most likely rather be a :py:class:`WaveformModel`.
    For a waveform pipeline, the :py:func:`annotate` and :py:func:`classify` functions are not automatically generated,
    but need to be implemented manually.

    Waveform pipelines offer functionality for downloading pipeline configurations from the SeisBench repository.
    Similarly to :py:class:`SeisBenchModel`, waveform pipelines expose a :py:func:`from_pretrained` function,
    that will download the configuration for a pipeline and its components.

    To implement a waveform pipeline, this class needs to be subclassed. This class will throw an exception when
    trying to instantiate.

    :param components: Dictionary of components contained in the model. This should contain all models used in the
                       pipeline.
    :type components: dict [str, SeisBenchModel]
    :param citation: Citation reference, defaults to None.
    :type citation: str, optional
    """

    def __init__(self, components, citation=None):
        self.components = components
        self._citation = citation
        self._docstring = None

    @classmethod
    @abstractmethod
    def component_classes(cls):
        """
        Returns a mapping of component names to their classes. This function needs to be defined in each pipeline,
        as it is required to load configurations.

        :return: Dictionary mapping component names to their classes.
        :rtype: Dict[str, SeisBenchModel classes]
        """
        return {}

    @property
    def docstring(self):
        return self._docstring

    @property
    def citation(self):
        return self._citation

    @property
    def name(self):
        return self._name_internal()

    @classmethod
    def _name_internal(cls):
        return cls.__name__

    @classmethod
    def _remote_path(cls):
        return os.path.join(
            seisbench.remote_root, "pipelines", cls._name_internal().lower()
        )

    @classmethod
    def _local_path(cls):
        return Path(seisbench.cache_root, "pipelines", cls._name_internal().lower())

    @classmethod
    def _config_path(cls, name):
        return cls._local_path() / f"{name}.json"

    def annotate(self, stream, **kwargs):
        raise NotImplementedError("This class does not expose an annotate function.")

    def classify(self, stream, **kwargs):
        raise NotImplementedError("This class does not expose a classify function.")

    @classmethod
    def from_pretrained(cls, name, force=False, wait_for_file=False):
        """
        Load pipeline from configuration. Automatically loads all dependent pretrained models weights.

        A pipeline configuration is a json file. On the top level, it has three entries:

        - "components": A dictionary listing all contained models and the pretrained weight to use for this model.
                        The instances of these classes will be created using the
                        :py:func:`~SeisBenchModel.from_pretrained` method.
                        The components need to match the components from the dictionary returned by
                        :py:func:`component_classes`.
        - "docstring": A string documenting the pipeline. Usually also contains information on the author.
        - "model_args": Argument dictionary passed to the init function of the pipeline. (optional)

        :param name: Configuration name
        :type name: str
        :param force: Force execution of download callback, defaults to False
        :type force: bool, optional
        :param wait_for_file: Whether to wait on partially downloaded files, defaults to False
        :type wait_for_file: bool, optional
        :return: Pipeline instance
        :rtype: WaveformPipeline
        """
        config_path = cls._config_path(name)
        cls._local_path().mkdir(parents=True, exist_ok=True)

        def download_callback(config_path):
            remote_config_path = os.path.join(cls._remote_path(), f"{name}.json")
            util.download_http(remote_config_path, config_path, progress_bar=False)

        seisbench.util.callback_if_uncached(
            config_path,
            download_callback,
            force=force,
            wait_for_file=wait_for_file,
        )

        with open(config_path, "r") as f:
            config = json.load(f)

        component_classes = cls.component_classes()
        component_weights = config.get("components", {})
        if sorted(component_weights.keys()) != sorted(component_classes.keys()):
            raise ValueError(
                "Invalid configuration. Components don't match between configuration and class."
            )

        components = {
            key: component_classes[key].from_pretrained(
                component_weights[key], force=force, wait_for_file=wait_for_file
            )
            for key in component_weights
        }

        model_args = config.get("model_args", {})
        model = cls(components, **model_args)

        model._docstring = config.get("docstring", None)

        return model

    @classmethod
    def list_pretrained(cls, details=False):
        """
        Returns list of available configurations and optionally their docstrings.

        :param details: If true, instead of a returning only a list, also return their docstrings.
                        Note that this requires to download the json files for each model in the background
                        and is therefore slower. Defaults to false.
        :type details: bool
        :return: List of available weights or dict of weights and their docstrings
        :rtype: list or dict
        """
        remote_path = cls._remote_path()

        try:
            configurations = [
                x[:-5]
                for x in seisbench.util.ls_webdav(remote_path)
                if x.endswith(".json")
            ]
        except ValueError:
            # No weights available
            configurations = []

        if details:
            detail_configurations = {}

            # Create path if necessary
            cls._local_path().mkdir(parents=True, exist_ok=True)

            for configuration in configurations:

                def download_callback(config_path):
                    remote_config_path = os.path.join(
                        cls._remote_path(), f"{configuration}.json"
                    )
                    seisbench.util.download_http(
                        remote_config_path, config_path, progress_bar=False
                    )

                config_path = cls._config_path(configuration)

                seisbench.util.callback_if_uncached(config_path, download_callback)

                with open(config_path, "r") as f:
                    config = json.load(f)
                detail_configurations[configuration] = config.get("docstring", None)

            configurations = detail_configurations

        return configurations


class Conv1dSame(nn.Module):
    """
    Add PyTorch compatible support for Tensorflow/Keras padding option: padding='same'.

    Discussions regarding feature implementation:
    https://discuss.pytorch.org/t/converting-tensorflow-model-to-pytorch-issue-with-padding/84224
    https://github.com/pytorch/pytorch/issues/3867#issuecomment-598264120

    """

    def __init__(self, in_channels, out_channels, kernel_size, stride=1, dilation=1):
        super().__init__()
        self.cut_last_element = (
            kernel_size % 2 == 0 and stride == 1 and dilation % 2 == 1
        )
        self.padding = math.ceil((1 - stride + dilation * (kernel_size - 1)) / 2)
        self.conv = nn.Conv1d(
            in_channels,
            out_channels,
            kernel_size,
            padding=self.padding + 1,
            stride=stride,
            dilation=dilation,
        )

    def forward(self, x):
        if self.cut_last_element:
            return self.conv(x)[:, :, :-1]
        else:
            return self.conv(x)


def hard_sigmoid(x):
    return torch.clip(0.2 * x + 0.5, 0, 1)


class ActivationLSTMCell(nn.Module):
    """
    LSTM Cell using variable gating activation, by default hard sigmoid

    If gate_activation=torch.sigmoid this is the standard LSTM cell

    Uses recurrent dropout strategy from https://arxiv.org/abs/1603.05118 to match Keras implementation.
    """

    def __init__(
        self, input_size, hidden_size, gate_activation=hard_sigmoid, recurrent_dropout=0
    ):
        super(ActivationLSTMCell, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.gate_activation = gate_activation
        self.recurrent_dropout = recurrent_dropout

        self.weight_ih = nn.Parameter(torch.randn(4 * hidden_size, input_size))
        self.weight_hh = nn.Parameter(torch.randn(4 * hidden_size, hidden_size))
        self.bias_ih = nn.Parameter(torch.randn(4 * hidden_size))
        self.bias_hh = nn.Parameter(torch.randn(4 * hidden_size))
        self.init_weights()

    def init_weights(self):
        with torch.no_grad():
            for param in [self.weight_hh, self.weight_ih]:
                for idx in range(4):
                    mul = param.shape[0] // 4
                    torch.nn.init.xavier_uniform_(param[idx * mul : (idx + 1) * mul])

    def forward(self, input, state):
        if state is None:
            hx = torch.zeros(
                input.shape[0], self.hidden_size, device=input.device, dtype=input.dtype
            )
            cx = torch.zeros(
                input.shape[0], self.hidden_size, device=input.device, dtype=input.dtype
            )
        else:
            hx, cx = state
        gates = (
            torch.mm(input, self.weight_ih.t())
            + self.bias_ih
            + torch.mm(hx, self.weight_hh.t())
            + self.bias_hh
        )
        ingate, forgetgate, cellgate, outgate = gates.chunk(4, 1)

        ingate = self.gate_activation(ingate)
        forgetgate = self.gate_activation(forgetgate)
        cellgate = torch.tanh(cellgate)
        outgate = self.gate_activation(outgate)

        if self.recurrent_dropout > 0:
            cellgate = F.dropout(cellgate, p=self.recurrent_dropout)

        cy = (forgetgate * cx) + (ingate * cellgate)
        hy = outgate * torch.tanh(cy)

        return hy, (hy, cy)


class CustomLSTM(nn.Module):
    """
    LSTM to be used with custom cells
    """

    def __init__(self, cell, *cell_args, bidirectional=True, **cell_kwargs):
        super(CustomLSTM, self).__init__()
        self.cell_f = cell(*cell_args, **cell_kwargs)
        self.bidirectional = bidirectional
        if self.bidirectional:
            self.cell_b = cell(*cell_args, **cell_kwargs)

    def forward(self, input, state=None):
        # Forward
        state_f = state
        outputs_f = []
        for i in range(len(input)):
            out, state_f = self.cell_f(input[i], state_f)
            outputs_f += [out]

        outputs_f = torch.stack(outputs_f)

        if not self.bidirectional:
            return outputs_f, None

        # Backward
        state_b = state
        outputs_b = []
        l = input.shape[0] - 1
        for i in range(len(input)):
            out, state_b = self.cell_b(input[l - i], state_b)
            outputs_b += [out]

        outputs_b = torch.flip(torch.stack(outputs_b), dims=[0])

        output = torch.cat([outputs_f, outputs_b], dim=-1)

        # Keep second argument for consistency with PyTorch LSTM
        return output, None
