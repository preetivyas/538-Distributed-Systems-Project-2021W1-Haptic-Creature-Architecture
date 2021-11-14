from multiprocessing import Process
from concurrent import futures
import connection
import pickle
from threading import Thread
import time

import grpc
import actuator_server_pb2
import actuator_server_pb2_grpc


class ActuatorClient:
    def __init__(self, config):
        self.ip = config['ip']
        self.port = config['port']
        address = self.ip + ":" + self.port
        channel = grpc.insecure_channel(address)
        self.actuator = actuator_server_pb2_grpc.ActuatorServerStub(channel)

    def perform(self, timestamp, command):
        command_msg = actuator_server_pb2.Command(timestamp=timestamp, master_command=command)
        status_msg = self.actuator.execute(command_msg) #PV: where execute is called? is this calling actuatorservicer?
        return status_msg.status

class ActuatorServicer(actuator_server_pb2_grpc.ActuatorServerServicer):
    def __init__(self):
        self.master_command_msg = {}

    def execute(self, request, context):

        self.master_command_msg['timestamp'] = request.timestamp
        self.master_command_msg['data'] = request.master_command

        #PV: todo: add actuator action code?

        timestamp_new = time.time()
        status = True
        return_msg = actuator_server_pb2.Status(timestamp=timestamp_new, status=status)
        return return_msg

class ActuatorToSensor(Thread):
    def __init__(self, config):
        super().__init__()
        self.connection = connection.SerialConnection(config)
        self.sensor_msg = {}

    def run(self):
        self.connection.connect()
        while True:
            time.sleep(0.1)
            success, msg_bytes = self.connection.receive()
            if success:
                msg = pickle.loads(msg_bytes)
                self.sensor_msg = msg
            else:
                self.connection.connect()

class Actuator(Process):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.master_thread = None
        self.sensor_threads = {}
        for connection_type, connection_config in config.items():
            name = connection_config['name']
            if 'Rpc' in connection_type:
                self.master_thread = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
                self.master_servicer = ActuatorServicer()
                actuator_server_pb2_grpc.add_ActuatorServerServicer_to_server(
                    self.master_servicer, self.master_thread)
                address = config['ip'] + ':' + config['port']
                self.master_thread.add_insecure_port(address)
            if 'Serial' in connection_type:
                self.sensor_threads[name] = ActuatorToSensor(connection_config)

    def run(self):
        if self.master_thread:
            self.master_thread.start()
            self.master_thread.wait_for_termination()
        elif self.sensor_threads:
            for name, thread in self.sensor_threads.items():
                thread.start()

        while True:
            time.sleep(0.1)
            sensor_msgs = {}
            sensor_timestamps = {}
            sensor_commands = {}
            for name, sensors in self.sensor_threads.items():
                sensor_msgs[name] = sensors.sensor_msg
                sensor_timestamps[name] = sensors.sensor_msg['timestamp']
                sensor_commands[name] = sensors.sensor_msg['data']

            master_command_msg = self.master_servicer.master_command_msg
            master_timestamp = master_command_msg['master_timestamp']
            master_command = master_command_msg['data']

            use_master = True
            sensor_command = master_command
            for name, sensor_time in sensor_timestamps.items():
                if master_timestamp < sensor_timestamps[name] + (0.3 * (10**6)):
                    use_master = False
                    sensor_command = sensor_commands[name]

            if use_master:
                final_command = master_command
            else:
                final_command = sensor_command
                
            print("performing command: ", final_command)