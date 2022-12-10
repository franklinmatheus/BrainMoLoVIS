from os.path import exists
from os import getcwd
import json

default_config = {
    'export_path':getcwd(),
    'logger_file': {
        'filename': {
            'subject':0,
            'session':1,
            'date':2,
            'time':3
        },
        'sep':';',
        'content': {
            'raweeg':0,
            'esenseat':1,
            'esensemed':2,
            'delta':3,
            'theta':4,
            'lowalpha':5,
            'highalpha':6,
            'lowbeta':7,
            'highbeta':8,
            'lowgamma':9,
            'highgamma':10,
            'genat':11,
            'genmed':12
        },
    },
    'monitor': {
        'average': 0,
        'esenseat': 1,
        'esensemed': 1,
        'genat': 'Theta/High Beta',
        'genmed': 'High Alpha',
        'range': 30
    }
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

def get_logger_file_content() -> tuple[dict, str]:
    temp = load_config()
    return temp['logger_file']['content'], temp['logger_file']['sep']

def set_logger_file_content(format: dict, sep: str) -> None:
    temp = load_config()
    temp['logger_file']['content'] = format
    temp['logger_file']['sep'] = sep
    save_config(temp)

def get_logger_file_content_reduced() -> tuple[list, dict, str]:
    temp = load_config()
    seq = [value[0] for value in sorted(dict(temp['logger_file']['content']).items(), key=lambda item: item[1]) if value[1] != -1]
    reduced = {key: value for key, value in dict(temp['logger_file']['content']).items() if key in seq}
    return seq, reduced, temp['logger_file']['sep']

def get_logger_file_sep() -> str:
    temp = load_config()
    return temp['logger_file']['sep']

def get_show_average() -> int:
    temp = load_config()
    return temp['monitor']['average']

def set_show_average(show_average: int) -> None:
    temp = load_config()
    temp['monitor']['average'] = show_average
    save_config(temp)

def get_show_esenseat() -> int:
    temp = load_config()
    return temp['monitor']['esenseat']

def set_show_esenseat(show_esenseat: int) -> None:
    temp = load_config()
    temp['monitor']['esenseat'] = show_esenseat
    save_config(temp)

def get_show_esensemed() -> int:
    temp = load_config()
    return temp['monitor']['esensemed']

def set_show_esensemed(show_esensemed: int) -> None:
    temp = load_config()
    temp['monitor']['esensemed'] = show_esensemed
    save_config(temp)

def get_opt_genat() -> str:
    temp = load_config()
    return temp['monitor']['genat']

def set_opt_genat(opt_genat: str) -> None:
    temp = load_config()
    temp['monitor']['genat'] = opt_genat
    save_config(temp)

def get_opt_genmed() -> str:
    temp = load_config()
    return temp['monitor']['genmed']

def set_opt_genmed(opt_genmed: str) -> None:
    temp = load_config()
    temp['monitor']['genmed'] = opt_genmed
    save_config(temp)

def get_xaxis_range() -> int:
    temp = load_config()
    return temp['monitor']['range']

def set_xaxis_range(xaxis_range: int) -> None:
    temp = load_config()
    temp['monitor']['range'] = xaxis_range
    save_config(temp)

def is_session_required() -> bool:
    temp = load_config()
    return temp['logger_file']['filename']['session'] != -1