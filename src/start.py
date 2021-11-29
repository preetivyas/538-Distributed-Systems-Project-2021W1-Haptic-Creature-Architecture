import configparser
import logging
import datetime
import os
import sys
import time

import master
import sensor
import actuator
import connection


def as_dict(config):
    the_dict = {}
    for section in config.sections():
        the_dict[section] = {}
        for key, val in config.items(section):
            the_dict[section][key] = val
    return the_dict

def read_config(file):
    config = configparser.ConfigParser()
    config.read(file)
    config_dict = as_dict(config)
    return config_dict

def main():
    # initialiate logger

    current_time = datetime.datetime.now()
    log_foldername = '..//logs//'+str(current_time.year)+'-'+str('%02d'%current_time.month)+'-'+str('%02d'%current_time.day)
    try:
        os.makedirs(log_foldername)
    except:
        pass
    log_filename = sys.argv[1]+'.log'
    logging.basicConfig(format='%(asctime)s %(filename)s[%(lineno)d] %(levelname)s %(message)s',
                        filename=log_foldername+'//'+log_filename,
                        filemode='a+',
                        level=logging.INFO)  # NOTSET

    logging.info("**********************"+sys.argv[1]+" initiated****************************")
    logging.basicConfig(datefmt='')
    logging.info('Initiated Time, '+str(time.time()*10**6))
    config_file = '../config/config_'+sys.argv[1]+'.ini' 
    config = read_config(config_file)
    if 'actuator' in sys.argv[1]:
        process = actuator.Actuator(config)
        process.start()
    elif 'sensor' in sys.argv[1]:
        process = sensor.Sensor(config)
        process.start()
    elif 'master' in sys.argv[1]:
        process = master.Master(config)
        process.start()
    else:
        print('Incorrect process')


if __name__ == '__main__':
    main()