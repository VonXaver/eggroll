# -*- coding: utf-8 -*-
#  Copyright (c) 2019 - now, Eggroll Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import numpy as np
import pandas as pd
import pyarrow as pa
from typing import Iterable

import cloudpickle
from eggroll.core.serdes.eggroll_serdes import PickleSerdes, \
    CloudPickleSerdes, EmptySerdes, eggroll_pickle_loads


class FrameBatch:
    def __init__(self, data, schema=None):
        if isinstance(data, FrameBatch):
            self._data = data._data
            self._schema = data._schema
        elif isinstance(data, bytes):
            context = pa.default_serialization_context()
            fb = FrameBatch(context.deserialize(data))
            self._data = fb._data
            self._schema = fb._schema
        elif isinstance(data, dict):
            fb = FrameBatch(pa.deserialize_components(data))
            self._data = fb._data
            self._schema = fb._schema
        elif isinstance(data, pd.DataFrame):
            fb = pa.RecordBatch.from_pandas(data)
            self._data = fb
            self._schema = fb.schema
        elif isinstance(data, pd.Series):
            fb = pa.RecordBatch.from_pandas(data.to_frame().transpose())
            self._data = fb
            self._schema = fb.schema
        elif isinstance(data, pa.RecordBatch):
            self._data = data
            self._schema = data.schema
        else:
            self._data = data
            self._schema = schema

    def __getitem__(self, item):
        return self.to_pandas().__getitem__(item)

    def to_pandas(self):
        return self._data.to_pandas()

    @staticmethod
    def from_pandas(obj):
        return FrameBatch(obj)

    @staticmethod
    def concat(frames: Iterable):
        frame = pd.concat(FrameBatch(f).to_pandas() for f in frames)
        return FrameBatch(frame)

    # TODO:0: implement numpy's empty interface
    @staticmethod
    def empty():
        return FrameBatch(data=None, schema=None)


class TensorBatch:
    META_SHAPE_KEY = bytes("eggroll.rollframe.tensor.shape", encoding="utf8")
    META_BLOCK_START_KEY = bytes("eggroll.rollframe.tensor.block.start", encoding="utf8")
    META_BLOCK_END_KEY = bytes("eggroll.rollframe.tensor.block.end", encoding="utf8")

    def __init__(self,
                 data,
                 block_start: tuple = None,
                 block_end: tuple = None,
                 options: dict = None):
        if options is None:
            options = dict()

        if isinstance(data, FrameBatch):
            self._shape = TensorBatch._bytes_to_int_tuple(data._schema.metadata[TensorBatch.META_SHAPE_KEY])
            self._block_start = TensorBatch._bytes_to_int_tuple(data._schema.metadata[TensorBatch.META_BLOCK_START_KEY])
            self._block_end = TensorBatch._bytes_to_int_tuple(data._schema.metadata[TensorBatch.META_BLOCK_END_KEY])
            self._data = pa.Tensor.from_numpy(data._data.to_pandas().to_numpy().reshape(self._shape))
        elif isinstance(data, np.ndarray):
            self._data = pa.Tensor.from_numpy(data)
            self._shape = self._data.shape
            self._block_start = (0, 0) if block_start is None else block_start
            self._block_end = data.shape if block_end is None else block_end
        else:
            self._data = data
            self._shape = data.shape
            self._block_start = block_start
            self._block_end = block_end

    def __setstate__(self, state):
        self.__init__(state[0], state[1])

    def __getstate__(self):
        return self._data.to_numpy(), self._shape

    @staticmethod
    def _int_tuple_to_str(t: tuple):
        return bytes(",".join(str(x) for x in t), encoding="utf8")

    @staticmethod
    def _bytes_to_int_tuple(s):
        return tuple(int(x) for x in s.decode(encoding="utf8").split(","))

    def _get_metadata(self):
        result = {}
        result[TensorBatch.META_SHAPE_KEY] = TensorBatch._int_tuple_to_str(self._shape)
        if self._block_start is not None:
            result[TensorBatch.META_BLOCK_START_KEY] = TensorBatch._int_tuple_to_str(self._block_start)

        if self._block_end is not None:
            result[TensorBatch.META_BLOCK_END_KEY] = TensorBatch._int_tuple_to_str(self._block_end)

        return result

    def _set_metadata(self):
        pass

    def to_numpy(self, reshape=True) -> np.ndarray:
        result = self._data.to_numpy()
        if reshape:
            result = result.reshape(self._shape)

        return result

    @staticmethod
    def from_numpy(np_array: np.ndarray):
        return TensorBatch(np_array)

    def to_frame(self):
        return FrameBatch(pa.RecordBatch.from_arrays(arrays=[self.to_numpy().reshape(-1)],
                                                     names=['__data'],
                                                     metadata=self._get_metadata()))

    @staticmethod
    def from_frame(frame: FrameBatch):
        return TensorBatch(frame)


def create_functor(func_bin):
    try:
        return cloudpickle.loads(func_bin)
    except:
        return eggroll_pickle_loads(func_bin)