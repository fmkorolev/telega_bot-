import json
from typing import Dict
def _decode(o):
    '''
    Превращение числовых данных в json в int при считывании из файла
    '''
    if isinstance(o, str):
        try:
            return int(o)
        except ValueError:
            return o
    elif isinstance(o, dict):
        return {k: _decode(v) for k, v in o.items()}
    elif isinstance(o, list):
        return [_decode(v) for v in o]
    else:
        return o

def database_read():
    '''
    Чтение базы данных
    '''
    
    with open("data.json", "r", encoding='utf-8') as read_file:
        data = read_file.read()
        if not data:
            return {}
        del data
        data_from_file = json.load(read_file, object_hook=_decode)
    return data_from_file

def write_to_database(task:Dict):
    database = database_read()
    id = len(database)+1
    database.update({id:task})
    with open("data.json", "w", encoding='utf-8') as write_file:
        json.dump(database, write_file,#запись в файл
                ensure_ascii=False,#можно не ASCII-символы - для русского языка
                indent = 4)
        
def add_to_temp_file(string:str):
    with open('temp.txt', 'a', encoding='utf-8') as file:
        file.write(f'{string}\n')

def clear_temp_file():
    with open('temp.txt', 'w', encoding='utf-8') as file:
        file.write('')

database_read()