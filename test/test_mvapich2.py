# Copyright (c) 2018, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable=invalid-name, too-few-public-methods, bad-continuation

"""Test cases for the mvapich2 module"""

from __future__ import unicode_literals
from __future__ import print_function

import logging # pylint: disable=unused-import
import unittest

from helpers import docker

from hpccm.mvapich2 import mvapich2

class Test_mvapich2(unittest.TestCase):
    def setUp(self):
        """Disable logging output messages"""
        logging.disable(logging.ERROR)

    @docker
    def test_defaults(self):
        """Default mvapich2 building block"""
        mv2 = mvapich2()
        self.assertEqual(str(mv2),
r'''# MVAPICH2 version 2.3b
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        byacc \
        file \
        openssh-client \
        wget && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p /tmp && wget -q --no-check-certificate -P /tmp http://mvapich.cse.ohio-state.edu/download/mvapich/mv2/mvapich2-2.3b.tar.gz && \
    tar -x -f /tmp/mvapich2-2.3b.tar.gz -C /tmp -z && \
    cd /tmp/mvapich2-2.3b &&   ./configure --prefix=/usr/local/mvapich2 --disable-mcast --with-cuda=/usr/local/cuda && \
    make -j4 && \
    make -j4 install && \
    rm -rf /tmp/mvapich2-2.3b.tar.gz /tmp/mvapich2-2.3b
ENV LD_LIBRARY_PATH=/usr/local/mvapich2/lib:$LD_LIBRARY_PATH \
    PATH=/usr/local/mvapich2/bin:$PATH''')

    @docker
    def test_directory(self):
        """Directory in local build context"""
        mv2 = mvapich2(directory='mvapich2-2.3')
        self.assertEqual(str(mv2),
r'''# MVAPICH2
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        byacc \
        file \
        openssh-client \
        wget && \
    rm -rf /var/lib/apt/lists/*
COPY mvapich2-2.3 /tmp/mvapich2-2.3
RUN cd /tmp/mvapich2-2.3 &&   ./configure --prefix=/usr/local/mvapich2 --disable-mcast --with-cuda=/usr/local/cuda && \
    make -j4 && \
    make -j4 install && \
    rm -rf /tmp/mvapich2-2.3
ENV LD_LIBRARY_PATH=/usr/local/mvapich2/lib:$LD_LIBRARY_PATH \
    PATH=/usr/local/mvapich2/bin:$PATH''')

    @docker
    def test_runtime(self):
        """Runtime"""
        mv2 = mvapich2()
        r = mv2.runtime()
        s = '\n'.join(str(x) for x in r)
        self.assertEqual(s,
r'''# MVAPICH2
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        openssh-client && \
    rm -rf /var/lib/apt/lists/*
COPY --from=0 /usr/local/mvapich2 /usr/local/mvapich2
ENV LD_LIBRARY_PATH=/usr/local/mvapich2/lib:$LD_LIBRARY_PATH \
    PATH=/usr/local/mvapich2/bin:$PATH''')
