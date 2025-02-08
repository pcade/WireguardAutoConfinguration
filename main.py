from utils.utils import *
from modules.key_manager import *
from modules.ip_manager import *
from modules.key_manager import *
from modules.ip_manager import *
from modules.config_manager import *
from modules.qr_generator import qr_main
import modules.daemon_reload
from modules.argparser import parse_args
from modules.str_checker import *
import sys


def get_client_name(args):
    """Получить имя клиента из аргументов или использовать значение по умолчанию."""
    if args.name:
        if not is_ascii(args.name):
            sys.exit(1)
        return args.name
    return 'test'

def get_ip_address(args):
    """Получить IP-адрес из аргументов или сгенерировать новый."""
    if args.ip:
        if not validate_ip(args.ip):
            sys.exit(1)
        return args.ip
    return increment_ip(get_last_allowed_ip(WG0 + CONF))

def create_keys(client_name):
    """Создать закрытый и открытый ключи для клиента."""
    private_key = create_private_keys(client_name).decode().strip()
    public_key = create_pub_keys(private_key, client_name).decode().strip()
    return private_key, public_key

def append_client_to_configuration(client_name, ip_address, private_key, public_key):
    """Добавить клиента в конфигурацию."""
    append_client_to_conf(client_name, 'x', ip_address, private_key)
    append_client_to_conf(WG0, 'a', ip_address, public_key)

def main():
    args = parse_args()
    
    client_name = get_client_name(args)
    ip_address = get_ip_address(args)
    comment = args.comment if args.comment else ''
    
    private_key, public_key = create_keys(client_name)
    
    append_client_to_configuration(client_name, ip_address, private_key, public_key)
    
    qr_main(WORK_DIR + client_name + CONF)

#def main():
#    client_name = 'test'
#    comment = ''
#    ip_address = increment_ip(get_last_allowed_ip(WG0+CONF))
#    args = parse_args()
#    if args.name != None:
#        if not is_ascii(args.name):
#            sys.exit(1)
#        client_name = args.name
#    if args.comment != None:
#        comment = args.comment
#    if args.ip != None:
#        if not validate_ip(args.ip):
#            sys.exit(1)
#        ip_address = args.ip
#    private_key = create_private_keys(client_name).decode().strip()
#    public_key = create_pub_keys(private_key, client_name).decode().strip()
#    append_client_to_conf(client_name, 'x', ip_address, private_key)
#    append_client_to_conf(WG0, 'a', ip_address, public_key)
#    qr_main(WORK_DIR+client_name+CONF)
#    modules.daemon_reload.main

if __name__ == "__main__":
    main()
#print(f"ip: {args.ip}, comment: {args.comment}, clinet: {client_name}")