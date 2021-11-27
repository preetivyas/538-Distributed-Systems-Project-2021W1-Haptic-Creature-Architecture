# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import master_server_pb2 as master__server__pb2


class MasterServerStub(object):
    """Interface exported by the server.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.get_sensor_data = channel.unary_unary(
                '/master_server.MasterServer/get_sensor_data',
                request_serializer=master__server__pb2.SensorName.SerializeToString,
                response_deserializer=master__server__pb2.SensorData.FromString,
                )
        self.sync_init = channel.unary_unary(
                '/master_server.MasterServer/sync_init',
                request_serializer=master__server__pb2.TimestampRequest.SerializeToString,
                response_deserializer=master__server__pb2.Timestamp.FromString,
                )
        self.sync = channel.unary_unary(
                '/master_server.MasterServer/sync',
                request_serializer=master__server__pb2.TimestampChange.SerializeToString,
                response_deserializer=master__server__pb2.TimestampChangeStatus.FromString,
                )


class MasterServerServicer(object):
    """Interface exported by the server.
    """

    def get_sensor_data(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def sync_init(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def sync(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MasterServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'get_sensor_data': grpc.unary_unary_rpc_method_handler(
                    servicer.get_sensor_data,
                    request_deserializer=master__server__pb2.SensorName.FromString,
                    response_serializer=master__server__pb2.SensorData.SerializeToString,
            ),
            'sync_init': grpc.unary_unary_rpc_method_handler(
                    servicer.sync_init,
                    request_deserializer=master__server__pb2.TimestampRequest.FromString,
                    response_serializer=master__server__pb2.Timestamp.SerializeToString,
            ),
            'sync': grpc.unary_unary_rpc_method_handler(
                    servicer.sync,
                    request_deserializer=master__server__pb2.TimestampChange.FromString,
                    response_serializer=master__server__pb2.TimestampChangeStatus.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'master_server.MasterServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class MasterServer(object):
    """Interface exported by the server.
    """

    @staticmethod
    def get_sensor_data(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/master_server.MasterServer/get_sensor_data',
            master__server__pb2.SensorName.SerializeToString,
            master__server__pb2.SensorData.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def sync_init(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/master_server.MasterServer/sync_init',
            master__server__pb2.TimestampRequest.SerializeToString,
            master__server__pb2.Timestamp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def sync(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/master_server.MasterServer/sync',
            master__server__pb2.TimestampChange.SerializeToString,
            master__server__pb2.TimestampChangeStatus.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)