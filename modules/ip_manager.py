from utils.utils import *

def GetLastAllowedIp(file_path):
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

def IncrementIp(ip_address):
    octets = ip_address.split('.')
    last_octet = int(octets[-1]) + 1

    if last_octet >= 250:
        raise ValueError("Последний октет превышает допустимый диапазон (0-250)")
    octets[-1] = str(last_octet)
    new_ip_address = '.'.join(octets)