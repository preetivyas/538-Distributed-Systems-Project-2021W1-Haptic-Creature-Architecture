from multiprocessing import Process
import connection
import pickle
from threading import Thread
import time
from actuator import ActuatorClient

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


class MasterToMaster(Thread):
    def __init__(self, config):
        super().__init__()
        self.connection = connection.TcpConnection(config)

    def run(self):
        self.connection.connect()
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
        for connection_type, connection_config in config.items():
            name = connection_config['name']
            if 'Udp' in connection_type:
                self.sensor_threads[name] = MasterToSensor(connection_config)
            if 'Rpc' in connection_type:
                self.actuator_clients[name] = ActuatorClient(connection_config)
            if 'Tcp' in connection_type:
                self.other_master_threads[name] = MasterToMaster(connection_config)

    def read_model(path):
        self.model = pickle.load(path) # placeholder

    def compute_response(self, sensor_msgs):
        data = {}
        timestamps = {}
        for name, sensor_msg in sensor_msgs.items():
            data[name] = sensor_msg['data']
            timestamps[name] = sensor_msg['timestamp']
        responses = [1, 1, 1, 1]
        return responses

    def run(self):
        # self.read_model(self.config['model_path'])
        for name, sensor in self.sensor_threads.items():
            sensor.start()
        for name, master in self.other_master_threads.items():
            master.start()
        while True:
            time.sleep(0.1)
            sensor_msgs = {}

            for name, sensors in self.sensor_threads.items():
                sensor_msgs[name] = sensors.sensor_msg

            # responses = self.compute_response(sensor_msgs)
            responses = [1, 1, 1, 1]

            for name, actuator in self.actuator_clients.items():
                response = responses[name]
                timestamp = time.time() * (10**6)
                actuator.perform(timestamp, response)
