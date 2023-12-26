''' модуль для django, предназначенный для удаления файлов миграций'''
import os
from typing import Optional
from manage import *

try:
    from config.settings import BASE_DIR
except ImportError:
    print("Can't find path to BASE DIR.")

INPUT_PHRASE = 'Please, input the name of your apps folder or leave it empty'


def concatenate_paths(path: str) -> Optional[str]:
    ''' Handles the BASE_DIR and additional path concatenation or asks for a BASE_DIR path '''
    try:
         return os.path.join(BASE_DIR, path)
    except NameError:
        try:
            return os.path.join(input('enter path to "config.settings"'), path)
        except ValueError:
            print(ValueError('unacceptable value for "config.settings" path'))
            return None


def clear_all_migrations(additional_path: str = '') -> None:
    ''' Чистит все папки миграций от файлов миграций, кроме инициализатора и кэша.
        Если приложения держатся в отдельной папке, принимает аргумент дополнительной папки '''
    base_dir = concatenate_paths(additional_path)
    if base_dir is None:
        return clear_all_migrations(INPUT_PHRASE)

    exceptions = ("__init__.py", "__pycache__")
    for item in os.listdir(base_dir):
        path = os.path.join(base_dir, item)
        if os.path.isdir(path):
            if str(item) == 'migrations':
                for file in os.listdir(path):
                    if str(file) not in exceptions:
                        os.remove(os.path.join(path, file))
                        print('INFO: removed ' + "\\".join(path.split("\\")[-2:]) + '\\' + file)
            else:
                clear_all_migrations(path)
    return


if __name__ == '__main__':
    clear_all_migrations(input(INPUT_PHRASE))
    print('SUCCESS: УСПЕШНО ЗАВЕРШЕНО')

