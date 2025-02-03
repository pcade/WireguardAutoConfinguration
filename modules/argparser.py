import argparse
from utils.utils import *


def parse_args() -> argparse.Namespace:
    """Парсер аргументов командной строки.
    """
    parser = argparse.ArgumentParser(description=f"{NAME} - {VERSION}")

    parser.add_argument(
        '--name',
        type=str,
        help='Параметр передачи имени клиентской конфигурации'
    )

    parser.add_argument(
        '--ip',
        type=str,
        help='Параметр передачи IP-адреса клиентской конфигурации'
    )

    parser.add_argument(
        '--comment',
        type=str,
        help='Параметр передачи комментария к создаваемой конфигурации'
    )

    parser.add_argument(
        '--version',
        action='version',
        version=VERSION,
        help='Вывод версии пакета'
    )
    return parser.parse_args()