import configparser
import sensor
import sys
import connection

# arguments sensor_1, sensor_2 etc. each sensor needs to have a config file

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
    sensor_config_file = '../config/config_'+sys.argv[1]+'.ini' 
    # '+sys.argv[1]+'
    print(sensor_config_file)
    sensor_config = read_config(sensor_config_file)
    sensor_process = sensor.Sensor(sensor_config)
    sensor_process.start()


if __name__ == '__main__':
    main()