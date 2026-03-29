from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()


class Config:
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
    # comment:
    PublicKey =
    AllowedIPs =
    '''

    FORM_CLI_CONF = f'''[Interface]
    Address = 
    DNS = {DNS}
    PrivateKey = 

    [Peer]
    PublicKey = {PUBLICKEY}
    AllowedIPs = {ALLOWEDIPS}
    Endpoint = {ENDPOINT}
    PersistentKeepalive = {PERSISTENTKEEPALIVE}\n
    '''

    RETURN = {'conf': '',
              'qr' : ''}

    PUBLICKEY = os.getenv('PUBLICKEY')
    ENDPOINT = os.getenv('ENDPOINT')
    DNS = os.getenv('DNS')
    ALLOWEDIPS = os.getenv('ALLOWEDIPS')
    PERSISTENTKEEPALIVE = os.getenv('PERSISTENTKEEPALIVE')

    @property
    def publickey(self) -> str:
        if self.PUBLICKEY is None:
            raise AttributeError("Переменная окружения PUBLICKEY не задана")
        return self.PUBLICKEY

    @property
    def endpoint(self) -> str:
        if self.ENDPOINT is None:
            raise AttributeError("Переменная окружения ENDPOINT не задана")
        return self.ENDPOINT

    @property
    def dns(self) -> str:
        if self.DNS is None:
            raise AttributeError("Переменная окружения DNS не задана")
        return self.DNS

    @property
    def allowedips(self) -> str:
        if self.ALLOWEDIPS is None:
            raise AttributeError("Переменная окружения ALLOWEDIPS не задана")
        return self.ALLOWEDIPS

    @property
    def pesistentkeepalive(self) -> str:
        if self.PERSISTENTKEEPALIVE is None:
            raise AttributeError("Переменная окружения PERSISTENTKEEPALIVE не задана")
        return self.PERSISTENTKEEPALIVE
