import configparser
import master
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
    master_config_file = '../config/config_master.ini'
    master_config = read_config(master_config_file)
    master_process = master.Master(master_config)
    master_process.start()






if __name__ == '__main__':
    main()