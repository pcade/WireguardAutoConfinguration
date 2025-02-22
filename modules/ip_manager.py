from utils.utils import *
import ipaddress
import sys


def get_last_allowed_ip(file_path):
    '''Извлекает последний доступный
    ip из файла конфигурации
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


def increment_ip(ip_address):
    '''Извлекает последний актет
    '''
    octets = ip_address.split('.')
    last_octet = int(octets[-1]) + 1

    if last_octet >= 250:
        raise ValueError("Последний октет превышает допустимый диапазон (0-250)")
    octets[-1] = str(last_octet)
    return '.'.join(octets)


def validate_ip(ip):
    '''Проверяет, является ли строка корректным IP-адресом.
    '''
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        print(f"Некорректный IP-адрес: {ip}")
        return False

def get_ip_address(args):
    """Получить IP-адрес из аргументов или сгенерировать новый."""
    if args.ip:
        if not validate_ip(args.ip):
            sys.exit(1)
        return args.ip
    return increment_ip(get_last_allowed_ip(f"{WORK_DIR}{WG0}{CONF}"))