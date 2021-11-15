from multiprocessing import Process
import connection
import pickle
from threading import Thread
import time
import numpy as np

class SensorToMaster(Thread):
    def __init__(self, config):
        super().__init__()
        self.connection = connection.UdpConnection(config)
        self.sensor_msg = {}
        self.clock_change = None

    def read_sensor(self):
        return np.random.rand(3, 10).tolist()

    # preprocess and send data
    def send_data(self,msg):
        msg_bytes = pickle.dumps(msg)
        self.master_connection.send(msg_bytes)

    def run(self):
        self.connection.connect()
        while True:
            time.sleep(0.1)
            msg = {}
            msg['data'] = self.read_sensor()
            msg['timestamp'] = time.time()+self.clock_change
            self.send_data(msg)
            self.sensor_msg = msg


class Sensor(Process):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.master_thread = None
        self.actuator_connections  = {}
        
        for connection_type, connection_config in config.items():
            name = connection_config['name']
            if 'Udp' in connection_type:
                self.master_thread = SensorToMaster(connection_config)
            if 'Serial' in connection_type:
                self.actuator_connections[name] = connection.SerialConnection(connection_config)

    def compute_response(self, name, msg):
        if name == 'actuator_1' and max(msg['data']) >= 1:
            response = 1
        else:
            response = 0
        return response

    def run(self):
       if self.master_thread:
            self.master_thread.start()
       if self.actuator_connections:
            for name, connection in self.actuator_connections.items(): 
                connection.connect()

       while True:
            time.sleep(0.1)
            sensor_msg = self.master_thread.sensor_msg
            for name, connection in self.actuator_connections.items():
                msg = {}
                msg['data'] = self.compute_response(name, sensor_msg)
                msg['timestamp'] = time.time()*(10**6)
                msg_bytes = pickle.dumps(msg)
                status = connection.send(msg_bytes)

