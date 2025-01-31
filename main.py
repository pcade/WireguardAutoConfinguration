import subprocess
from utils.utils import *
from modules.key_manager import *
#from modules.config_manager import *
#from modules.ip_manager import *

CLIENT_NAME = 'test'

PRIVATE_KEY = create_private_keys(CLIENT_NAME).decode().strip()
PUBLIC_KEY = create_pub_keys(PRIVATE_KEY, CLIENT_NAME).decode().strip()
from modules.config_manager import *
#IP_ADDRESS = IncrementIp(GetLastAllowedIp('wg0.conf'))

#AppendClientToConf(WG0, 'a')


if __name__ == "__main__":
    main()