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

def main():
    args = parse_args()
    
    client_name = get_client_name(args)
    ip_address = get_ip_address(args)
    comment = args.comment if args.comment else ''

    private_key, public_key = create_keys(client_name)
    
    append_client_to_configuration(client_name, ip_address, private_key, public_key, comment)

    qr_main(WORK_DIR + client_name + CONF)

if __name__ == "__main__":
    main()