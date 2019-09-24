import logging


def get_config():
    config = {}
    try:
        with open("/etc/httpd.conf", "r") as fs:
            for line in fs.readlines():
                k, v = line.split()
                config[k] = v
    except Exception as e:
        logging.error("ERROR " + str(e))
    return config


CONFIG = get_config()
