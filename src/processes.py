from multiprocessing import Process
import connection
import pickle

class Master(Process):
    def __init__(self, config):
        super().__init__()
        self.model = None
        self.sensor_connection = connection.UdpConnection(config)
        self.actuator_connection = connection.RpcConnection(config)
        self.master_connection = None # communication with other masters, none by default

    def read_model(path):
        self.model = pickle.load(path) # placeholder

    def compute_response():
        sensor_data = self.sensor_connection.receive()
        response = self.model.map(sensor_data)
        self.actuator_connection.send(response)


class Sensor(Process):
    def __init__(self, config):
        super().__init__()
        self.master_connection = connection.UdpConnection(config)
        self.actuator_connection = connection.SerialConnection(config)

    def update_config(config):
        pass

    def read_sensor():
        pass

    # preprocess and send data
    def send_data():
        pass

    def reset():
        self.actuator_connection.reset()
        self.master_connection.reset()
        # clear all other member variables
        pass


class Actuator(Process):
    def __init__(self, config):
        super().__init__()
        self.master_connection = connection.RpcConnection(config)
        self.sensor_connection = connection.SerialConnection(config)

    def update_config(config):
        pass

    def send_command():
        pass

    def reset():
        self.sensor_connection.reset()
        self.master_connection.reset()
        # clear all other member variables
        pass