import configparser
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
    actuator_config_file = '../config/config_actuator_1.ini' 
    actuator_config = read_config(actuator_config_file)
    actuator_process = actuator.Actuator(actuator_config)
    actuator_process.start()


if __name__ == '__main__':
    main()