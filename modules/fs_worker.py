from utils.utils import *
import os
import shutil

def dir_creator(path: str, name: str) -> bool:
    """
    Создаёт директорию по указанному пути с заданным именем.

    :path: Путь, где будет создана директория.
    :name имя_директории: Имя создаваемой директории.
    """
    full_path = os.path.join(path, name)
    try:
        os.makedirs(full_path, exist_ok=True)
        dir_checker(full_path)
    except Exception as e:
        print(f"Ошибка при создании директории: {full_path} {e}")
        return False

def file_checker(path: str) -> bool:
    """
    Проверяет наличие файла по указанному пути.

    :path путь_к_файлу: Полный путь к файлу.s
    :return: True, если файл существует, иначе False.
    """
    try:
        return os.path.isfile(path)
    except Exception as e:
        print(f"Ошибка при проверке пути к файлу: {e}")
        return False

def dir_checker(path: str) -> bool:
    """
    Проверяет наличие директории по указанному пути.

    :path путь_к_директории: Полный путь к директории.
    :return: True, если директория существует, иначе False.
    """
    try:
        return os.path.isdir(path)
    except Exception as e:
        print(f"Ошибка при проверке пути к дирректории: {e}")
        return False

def pre_start_checks() -> bool:
    """
    Проверяет доступность путей необходимых для работы
    сервиса.

    :path путь_к_директории: Полный путь к директории.
    :return: True, если директория существует, иначе False.
    """
    if not dir_checker(WORK_DIR):
        return False
    if not file_checker(f"{WORK_DIR}{WG0}{CONF}"):
        return False
    if not dir_checker(f"{WORK_DIR}{CONFIGS_DIR}"):
        dir_creator(WORK_DIR, CONFIGS_DIR)
    return True

def path_worker(name: str) -> bool:
    """
    Проверят наличие создаваемого пути и
    создаёт рабочую директорию.

    :name: имя создаваемой директориии
    :return: True, если директория существует, иначе False.
    """
    if dir_checker(WORK_DIR + name):
        print('Директория конфигурации с таким именем уже существует')
        return False
    if file_checker(f"{WORK_DIR}{name}/{name}{CONF}"):
        print('Конфигурация с таким именем уже существует')
        return False
    dir_creator(WORK_DIR + CONFIGS_DIR, name)
    return True

def dir_remover(name: str) -> bool:
    """
    Удаляет директорию по указанному пути вместе со всеми вложенными файлами и поддиректориями.

    :param name: Имя директории с конфигурациионым файлом, которую нужно удалить.
    :return: True, если удаление прошло успешно, иначе False.
    """
    try:
        shutil.rmtree(WORK_DIR+CONFIGS_DIR+name)
        print(f"Директория успешно удалена: {WORK_DIR+CONFIGS_DIR+name}")
        return True
    except Exception as e:
        print(f"Ошибка при удалении директории: {WORK_DIR+CONFIGS_DIR+name} {e}")
        return False