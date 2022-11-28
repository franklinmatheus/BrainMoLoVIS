from os.path import exists
from os import getcwd
import json

default_config = {
    'export_path':getcwd(),
    'logger_file': {
        'filename': {
            'subject':0,
            'date':1,
            'time':2
        },
        'sep':';',
        'content': {
            'rawEeg':0,
            'eSenseAT':1,
            'eSenseMED':2,
            'delta':3,
            'theta':4,
            'lowAlpha':5,
            'highAlpha':6,
            'lowBeta':7,
            'highBeta':8,
            'lowGamma':9,
            'highGamma':10,
        },
    },
}

def create_default_config() -> None:
    with open('./config.json', 'w') as file:
        file.write(json.dumps(default_config, indent=4))

def save_config(new_config: dict) -> None:
    with open('./config.json', 'w') as file:
        file.write(json.dumps(new_config, indent=4))

def load_config() -> dict:
    if exists('./config.json'):
        with open('./config.json', 'r') as file:
            data = file.read()
            if data == '':
                create_default_config()
            else:
                json_data = ''
                with open('./config.json', 'r') as file:
                    try: json_data = json.loads(file.read())
                    except Exception:
                        json_data = default_config
                        create_default_config()
                return json_data
    else:
        create_default_config()
        return default_config

def get_export_path() -> str:
    return load_config()['export_path']

def set_export_path(path: str) -> None:
    temp = load_config()
    temp['export_path'] = path
    save_config(temp)

def get_logger_filename() -> dict:
    return load_config()['logger_file']['filename']

def set_logger_filename(format: dict) -> None:
    temp = load_config()
    temp['logger_file']['filename'] = format
    save_config(temp)