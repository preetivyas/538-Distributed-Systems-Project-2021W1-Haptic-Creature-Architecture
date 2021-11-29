# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import actuator_server_pb2 as actuator__server__pb2


class ActuatorServerStub(object):
    """Interface exported by the server.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.execute_command = channel.unary_unary(
                '/actuator_server.ActuatorServer/execute_command',
                request_serializer=actuator__server__pb2.Command.SerializeToString,
                response_deserializer=actuator__server__pb2.Status.FromString,
                )
        self.execute_sync_init = channel.unary_unary(
                '/actuator_server.ActuatorServer/execute_sync_init',
                request_serializer=actuator__server__pb2.TimestampRequest.SerializeToString,
                response_deserializer=actuator__server__pb2.Timestamp.FromString,
                )
        self.execute_sync = channel.unary_unary(
                '/actuator_server.ActuatorServer/execute_sync',
                request_serializer=actuator__server__pb2.TimestampChange.SerializeToString,
                response_deserializer=actuator__server__pb2.TimestampChangeStatus.FromString,
                )


class ActuatorServerServicer(object):
    """Interface exported by the server.
    """

    def execute_command(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def execute_sync_init(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def execute_sync(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ActuatorServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'execute_command': grpc.unary_unary_rpc_method_handler(
                    servicer.execute_command,
                    request_deserializer=actuator__server__pb2.Command.FromString,
                    response_serializer=actuator__server__pb2.Status.SerializeToString,
            ),
            'execute_sync_init': grpc.unary_unary_rpc_method_handler(
                    servicer.execute_sync_init,
                    request_deserializer=actuator__server__pb2.TimestampRequest.FromString,
                    response_serializer=actuator__server__pb2.Timestamp.SerializeToString,
            ),
            'execute_sync': grpc.unary_unary_rpc_method_handler(
                    servicer.execute_sync,
                    request_deserializer=actuator__server__pb2.TimestampChange.FromString,
                    response_serializer=actuator__server__pb2.TimestampChangeStatus.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'actuator_server.ActuatorServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ActuatorServer(object):
    """Interface exported by the server.
    """

    @staticmethod
    def execute_command(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/actuator_server.ActuatorServer/execute_command',
            actuator__server__pb2.Command.SerializeToString,
            actuator__server__pb2.Status.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def execute_sync_init(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/actuator_server.ActuatorServer/execute_sync_init',
            actuator__server__pb2.TimestampRequest.SerializeToString,
            actuator__server__pb2.Timestamp.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def execute_sync(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/actuator_server.ActuatorServer/execute_sync',
            actuator__server__pb2.TimestampChange.SerializeToString,
            actuator__server__pb2.TimestampChangeStatus.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
