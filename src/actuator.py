from multiprocessing import Process
from concurrent import futures
import connection
import pickle
from threading import Thread
import time

import grpc
import actuator_server_pb2
import actuator_server_pb2_grpc


class ActuatorClient: #actuator client is actually master, master run functions in this class
    def __init__(self, config):
        self.ip = config['ip']
        self.port = config['port']
        address = self.ip + ":" + self.port
        channel = grpc.insecure_channel(address)
        self.actuator = actuator_server_pb2_grpc.ActuatorServerStub(channel)

    def perform_command(self, timestamp, command):
        try:
            command_msg = actuator_server_pb2.Command(timestamp=timestamp, master_command=command)
            status_msg = self.actuator.execute_command(command_msg)
            return status_msg.status
        except Exception as e:
            print("Perform Command Error:", e)
            return False

    def perform_sync_init(self, timestamp, sync_request):
        try:
            timestamprequest_msg = actuator_server_pb2.TimestampRequest(timestamp=timestamp, sync_request=sync_request)
            timestamp_msg = self.actuator.execute_sync_init(timestamprequest_msg) 
            return True, timestamp_msg.timestamp
        except Exception as e:
            print("Perform Sync Init Error: ", e)
            return False, 0.0

    def perform_sync(self, timestamp, change):
        try:
            timestampsync_msg = actuator_server_pb2.TimestampChange(timestamp=timestamp, change= change)
            status_msg = self.actuator.execute_sync(timestampsync_msg) 
            return status_msg.status
        except Exception as e:
            print("Perform Sync Error: ", e)
            return False

class ActuatorServicer(actuator_server_pb2_grpc.ActuatorServerServicer):
    def __init__(self):
        self.master_command_msg = {}
        self.master_timechange_msg = None
        self.clock_change = 0.0

    def execute_command(self, request, context):

        self.master_command_msg['timestamp'] = request.timestamp
        self.master_command_msg['data'] = request.master_command

        #PV: todo: add actuator action code?
    
        timestamp_new = int(time.time()*(10**6)+ self.clock_change)
        status = True
        return_msg = actuator_server_pb2.Status(timestamp=timestamp_new, status=status)
        return return_msg

    def execute_sync_init (self, request, context):
        if request.sync_request: #sync_request message is true then return the current time stampe
            timestamp_sync = int(time.time()*(10**6)+ self.clock_change)
            return actuator_server_pb2.Timestamp(timestamp=timestamp_sync)
        else:
            return actuator_server_pb2.Timestamp(timestamp=0.0)        

    def execute_sync (self, request, context):
        self.clock_change  = request.change
        #PV:  self.master_timesync_msg will be added to all timestamp values
        status = True
        return actuator_server_pb2.TimestampChangeStatus(status=status)
        

class ActuatorToSensor(Thread):
    def __init__(self, config):
        super().__init__()
        self.connection = connection.SerialConnection(config)
        self.sensor_msg = None

    def run(self):
        self.connection.connect()
        while True:
            time.sleep(0.1)
            success, msg_bytes = self.connection.receive()
            if success:
                if len(msg_bytes) != 0:
                    msg = pickle.loads(msg_bytes)
                    self.sensor_msg = msg
            else:
                self.connection.connect()

class Actuator(Process):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.master_thread = None
        self.default_command = 0.0
        self.sensor_threads = {}
        for connection_type, connection_config in config.items():
            if 'Rpc' in connection_type:
                self.master_thread = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
                self.master_servicer = ActuatorServicer()
                actuator_server_pb2_grpc.add_ActuatorServerServicer_to_server(
                    self.master_servicer, self.master_thread)
                address = connection_config['ip'] + ':' + connection_config['port']
                self.master_thread.add_insecure_port(address)
            if 'Serial' in connection_type:
                name = connection_config['name']
                self.sensor_threads[name] = ActuatorToSensor(connection_config)
                self.sensor_threads[name].daemon = True

    def run(self):
        if self.master_thread:
            self.master_thread.start()

        if self.sensor_threads:
            for name, thread in self.sensor_threads.items():
                thread.start()

        master_timestamp = time.time()*(10**6)
        
        while True:
            time.sleep(0.1)
            master_command = self.default_command
            sensor_msgs = {}
            sensor_timestamps = {}
            sensor_commands = {}
            for name, sensors in self.sensor_threads.items():
                if sensors.sensor_msg != None:
                    sensor_msgs[name] = sensors.sensor_msg
                    sensor_timestamps[name] = sensors.sensor_msg['timestamp']
                    sensor_commands[name] = sensors.sensor_msg['data']

            if self.master_thread != None:
                master_command_msg = self.master_servicer.master_command_msg
                if len(master_command_msg) != 0:
                    master_timestamp = master_command_msg['timestamp']
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
                
            # print("performing command: ", final_command)