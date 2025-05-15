import json
import os

CONFIG_FILE = "variables/config.json"

default_config = {
    "nb_dechets": 10,
    "largeur_plage": 100,
    "niveau_maree": 1,
    "vitesse_simulation": 1,
    "best_score": 0,
    "ip": "192.168.0.1",
    "port_usb": "COM3",
    "port_wifi": 8080,
    "robot_connect": False
}

def load_config():

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                return config
        except Exception as e:
            return default_config.copy()
    else:
        save_config(default_config)
        return default_config.copy()

def save_config(config):

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def modify_variable(variable, value):

    config = load_config()

    if variable in config:
        config[variable] = value
        save_config(config)

