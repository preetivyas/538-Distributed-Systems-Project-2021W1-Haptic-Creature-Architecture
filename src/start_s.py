import configparser
import sensor
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
    sensor_config_file = '../config/config_sensor_1.ini' 
    sensor_config = read_config(sensor_config_file)
    sensor_process = sensor.Sensor(sensor_config)
    sensor_process.start()


if __name__ == '__main__':
    main()