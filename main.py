import sys
import json
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
from modules.daemon_reload import reload_daemon
import modules.fs_worker

def main():
    if modules.fs_worker.pre_start_checks() == False:
        sys.exit(1)
    args = parse_args()

    if args.remove:
        remove_configuration_by_ip(args.remove)
        return sys.exit(0)

    if args.daemonreload:
        reload_daemon()
        return sys.exit(0)

    if args.removeconfig:
        modules.fs_worker.dir_remover(args.removeconfig)
        return sys.exit(0)

    if args.config:
        ip_list: list = extract_ip_addresses(f'{WORK_DIR}{WG0}{CONF}')
        return sys.stdout.write(json.dumps(ip_list))

    client_name = args.name if args.name else f"auto_{increment_ip(get_last_allowed_ip(f'{WORK_DIR}{WG0}{CONF}')).split('.')[-1]}"

    modules.fs_worker.path_worker(client_name)

    ip_address = get_ip_address(args)

    comment = args.comment if args.comment else ''
    date = args.date if args.date else ''

    private_key, public_key = create_keys(client_name)

    create_client_to_configuration(client_name, ip_address, private_key)
    append_client_to_configuration(ip_address, public_key, client_name, date, comment)

    path_conf = WORK_DIR + CONFIGS_DIR + client_name + '/' + client_name + CONF
    path_qr = WORK_DIR + CONFIGS_DIR + client_name + '/' + client_name + '.png'

    qr_main(path_conf, path_qr)

    if args.json:
        RETURN['conf'] = path_conf
        RETURN['qr'] = path_qr
        sys.stdout.write(json.dumps(RETURN))

if __name__ == "__main__":
    main()