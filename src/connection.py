import socket
import serial
import time


# Define the structure of connection classes
class BaseConnection:
    def __init__(self, config):
        self.connected = False
        self.config = config

    # establish connection (keep trying until success)
    def connect(self):
        pass

    # # start communication and initialize necessary variables ()
    # def start_communication(self):
    #     pass

    # convert arrays into data bytes and send
    def send(self, data):
        pass

    # parse raw data into meaningful arrays
    def receive(self, data):
        pass

    # stop communication
    def end_communication(self):
        pass

    # reset internal states
    def reset(self):
        self.connected = False
        self.end_communication()
        self.connect()


class TcpConnection(BaseConnection):
    def __init__(self, config):
        super().__init__(config)
        self.role = self.config['role'] # server or client
        self.ip = self.config['ip']
        self.port = int(self.config['port'])
        self.buffer_size = int(self.config['buffer_size'])
        self.timeout = self.config['timeout']
        self.connect()

    def connect(self):
        while(self.connected == False):
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.settimeout(self.timeout)
                # self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                if self.role == 'server':
                    self.socket.bind((self.ip, self.port))
                    self.socket.listen(1)
                    self.connection, self.address = self.socket.accept()
                    self.connected = True
                    print('Tcp server connected to: ', self.address)
                elif self.role == 'client':
                    self.socket.connect((self.ip, self.port))
                    self.connected = True
                else:
                    raise ValueError('Unrecognized role: Choose either server or client')
            except ValueError:
                break
            except:
                time.sleep(0.5)
                continue

    def send(self, data):
        if self.connected == True:
            if self.role == 'server':
                self.connection.sendall(data)
            elif self.role == 'client':
                self.socket.sendall(data)
            return True
        else:
            return False

    def receive(self):
        try:
            if self.role == 'server':
                data = self.connection.recv(self.buffer_size)
            elif self.role == 'client':
                data = self.socket.recv(self.buffer_size)
            return True, data
        except socket.timeout:
            self.connected = False
            print('Tcp Timeout')
            return False, None

    def end_communication(self):
        if self.role == 'server':
            self.connection.close()
        else self.role == 'client':
            self.socket.close()
        self.connected = False

class UdpConnection(BaseConnection):
    def __init__(self, config):
        super().__init__(config)
        self.role = self.config['role'] # server or client
        self.ip = self.config['ip']
        self.port = int(self.config['port'])
        self.buffer_size = int(self.config['buffer_size'])
        self.timeout = self.config['timeout']
        self.address = None
        self.connect()

    def connect(self):
        while(self.connected == False):
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.socket.settimeout(self.timeout)
                # self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                if self.role == 'server':
                    self.socket.bind((self.ip, self.port))
                    self.connected = True
                    print('Udp server connected to: ', self.address)
                elif self.role == 'client':
                    self.address = (self.ip, self.port)
                    self.connected = True
                else:
                    raise ValueError('Unrecognized role: Choose either server or client')
            except ValueError:
                break
            except:
                time.sleep(0.5)
                continue

    def send(self, data):
        if connect == True:
            if self.address == None:
                _, self.address = self.socket.recvfrom(self.buffer_size)
            self.socket.sendto(data, self.address)
            return True
        else:
            return False

    def receive(self):
        try:
            data, address = self.socket.recvfrom(self.buffer_size)
            if self.role == 'server':
                self.address = address
                return True, data
            elif self.role == 'client':
                return True, data
        except socket.timeout:
            self.connected = False
            print('Udp Timeout')
            return False, None

    def end_communication(self):
        self.socket.close()
        self.connected = False

class SerialConnection(BaseConnection):
    def __init__(self, config):
        super().__init__(config)
        self.port = self.config['port']
        self.baud_rate = int(self.config['baudrate'])
        self.buffer_size = int(self.config['buffer_size'])
        self.timeout = self.config['timeout']
        self.connect()

    def connect(self):
        while(self.connected == False):
            try:
                self.connection = serial.Serial(self.port, self.baud_rate, timeout=time_out)
                self.connected = True
            except:
                time.sleep(0.5)
                print('Serial open error')
                continue

    def send(self, data):
        if connect == True:
            self.connection.write(data)
            return True
        else:
            return False

    def receive(self):
        try:
            receive_data = self.connection.readline(self.buffer_size)
            return True, data
        except serial.SerialTimeoutException:
            self.connected = False
            print('Serial Timeout')
            return False, None

    def end_communication(self):
        self.connection.close()
        self.connected = False

class RpcConnection(BaseConnection):
    pass