from utils.utils import *
import ipaddress
import sys


def get_last_allowed_ip(file_path) -> str:
    '''
    Извлекает последний доступный
    ip из файла конфигурации

    :file_path: str
    :return: str
    '''
    last_allowed_ip = None
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.startswith("AllowedIPs"):
                    # Извлекаем IP-адрес из строки
                    last_allowed_ip = line.split('=')[1].split('/')[0].strip()
    except Exception as error:
        print(f"Оишбка в GetLastAllowedIp(file_path): {error}")
    return last_allowed_ip


def increment_ip(ip_address) -> str:
    '''
    Извлекает последний актет
    и возвращает ip

    :ip_address: str
    :return: str
    '''
    octets = ip_address.split('.')
    last_octet = int(octets[-1]) + 1

    if last_octet >= 250:
        raise ValueError("Последний октет превышает допустимый диапазон (0-250)")
    octets[-1] = str(last_octet)
    return '.'.join(octets)


def validate_ip(ip) -> bool:
    '''
    Проверяет, является ли строка корректным IP-адресом.

    :ip: str
    :return: bool
    '''
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        print(f"Некорректный IP-адрес: {ip}")
        return False

def get_ip_address(args) -> str:
    '''
    Получить IP-адрес из аргументов или сгенерировать новый.

    :args: str
    :return: str
    '''
    if args.ip:
        if not validate_ip(args.ip):
            sys.exit(1)
        return args.ip
    return increment_ip(get_last_allowed_ip(f"{WORK_DIR}{WG0}{CONF}"))