from utils.utils import *
import re
import json

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

def remove_configuration_by_ip(ip_address: str) -> None:
    """
    Удаляет конфигурацию по указанному IP-адресу из файла конфигурации.

    :param ip_address: IP-адрес, конфигурацию которого нужно удалить (str);
    :return: None.
    """
    try:
        config_text = read_configuration_file(WORK_DIR + WG0 + CONF)
        updated_config_text = remove_ip_configuration(config_text, ip_address)
        write_configuration_file(WORK_DIR + WG0 + CONF, updated_config_text)
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def read_configuration_file(path: str) -> str:
    """
    Читает файл конфигурации и возвращает его содержимое.

    :path: содержит путь к файлу (str):
    :return: Содержимое файла конфигурации (str).
    """
    with open(path, 'r') as config_file:
        return config_file.read()


def write_configuration_file(path: str, config_text: str) -> None:
    """
    Записывает обновленное содержимое в файл конфигурации.

    :path: содержит путь к файлу (str):
    :param config_text: Содержимое для записи в файл (str).
    :return: None.
    """
    with open(path, 'w') as config_file:
        config_file.write(config_text)


def remove_ip_configuration(config_text: str, ip_address: str) -> str:
    """
    Удаляет конфигурацию для указанного IP-адреса из текста конфигурации.

    :param config_text: Содержимое файла конфигурации (str);
    :param ip_address: IP-адрес, конфигурацию которого нужно удалить (str);
    :return: Обновленное содержимое файла конфигурации (str).
    """
    search_string = f'AllowedIPs = {ip_address}/32'
    start_index = config_text.find(search_string)

    if start_index == -1:
        return config_text  # Если строка не найдена, возвращаем оригинальный текст

    peer_index = config_text.rfind('[Peer]', 0, start_index)

    if peer_index == -1:
        # Если [Peer] не найден, удаляем от найденной строки до конца текста
        return config_text[:start_index]
    else:
        # Удаляем текст от [Peer] до конца строки с AllowedIPs
        return config_text[:peer_index]

import re
import json

def extract_from_config(config_file_path: str) -> str:
    """
    Извлекает все строки из указанного файла конфигурации, которые не содержат ключи,
    и возвращает их в формате JSON с группировкой по значению AllowedIPs.
    Гарантирует, что каждая группа начинается с [Peer].

    :param config_file_path: Путь к файлу конфигурации (str);
    :return: JSON-строка, содержащая строки, сгруппированные по значению AllowedIPs (str).
    """
    result = {}
    current_group = None
    allowed_ips = None

    try:
        with open(config_file_path, 'r') as config_file:
            for line in config_file:
                line = line.strip()

                # Пропускаем пустые строки
                if not line:
                    continue

                # Если находим начало нового блока [Peer]
                if line.startswith("[Peer]"):
                    if current_group and allowed_ips:
                        result[allowed_ips] = current_group
                    current_group = [line]  # Начинаем новую группу с [Peer]
                    allowed_ips = None  # Сбрасываем значение AllowedIPs для новой группы

                # Если находим строку с AllowedIPs, сохраняем её значение
                elif line.startswith("AllowedIPs"):
                    allowed_ips = line.split("=")[1].strip()

                # Добавляем строку в текущую группу, если она не содержит ключей
                elif current_group is not None and not re.search(r'(Address|PrivateKey|PublicKey|ListenPort)\s*=', line):
                    current_group.append(line)

            # Добавляем последнюю группу в результат, если она существует
            if current_group and allowed_ips:
                result[allowed_ips] = current_group

    except Exception as e:
        print(f"Произошла ошибка при извлечении строк: {e}")

    # Преобразуем словарь в JSON-строку
    return json.dumps(result, ensure_ascii=False, indent=4)