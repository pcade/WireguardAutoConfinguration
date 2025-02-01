from utils.utils import *
from modules.key_manager import *
from modules.ip_manager import *

CLIENT_NAME = 'test'


from modules.key_manager import *
private_key = create_private_keys(CLIENT_NAME).decode().strip()
public_key = create_pub_keys(private_key, CLIENT_NAME).decode().strip()


from modules.ip_manager import *
ip_address = increment_ip(get_last_allowed_ip(WG0+CONF))



from modules.config_manager import *
append_client_to_conf(CLIENT_NAME, 'x', ip_address, private_key)
append_client_to_conf(WG0, 'a', ip_address, public_key)

from modules.qr_generator import qr_main
qr_main(WORK_DIR+CLIENT_NAME+CONF)

import modules.daemon_reload
modules.daemon_reload.main
#IP_ADDRESS = IncrementIp(GetLastAllowedIp('wg0.conf'))

#AppendClientToConf(WG0, 'a')


#def main():
#    pass
#
#if __name__ == "__main__":
#    main()