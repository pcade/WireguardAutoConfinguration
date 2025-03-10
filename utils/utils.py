# File for GLOBALS
from dotenv import load_dotenv
import os
from datetime import datetime

NAME = 'WireguardAutoConfinguration'
VERSION = '1'

# Загружаем переменные окружения из файла .env
load_dotenv()

TODAY = datetime.now().strftime("%d.%m.%Y")

WORK_DIR = '/etc/wireguard/'
#WORK_DIR = "/home/gpahomov/Nextcloud/scripts/git/"
APP_DIR = "WireguardAutoConfinguration/"
CONFIGS_DIR = "configs/"
END_PRIVATE_KEY = '_private.key'
END_PUBLIC_KEY = '_public.key'
SUDO_TEE = 'sudo tee'
ECHO = 'echo'
WG_GENKEY = 'wg genkey'
WG_PUBKEY = 'wg pubkey'
SERVER = 'server'
CONF = '.conf'

WG0 = 'wg0'

FORM_WG0_CONF = '''\n\n[Peer]
# name:
# date:
# commnet:
PublicKey =
AllowedIPs =
'''

PublicKey = os.getenv('PublicKey')
Endpoint = os.getenv('Endpoint')
Dns = os.getenv('DNS')
AllowedIPs = os.getenv('AllowedIPs')
PersistentKeepalive = os.getenv('PersistentKeepalive')

FORM_CLI_CONF = f'''[Interface]
Address = 
DNS = {Dns}
PrivateKey = 

[Peer]
PublicKey = {PublicKey}
AllowedIPs = {AllowedIPs}
Endpoint = {Endpoint}
PersistentKeepalive = {PersistentKeepalive}\n
'''

RETURN = {'conf': '',
          'qr' : ''}