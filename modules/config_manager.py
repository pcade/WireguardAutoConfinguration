from main import IP_ADDRESS, PRIVATE_KEY, PUBLIC_KEY
from utils.utils import *

def CreateConfig(form_conf, replacements):
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

def CreateClientConf():
    replacements = {
        'Address =': f"{IP_ADDRESS}/24",
        'PrivateKey =': PRIVATE_KEY
    }
    return CreateConfig(FORM_CLI_CONF, replacements)

def CreateStrWGconf():
    replacements = {
        'PublicKey =': PUBLIC_KEY,
        'AllowedIPs =': f"{IP_ADDRESS}/32"
    }
    return CreateConfig(FORM_WG0_CONF, replacements)

def AppendClientToConf(name, type_write):
    # x - на создание, a - на добавление в конец
    try:
        with open(WORK_DIR+name+CONF, type_write) as config_file:
            if name == WG0: 
                config_file.write(CreateStrWGconf())
            else:
                config_file.write(CreateClientConf())
        print(f"WireGuard configuration file created at {WORK_DIR+name+CONF}")
    except PermissionError:
        print("Permission denied: You need to run this script with sudo.")
    except Exception as e:
        print(f"An error occurred: {e}")