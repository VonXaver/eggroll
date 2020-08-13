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

import argparse
import configparser
import logging
import os
import shutil
import signal
import time
from collections.abc import Iterable
from concurrent import futures
import threading
import platform

import grpc
import numpy as np

from eggroll.core.client import ClusterManagerClient
from eggroll.core.command.command_router import CommandRouter
from eggroll.core.command.command_service import CommandServicer
from eggroll.core.conf_keys import SessionConfKeys, \
    ClusterManagerConfKeys, RollPairConfKeys, CoreConfKeys
from eggroll.core.constants import ProcessorTypes, ProcessorStatus, SerdesTypes
from eggroll.core.datastructure.broker import FifoBroker
from eggroll.core.meta_model import ErPair
from eggroll.core.meta_model import ErTask, ErProcessor, ErEndpoint
from eggroll.core.proto import command_pb2_grpc, transfer_pb2_grpc
from eggroll.core.transfer.transfer_service import GrpcTransferServicer, \
    TransferService
from eggroll.core.utils import _exception_logger
from eggroll.core.utils import hash_code
from eggroll.core.utils import set_static_er_conf, get_static_er_conf
from eggroll.roll_pair import create_adapter, create_serdes, create_functor
from eggroll.roll_pair.transfer_pair import TransferPair
from eggroll.roll_pair.utils.pair_utils import generator, partitioner, \
    set_data_dir
from eggroll.utils.log_utils import get_logger
from eggroll.utils.profile import get_system_metric

L = get_logger()


class EggFrame(object):
    def __init__(self):
        self.functor_serdes = create_serdes(SerdesTypes.CLOUD_PICKLE)

    def __partitioner(self, hash_func, total_partitions):
        return lambda k: hash_func(k) % total_partitions

    @_exception_logger
    def run_task(self, task: ErTask):
        L.info(f"run task called for task._id={task._id}")
        f = self.functor_serdes.deserialize(task._job._functors[0]._body)
        f_result = f(task)

        result = ErPair(key=self.functor_serdes.serialize(task._id),
                        value=self.functor_serdes.serialize(f_result))
        return result


def serve(args):
    prefix = 'v1/egg-frame'

    set_data_dir(args.data_dir)

    CommandRouter.get_instance().register(
        service_name=f"{prefix}/runTask",
        route_to_module_name="eggroll.roll_frame.egg_frame",
        route_to_class_name="EggFrame",
        route_to_method_name="run_task")

    max_workers = 96
    command_server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=max_workers,
        thread_name_prefix="eggpair-command-server"),
        options=[
            ("grpc.max_metadata_size",
             int(CoreConfKeys.EGGROLL_CORE_GRPC_SERVER_CHANNEL_MAX_INBOUND_METADATA_SIZE.get())),
            ('grpc.max_send_message_length',
             int(CoreConfKeys.EGGROLL_CORE_GRPC_SERVER_CHANNEL_MAX_INBOUND_MESSAGE_SIZE.get())),
            ('grpc.max_receive_message_length',
             int(CoreConfKeys.EGGROLL_CORE_GRPC_SERVER_CHANNEL_MAX_INBOUND_MESSAGE_SIZE.get()))])

    command_servicer = CommandServicer()
    command_pb2_grpc.add_CommandServiceServicer_to_server(command_servicer,
                                                          command_server)

    transfer_servicer = GrpcTransferServicer()

    port = args.port
    transfer_port = args.transfer_port

    port = command_server.add_insecure_port(f'[::]:{port}')

    if transfer_port == "-1":
        transfer_server = command_server
        transfer_port = port
        transfer_pb2_grpc.add_TransferServiceServicer_to_server(transfer_servicer,
                                                                transfer_server)
    else:
        transfer_server_max_workers = 48
        transfer_server = grpc.server(futures.ThreadPoolExecutor(
            max_workers=transfer_server_max_workers,
            thread_name_prefix="transfer_server"),
            options=[
                ('grpc.max_metadata_size',
                 int(CoreConfKeys.EGGROLL_CORE_GRPC_SERVER_CHANNEL_MAX_INBOUND_METADATA_SIZE.get())),
                ('grpc.max_send_message_length',
                 int(CoreConfKeys.EGGROLL_CORE_GRPC_SERVER_CHANNEL_MAX_INBOUND_MESSAGE_SIZE.get())),
                ('grpc.max_receive_message_length',
                 int(CoreConfKeys.EGGROLL_CORE_GRPC_SERVER_CHANNEL_MAX_INBOUND_MESSAGE_SIZE.get()))])
        transfer_port = transfer_server.add_insecure_port(f'[::]:{transfer_port}')
        transfer_pb2_grpc.add_TransferServiceServicer_to_server(transfer_servicer,
                                                                transfer_server)
        transfer_server.start()
    pid = os.getpid()

    L.info(f"starting egg_pair service, port: {port}, transfer port: {transfer_port}, pid: {pid}")
    command_server.start()

    cluster_manager = args.cluster_manager
    myself = None
    cluster_manager_client = None
    if cluster_manager:
        session_id = args.session_id
        server_node_id = int(args.server_node_id)
        static_er_conf = get_static_er_conf()
        static_er_conf['server_node_id'] = server_node_id

        if not session_id:
            raise ValueError('session id is missing')
        options = {
            SessionConfKeys.CONFKEY_SESSION_ID: args.session_id
        }
        myself = ErProcessor(id=int(args.processor_id),
                             server_node_id=server_node_id,
                             processor_type=ProcessorTypes.EGG_PAIR,
                             command_endpoint=ErEndpoint(host='localhost', port=port),
                             transfer_endpoint=ErEndpoint(host='localhost', port=transfer_port),
                             pid=pid,
                             options=options,
                             status=ProcessorStatus.RUNNING)

        cluster_manager_host, cluster_manager_port = cluster_manager.strip().split(':')

        L.info(f'egg_pair cluster_manager: {cluster_manager}')
        cluster_manager_client = ClusterManagerClient(options={
            ClusterManagerConfKeys.CONFKEY_CLUSTER_MANAGER_HOST: cluster_manager_host,
            ClusterManagerConfKeys.CONFKEY_CLUSTER_MANAGER_PORT: cluster_manager_port
        })
        cluster_manager_client.heartbeat(myself)

    L.info(f'egg_pair started at port {port}, transfer_port {transfer_port}')

    run = True

    def exit_gracefully(signum, frame):
        nonlocal run
        run = False
        L.info(f'egg_pair {args.processor_id} at port {port}, transfer_port {transfer_port}, pid {pid} receives signum {signal.getsignal(signum)}, stopping gracefully.')

    signal.signal(signal.SIGTERM, exit_gracefully)
    signal.signal(signal.SIGINT, exit_gracefully)

    while run:
        time.sleep(1)

    if cluster_manager:
        myself._status = ProcessorStatus.STOPPED
        cluster_manager_client.heartbeat(myself)

    L.info(f'system metric at exit: {get_system_metric(1)}')
    L.info(f'egg_pair {args.processor_id} at port {port}, transfer_port {transfer_port}, pid {pid} stopped gracefully')


if __name__ == '__main__':
    L.info(f'system metric at start: {get_system_metric(0.1)}')
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('-d', '--data-dir')
    args_parser.add_argument('-cm', '--cluster-manager')
    args_parser.add_argument('-nm', '--node-manager')
    args_parser.add_argument('-s', '--session-id')
    args_parser.add_argument('-p', '--port', default='0')
    args_parser.add_argument('-t', '--transfer-port', default='0')
    args_parser.add_argument('-sn', '--server-node-id')
    args_parser.add_argument('-prid', '--processor-id', default='0')
    args_parser.add_argument('-c', '--config')

    args = args_parser.parse_args()

    EGGROLL_HOME = os.environ['EGGROLL_HOME']
    configs = configparser.ConfigParser()
    if args.config:
        conf_file = args.config
        L.info(f'reading config path: {conf_file}')
    else:
        conf_file = f'{EGGROLL_HOME}/conf/eggroll.properties'
        L.info(f'reading default config: {conf_file}')

    configs.read(conf_file)
    set_static_er_conf(configs['eggroll'])
    if configs:
        if not args.data_dir:
            args.data_dir = configs['eggroll']['eggroll.data.dir']

    L.info(args)
    serve(args)