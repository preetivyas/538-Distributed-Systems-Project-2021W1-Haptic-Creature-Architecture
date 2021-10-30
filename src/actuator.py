from multiprocessing import Process
import connection
import pickle
from threading import Thread
import time
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer


class ActuatorClient:
    def __init__(self, config):
        self.ip = config['ip']
        self.port = config['port']
        uri = "http://" + self.ip + ":" + self.port
        self.actuator = ServerProxy(uri)

    def perform(timestamp, command):
        status = self.actuator.execute(timestamp, command)
        return status

class ActuatorServer(Thread):
    def __init__(self, config):
        self.ip = config['ip']
        self.port = int(config['port'])
        self.server = SimpleXMLRPCServer((self.ip, self.port))
        self.sensor_msgs = None

    def execute(self, timestamp, master_command):
        sensor_msgs = self.sensor_msgs

        timestamps = {}
        sensor_commands = {}
        for name, sensor_msg in sensor_msgs.items():
            timestamps[name] = sensor_msg['timestamp']
            sensor_commands[name] = sensor_msg['data']

        use_master = True
        sensor_command = master_command
        for name, sensor_time in timestamps.items():
            if timestamp < timestamps[name] + (0.3 * (10**6)):
                use_master = False
                sensor_command = sensor_commands[name]

        if use_master:
            final_command = master_command
        else:
            final_command = sensor_command
            
        print("performing command: ", final_command)
        status = True
        return status

    def run(self):
        self.server.register_function(self.execute, "execute")
        self.server.serve_forever()

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
        for connection_type, connection_config in config.items():
            name = connection_config['name']
            if 'Rpc' in connection_type:
                self.master_thread = ActuatorServer(connection_config)
            if 'Serial' in connection_type:
                self.sensor_threads[name] = ActuatorToSensor(connection_config)

    def run(self):
        self.master_thread.start()
        for name, thread in self.sensor_threads.items():
            thread.start()

        while True:
            time.sleep(0.1)
            sensor_msgs = {}
            for name, sensors in self.sensor_threads.items():
                sensor_msgs[name] = sensors.sensor_msg

            self.ActuatorServer.sensor_msgs = sensor_msgs