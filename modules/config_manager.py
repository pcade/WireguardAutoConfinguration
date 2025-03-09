from utils.utils import *
import re

def create_config(form_conf: str, replacements: dict) -> str:
    """
    Проходит по каждой строке конфигурации и заменяет
    указанные шаблоны на заданные значения.

    :param form_conf: Строка конфигурации (str);
    :param replacements: Словарь замен (dict);
    :return: Обновленная строка конфигурации (str).
    """
    lines = form_conf.splitlines()
    for i, line in enumerate(lines):
        for placeholder, value in replacements.items():
            if line.strip() == placeholder:
                lines[i] = f"{placeholder} {value}"
    # Объединяем строки обратно в одну строку
    return '\n'.join(lines)


def create_str_client_conf(ip_addr: str, private_key: str) -> str:
    """
    Создает строку конфигурации клиента.

    :param ip_addr: IP-адрес клиента (str);
    :param private_key: Приватный ключ клиента (str);
    :return: Строка конфигурации клиента (str).
    """
    replacements = {
        'Address =': f"{ip_addr}/24",
        'PrivateKey =': private_key
    }
    return create_config(FORM_CLI_CONF, replacements)


def create_str_wg_conf(ip_addr: str, public_key: str, name: str, date: str, comment: str) -> str:
    """
    Создает строку конфигурации WireGuard.

    :param ip_addr: IP-адрес клиента (str);
    :param public_key: Публичный ключ клиента (str);
    :param name: Имя клиента (str);
    :param date: Дата добавления клиента (str);
    :param comment: Комментарий к клиенту (str);
    :return: Строка конфигурации WireGuard (str).
    """
    replacements = {
        '# name:': name,
        '# date:': f"{TODAY} - {date}",
        '# commnet:': comment,
        'PublicKey =': public_key,
        'AllowedIPs =': f"{ip_addr}/32"
    }
    return create_config(FORM_WG0_CONF, replacements)


def append_client_to_configuration(ip_addr: str, public_key: str, name: str, date: str, comment: str) -> None:
    """
    Добавляет клиента в конфигурацию WireGuard.

    :param ip_addr: IP-адрес клиента (str);
    :param public_key: Публичный ключ клиента (str);
    :param name: Имя клиента (str);
    :param date: Дата добавления клиента (str);
    :param comment: Комментарий к клиенту (str);
    :return: None.
    """
    try:
        with open(WORK_DIR+WG0+CONF, 'a') as config_file:
            config_file.write(create_str_wg_conf(ip_addr, public_key, name, date, comment))
    except Exception as e:
        print(f"Произошла ошибка в append_client_to_conf: {e}")

def create_client_to_configuration(client_name: str, ip_address: str, private_key: str) -> None:
    """
    Добавляет клиента в конфигурацию.

    :param client_name: Имя клиента (str);
    :param ip_address: IP-адрес клиента (str);
    :param private_key: Приватный ключ клиента (str);
    :return: None.
    """
    try:
            with open(f"{WORK_DIR}{CONFIGS_DIR}/{client_name}/{client_name}{CONF}", 'x') as config_file:
                config_file.write(create_str_client_conf(ip_address, private_key))
    except Exception as e:
        print(f"Произошла ошибка в append_client_to_conf: {e}")

def extract_ip_addresses(config_file_path: str) -> list:
    """
    Извлекает все IP-адреса из указанного файла конфигурации без масок.

    :param config_file_path: Путь к файлу конфигурации (str);
    :return: Список IP-адресов (list).
    """
    ip_addresses = []
    try:
        with open(config_file_path, 'r') as config_file:
            for line in config_file:
                # Ищем строки, содержащие IP-адреса
                match = re.search(r'(?:(?:Address|AllowedIPs)\s*=\s*)([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)(?:/[0-9]+)?', line)
                if match:
                    ip_addresses.append(match.group(1))  # Добавляем только IP-адрес без маски
    except Exception as e:
        print(f"Произошла ошибка при извлечении IP-адресов: {e}")

    return ip_addresses
