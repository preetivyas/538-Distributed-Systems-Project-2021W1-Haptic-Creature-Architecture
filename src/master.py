from multiprocessing import Process
import connection
import pickle
from threading import Thread
import time
from actuator import ActuatorClient
import grpc
import master_server_pb2
import master_server_pb2_grpc
import numpy as np

class MasterToSensor(Thread):
    def __init__(self, config):
        super().__init__()
        self.connection = connection.UdpConnection(config)
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


class MasterServicer(master_server_pb2_grpc.MasterServerServicer):
    def __init__(self):
        self.sensor_msgs = None

    def get_sensor_data(self, request, context):

        sensor_name = request.name

        data = sensor_msgs[name]
        sensor_proto = master_server_pb2.SensorData()
        data_array = np.array(data)

        sensor_proto.timestamp = time.time()
        sensor_proto.row_number = data_array.shape[1]
        sensor_proto.col_number = data_array.shape[0]

        data_flat = data_array.flatten().tolist()
        sensor_proto.sensor_data.extend(data_flat)
        return sensor_proto


class MasterToMaster(Thread):
    def __init__(self, config):
        super().__init__()
        self.model = None

        self.master_server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        self.master_servicer = MasterServicer()
        master_server_pb2_grpc.add_MasterServerServicer_to_server(
            self.master_servicer, self.master_server)
        my_address = config['my_ip'] + ':' + config['my_port']
        self.master_server.add_insecure_port(my_address)

        their_address = config['their_ip'] + ":" + config['their_port']
        channel = grpc.insecure_channel(their_address)
        self.proxy = master_server_pb2_grpc.MasterServerStub(channel)

    def run(self):
        self.connection.connect()
        self.master_thread.start()
        self.master_thread.wait_for_termination()
        while True:
            time.sleep(0.1)


class Master(Process):
    def __init__(self, config):
        super().__init__()
        self.model = None
        self.sensor_threads = {}
        self.actuator_clients = {}
        self.other_master_threads = {}
        self.config = config
        self.other_master_present = False
        for connection_type, connection_config in config.items():
            name = connection_config['name']
            if 'Udp' in connection_type:
                self.sensor_threads[name] = MasterToSensor(connection_config)
            if 'Rpc' in connection_type:
                if 'master' in name:
                    self.other_master_present = True
                    self.other_master_threads[name] = MasterToMaster(connection_config)
                else:
                    self.actuator_clients[name] = ActuatorClient(connection_config)

    def read_model(path):
        self.model = pickle.load(path) # placeholder
        for name, master in self.other_master_threads.items():
            master.model = self.model

    def compute_response(self, sensor_msgs, other_sensor_msgs=None):
        data = {}
        timestamps = {}
        for name, sensor_msg in sensor_msgs.items():
            data[name] = sensor_msg['data']
            timestamps[name] = sensor_msg['timestamp']
        responses = [1, 1, 1, 1]
        return responses

    def parse_sensor_protobuf(self, sensor_proto):
        timestamp = sensor_proto.timestamp
        row_num = sensor_proto.row_number
        col_num = sensor_proto.col_number
        data_flat = []
        for val in sensor_proto.sensor_data:
            data_flat.append(val)
        data_flat = np.array(data_flat)
        data = data_flat.reshape(row_num, col_num)
        sensor_msg = {}
        sensor_msg['timestamp'] = timestamp
        sensor_msg['data'] = data.tolist()
        return sensor_msg

    def run(self):
        
        # self.read_model(self.config['model_path'])
        for name, sensor in self.sensor_threads.items():
            sensor.start()
        for name, master in self.other_master_threads.items():
            master.start()
        while True:
            time.sleep(0.1)
            sensor_msgs = {}
            other_sensor_msgs = {}

            for name, sensors in self.sensor_threads.items():
                sensor_msgs[name] = sensors.sensor_msg

            if self.other_master_present:
                for other_master_name, master in self.other_master_threads.items():
                    master.master_servicer.sensor_msgs = sensor_msgs

                    for sensor_name, sensor in self.sensor_threads.items():
                        sensor_of_interest = other_master_name + '_' + sensor_name
                        sensor_name_msg = master_server_pb2.SensorName(name=sensor_name)
                        sensor_of_interest_proto = master.proxy.get_sensor_data(sensor_name_msg)
                        other_sensor_msgs[sensor_of_interest] = self.parse_sensor_protobuf(sensor_of_interest_proto)
            # responses = self.compute_response(sensor_msgs, other_sensor_msgs)
            responses = [1, 1, 1, 1]

            for name, actuator in self.actuator_clients.items():
                response = responses[name]
                timestamp = time.time() * (10**6)
                actuator.perform(timestamp, response)
