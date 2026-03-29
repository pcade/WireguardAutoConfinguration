import argparse
from config.config import Config


class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description=f"{Config.NAME} - {Config.VERSION}"
        )
        self._setup_arguments()

    def _setup_arguments(self) -> None:
        self.parser.add_argument(
            '--name',
            type=str,
            help='Параметр передачи имени клиентской конфигурации'
        )

        self.parser.add_argument(
            '--ip',
            type=str,
            help='Параметр передачи IP-адреса клиентской конфигурации'
        )

        self.parser.add_argument(
            '--date',
            type=str,
            help='Параметр передачи даты в формате "Д/М/Г"'
        )

        self.parser.add_argument(
            '--comment',
            type=str,
            help='Параметр передачи комментария к создаваемой конфигурации'
        )

        self.parser.add_argument(
            '--remove',
            type=str,
            help='Параметр удаления конфигурации'
        )

        self.parser.add_argument(
            '--removeconfig',
            type=str,
            help='Параметр удаления файлов конфигурации'
        )

        self.parser.add_argument(
            '--config',
            action='store_true',
            help='Параметр отображения текущих ip адресов в конфигурационном файле'
        )

        self.parser.add_argument(
            '--daemonreload',
            action='store_true',
            help='Параметр перезагрузки сервисов'
        )

        self.parser.add_argument(
            '--version',
            action='version',
            version=Config.VERSION,
            help='Вывод версии пакета'
        )

        self.parser.add_argument(
            '--json',
            action='store_true',
            help='Вывод словаря с путями к конфигурационному файлу и qr коду'
        )

    def parse(self) -> argparse.Namespace:
        return self.parser.parse_args()
