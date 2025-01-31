from utils.utils import *

def create_config(form_conf, replacements):
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

def create_str_client_conf(ip_addr, private_key):
    replacements = {
        'Address =': f"{ip_addr}/24",
        'PrivateKey =': private_key
    }
    return create_config(FORM_CLI_CONF, replacements)

def create_str_wg_conf(ip_addr, public_key):
    replacements = {
        'PublicKey =': public_key,
        'AllowedIPs =': f"{ip_addr}/32"
    }
    return create_config(FORM_WG0_CONF, replacements)

def append_client_to_conf(name, type_write, ip_addr, key):
    # x - на создание, a - на добавление в конец
    try:
        with open(WORK_DIR+name+CONF, type_write) as config_file:
            if name == WG0: 
                config_file.write(create_str_wg_conf(ip_addr, key))
            else:
                config_file.write(create_str_client_conf(ip_addr, key))
        print(f"Файл конфигурации WireGuard создан по адресу {WORK_DIR+name+CONF}")
    except PermissionError:
        print("Ошибка доступа: Вам нужно запустить этот скрипт с правами sudo.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")