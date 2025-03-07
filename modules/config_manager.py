from utils.utils import *
import re

def create_config(form_conf: str, replacements: dict) -> str:
    '''
    Проходим по каждой строке
    Заменяем указанные шаблоны на заданные значения
    '''
    lines = form_conf.splitlines()
    for i, line in enumerate(lines):
        for placeholder, value in replacements.items():
            if line.strip() == placeholder:
                lines[i] = f"{placeholder} {value}"
    # Объединяем строки обратно в одну строку
    return '\n'.join(lines)


def create_str_client_conf(ip_addr: str, private_key: str) -> str:
    replacements = {
        'Address =': f"{ip_addr}/24",
        'PrivateKey =': private_key
    }
    return create_config(FORM_CLI_CONF, replacements)


def create_str_wg_conf(ip_addr: str, public_key: str, comment: str) -> str:
    replacements = {
        '#': comment,
        'PublicKey =': public_key,
        'AllowedIPs =': f"{ip_addr}/32"
    }
    return create_config(FORM_WG0_CONF, replacements)


def append_client_to_conf(name: str, type_write: str, ip_addr: str, key: str, comment: str):
    # x - на создание, a - на добавление в конец
    try:
        if name == WG0:
            with open(WORK_DIR+name+CONF, type_write) as config_file:
                config_file.write(create_str_wg_conf(ip_addr, key, comment))
        else:
            with open(f"{WORK_DIR}{CONFIGS_DIR}/{name}/{name}{CONF}", type_write) as config_file:
                config_file.write(create_str_client_conf(ip_addr, key))
    except Exception as e:
        print(f"Произошла ошибка в append_client_to_conf: {e}")

def append_client_to_configuration(client_name, ip_address, private_key, public_key, comment):
    """Добавить клиента в конфигурацию."""
    append_client_to_conf(client_name, 'x', ip_address, private_key, comment='')
    append_client_to_conf(WG0, 'a', ip_address, public_key, comment)

def extract_ip_addresses(config_file_path: str) -> list:
    """
    Извлекает все IP-адреса из указанного файла конфигурации без масок.

    :param config_file_path: Путь к файлу конфигурации (str).
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
