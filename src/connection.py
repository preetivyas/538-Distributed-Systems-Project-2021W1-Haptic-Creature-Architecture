from multiprocessing import Process
import socket


class BaseConnection(Process):
    def __init__(self, config):
        self.connected = False
        self.config = config

    # establish connection
    def connect(self):
        pass

    # start communication and initialize necessary variables
    def start_communication(self):
        self.connect()
        pass

    # stop communication
    def end_communication(self):
        pass

    # reset internal states
    def reset(self):
        pass

    # convert arrays into data bytes and send
    def send(self, data):
        pass

    # parse raw data into meaningful arrays
    def on_receive(self, data):
        pass


class TcpConnection(BaseConnection):
    def __init__(self, config):
        super().__init__(config)
        self.local_ip = self.config['local_ip']
        self.local_port = int(self.config['local_port'])
        self.remote_ip = self.config['remote_ip']
        self.remote_port = int(self.config['remote_port'])

    def send(self, data, ack = False): # ack probably not needed for tcp
        pass


class UdpConnection(BaseConnection):
    pass

class RpcConnection(BaseConnection):
    pass

class SerialConnection(BaseConnection):
    pass