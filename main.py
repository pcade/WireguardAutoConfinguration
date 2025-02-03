from utils.utils import *
from modules.key_manager import *
from modules.ip_manager import *
from modules.key_manager import *
from modules.ip_manager import *
from modules.config_manager import *
from modules.qr_generator import qr_main
import modules.daemon_reload
from modules.argparser import parse_args



def main():
    args = parse_args()
    if args.name != None:
        CLIENT_NAME = args.name
    else:
        CLIENT_NAME = 'test'
    private_key = create_private_keys(CLIENT_NAME).decode().strip()
    public_key = create_pub_keys(private_key, CLIENT_NAME).decode().strip()
    ip_address = increment_ip(get_last_allowed_ip(WG0+CONF))
    append_client_to_conf(CLIENT_NAME, 'x', ip_address, private_key)
    append_client_to_conf(WG0, 'a', ip_address, public_key)
    qr_main(WORK_DIR+CLIENT_NAME+CONF)
#    modules.daemon_reload.main

if __name__ == "__main__":
    main()
#print(f"ip: {args.ip}, comment: {args.comment}, clinet: {CLIENT_NAME}")