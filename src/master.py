from multiprocessing import Process
from concurrent import futures

from numpy.lib.function_base import diff
import connection
import pickle
from threading import Thread
import time
from actuator import ActuatorClient
import grpc
import master_server_pb2
import master_server_pb2_grpc
import numpy as np

#handling data from local sensor
class MasterToSensor(Thread):

    def __init__(self, config):
        super().__init__()
        self.connection = connection.UdpConnection(config)
        self.sensor_msg = {}
        self.master_msg = {}
        self.time_stamp = None
        self.time_sync = False #flag if true initiates time sync code
        self.time_change = False #flag is true sends clock_change to sensors
        self.clock_change = 0.0 #update for each node 
        self.clock_node = 0.0 #clock of the sensor node

    # preprocess and send data
    def send_data(self,msg):
        msg_bytes = pickle.dumps(msg)
        self.connection.send(msg_bytes)

    def run(self):
        self.connection.connect()
        while True:
            time.sleep(0.1)
            success, msg_bytes = self.connection.receive()
            msg_send = {}
            if success:
                msg = pickle.loads(msg_bytes)
                self.sensor_msg = msg

                if msg['data'] == "node_timestamp":
                    # save timestamp
                    self.time_sync = False
                    self.clock_node = msg ['timestamp']

                if self.time_sync: #if this is true send time_sync message
                    msg_send['data'] = "initiate_time_sync"
                    msg_send['timestamp'] =  time.time()*(10**6)+self.clock_change #PV note: this should be specific to the node
                    self.send_data(msg_send)
                    self.master_msg = msg_send
                    #assuming message delivered in one go

                if self.time_change: 
                    msg_send['data'] = "clock_change"
                    msg_send['time_change'] = self.clock_change
                    msg_send['timestamp'] =  time.time()*(10**6)+self.clock_change
                    self.send_data(msg_send)
                    self.master_msg = msg_send
                    self.time_change = False

            else:
                self.connection.connect()


#facilitating sensor data for other master
class MasterServicer(master_server_pb2_grpc.MasterServerServicer):

    def __init__(self):
        self.sensor_msgs = None #dictionary keyed by name of the sensor
        self.clock_change = 0.0

    def get_sensor_data(self, request, context):
        sensor_name = request.name
        data = self.sensor_msgs[sensor_name] #get the latest data from the sensor
        data_array = np.array(data)

        sensor_proto = master_server_pb2.SensorData() #instance of proto object

        sensor_proto.timestamp = time.time()*(10**6)+ self.clock_change
        sensor_proto.row_number = data_array.shape[1]
        sensor_proto.col_number = data_array.shape[0]

        data_flat = data_array.flatten().tolist()
        sensor_proto.sensor_data.extend(data_flat)
        return sensor_proto

    def execute_sync_init (self, request, context):
        if request.sync_request: #sync_request message is true then return the current time stampe
            timestamp_sync = time.time()*(10**6)+ self.clock_change
            return master_server_pb2.Timestamp(timestamp=timestamp_sync)
        else:
            return master_server_pb2.Timestamp(timestamp=None)        

    def execute_sync (self, request, context):
        self.clock_change  = request.change
        #PV:  self.master_timesync_msg will be added to all timestamp values
        status = True
        return master_server_pb2.TimestampChangeStatus(status=status)
        


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
        self.proxy = master_server_pb2_grpc.MasterServerStub(channel) #setting up a client so we can use the sensor on other master

    def run(self):
        self.master_server.start()
        self.master_server.wait_for_termination()
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
        self.clock_change = None #local master's clock change
        
        if config['Time_head']['time_head']: #if master is time head that updates the time periodically
            self.clock_change = None #the value by which clock changes on all actuator and sensor node
            self.clock_time_diff = {} #difference between timestampl for each node, should be an array
            self.clock_node = {} #extracted timestamp of the node
            self.clock_sync_start_time = time.time()*(10**6) #current timer flag for counting
            self.clock_sync_update = int(config['Time_head']['count']) #time within which the clock synchronizes 
            self.time_head=True #says that this master is time head
            self.sync_time = None  #sync time bool flag: syncing or not syncing 

#think about how this class behaves in time head or other mode

        for connection_type, connection_config in config.items():
            if 'Udp' in connection_type:
                name = connection_config['name']
                self.sensor_threads[name] = MasterToSensor(connection_config)
                self.sensor_threads[name].daemon = True
            if 'Rpc' in connection_type:
                name = connection_config['name']
                if 'master' in name:
                    self.other_master_present = True
                    self.other_master_threads[name] = MasterToMaster(connection_config)
                    self.other_master_threads[name].daemon = True
                else:
                    self.actuator_clients[name] = ActuatorClient(connection_config)
                    self.actuator_clients[name].daemon = True


    def read_model(self, path):
        self.model = pickle.load(path) # placeholder
        
        for name, master in self.other_master_threads.items(): #PV: does every master use the same model?
            master.model = self.model

    def compute_response(self, sensor_msgs, other_sensor_msgs=None):
        data = {}
        timestamps = {}
        for name, sensor_msg in sensor_msgs.items():
            data[name] = sensor_msg['data']
            timestamps[name] = sensor_msg['timestamp']
        responses = [1, 1, 1, 1] #PV: todo: reference the model here
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
                print(name, sensors.sensor_msg)

            if self.other_master_present:
                for other_master_name, master in self.other_master_threads.items(): #iterate through master connections
                    master.master_servicer.sensor_msgs = sensor_msgs #update master servicer with latest sensor message

                    for sensor_name, sensor in self.sensor_threads.items(): #iterating through no of sensors; assuming same type of sensors
                        sensor_of_interest = other_master_name + '_' + sensor_name
                        sensor_name_msg = master_server_pb2.SensorName(name=sensor_name)
                        sensor_of_interest_proto = master.proxy.get_sensor_data(sensor_name_msg) #PV: similar for sync calls 
                        other_sensor_msgs[sensor_of_interest] = self.parse_sensor_protobuf(sensor_of_interest_proto) #building a dictionary of other sensor messages
            # responses = self.compute_response(sensor_msgs, other_sensor_msgs)
            responses = [1, 1, 1, 1]

            for name, actuator in self.actuator_clients.items():
                response = responses[name]
                timestamp = time.time()*(10**6) + self.clock_change
                actuator.perform_command(timestamp, response)

            #---------------------TIME SYNC ------------------------

            if self.time_head: #if master is time head that updates the time periodically

                if (time.time()*(10**6)-self.clock_sync_start_time) < self.clock_sync_update:
                     total_active_nodes = len(self.actuator_clients)+len(self.sensor_threads)+len(self.other_master_threads)
                     sync_request = True

                #-------------initiate sync process: ask everyone to send their clock-----------
                     for name, actuator in self.actuator_clients.items():
                          self.clock_node[name] = actuator.perform_sync_init(time.time()*(10**6) + self.clock_change,sync_request) #we get node timestamp 
                          self.clock_time_diff[name] =  time.time()*(10**6) - self.clock_node[name]
                     
                     for name, sensors in self.sensor_threads.items():  
                         sensors.time_sync = True #this initiate the send loop in MastertoSensor thread
                         self.clock_node[name] = sensors.clock_node #assuming 
                         self.clock_time_diff[name] =  time.time()*(10**6) - self.clock_node[name]
                
                     for other_master_name, master in self.other_master_threads.items():
                         self.clock_node[name] = master.perform_sync_init(time.time()*(10**6) + self.clock_change,sync_request)
                         self.clock_time_diff[name] =  time.time()*(10**6) - self.clock_node[name]
                  
                    #--------calculate delta------------
                     if len(self.clock_time_diff) == total_active_nodes and total_active_nodes != 0:
                         clock_diff_values = [item for _, item in self.clock_time_diff.items() if item != 0]
                         self.clock_change = sum(clock_diff_values) / len(clock_diff_values)

                   #--------sending clock change value on each node-------
                     for name, actuator in self.actuator_clients.items():
                         self.clock_update[name] = actuator.perform_sync(time.time()*(10**6) + self.clock_change, self.clock_change ) #we update node timestamp 
                    
                     for name, sensors in self.sensor_threads.items():  
                         sensors.clock_change = self.clock_change
                         sensors.time_change =  True
                    
                     for other_master_name, master in self.other_master_threads.items():
                         self.clock_update[name] = master.perform_sync(time.time()*(10**6) + self.clock_change, self.clock_change )
                    
                else:
                    self.clock_sync_start_time = time.time()*(10**6)
