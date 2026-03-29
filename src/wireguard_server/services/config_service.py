import json
import os
import re
import subprocess
from datetime import datetime


class ConfigService:
    def __init__(
        self,
        work_dir: str,
        configs_dir: str,
        wg0: str,
        conf_ext: str,
        form_cli_conf: str,
        form_wg0_conf: str,
    ):
        self.work_dir = work_dir
        self.configs_dir = configs_dir
        self.wg0 = wg0
        self.conf_ext = conf_ext
        self.form_cli_conf = form_cli_conf
        self.form_wg0_conf = form_wg0_conf

    @property
    def wg_conf_path(self) -> str:
        return os.path.join(self.work_dir, f"{self.wg0}{self.conf_ext}")

    def create_config(self, form_conf: str, replacements: dict[str, str]) -> str:
        """
        Проходит по каждой строке конфигурации и заменяет указанные шаблоны.
        """
        lines = form_conf.splitlines()
        for i, line in enumerate(lines):
            for placeholder, value in replacements.items():
                if line.strip() == placeholder:
                    lines[i] = f"{placeholder} {value}"
        return "\n".join(lines)

    def create_str_client_conf(self, ip_addr: str, private_key: str) -> str:
        """
        Создаёт строку конфигурации клиента.
        """
        replacements = {
            "Address =": f"{ip_addr}/24",
            "PrivateKey =": private_key,
        }
        return self.create_config(self.form_cli_conf, replacements)

    def create_str_wg_conf(
        self,
        ip_addr: str,
        public_key: str,
        name: str,
        date: str,
        comment: str,
    ) -> str:
        """
        Создаёт строку конфигурации WireGuard.
        """
        today = datetime.now().strftime("%d.%m.%Y")
        replacements = {
            "# name:": name,
            "# date:": f"{today} - {date}",
            "# comment:": comment,
            "PublicKey =": public_key,
            "AllowedIPs =": f"{ip_addr}/32",
        }
        return self.create_config(self.form_wg0_conf, replacements)

    def append_client_to_configuration(
        self,
        ip_addr: str,
        public_key: str,
        name: str,
        date: str,
        comment: str,
    ) -> None:
        """
        Добавляет клиента в конфигурацию WireGuard.
        """
        try:
            with open(self.wg_conf_path, "a", encoding="utf-8") as config_file:
                config_file.write(
                    self.create_str_wg_conf(ip_addr, public_key, name, date, comment)
                )
        except OSError as e:
            raise RuntimeError(
                f"Не удалось добавить клиента в конфигурацию: {self.wg_conf_path}"
            ) from e

    def create_client_to_configuration(
        self,
        client_name: str,
        ip_address: str,
        private_key: str,
    ) -> None:
        """
        Создаёт клиентский конфигурационный файл.
        """
        client_dir = os.path.join(self.work_dir, self.configs_dir, client_name)
        client_conf_path = os.path.join(client_dir, f"{client_name}{self.conf_ext}")

        try:
            with open(client_conf_path, "x", encoding="utf-8") as config_file:
                config_file.write(
                    self.create_str_client_conf(ip_address, private_key)
                )
        except FileExistsError as e:
            raise FileExistsError(
                f"Конфигурация клиента уже существует: {client_conf_path}"
            ) from e
        except OSError as e:
            raise RuntimeError(
                f"Не удалось создать конфигурацию клиента: {client_conf_path}"
            ) from e

    def remove_configuration_by_ip(self, ip_address: str) -> None:
        """
        Удаляет конфигурацию по указанному IP-адресу из wg-конфига.
        """
        config_text = self.read_configuration_file(self.wg_conf_path)
        updated_config_text = self.remove_ip_configuration(config_text, ip_address)
        self.write_configuration_file(self.wg_conf_path, updated_config_text)

    def read_configuration_file(self, path: str) -> str:
        """
        Читает файл конфигурации и возвращает содержимое.
        """
        try:
            with open(path, "r", encoding="utf-8") as config_file:
                return config_file.read()
        except OSError as e:
            raise RuntimeError(f"Не удалось прочитать файл конфигурации: {path}") from e

    def write_configuration_file(self, path: str, config_text: str) -> None:
        """
        Записывает обновлённое содержимое в файл конфигурации.
        """
        try:
            with open(path, "w", encoding="utf-8") as config_file:
                config_file.write(config_text)
        except OSError as e:
            raise RuntimeError(f"Не удалось записать файл конфигурации: {path}") from e

    def remove_ip_configuration(self, config_text: str, ip_address: str) -> str:
        """
        Удаляет конфигурацию для указанного IP-адреса из текста конфигурации.
        """
        search_string = f"AllowedIPs = {ip_address}/32"
        start_index = config_text.find(search_string)

        if start_index == -1:
            return config_text

        peer_index = config_text.rfind("[Peer]", 0, start_index)

        if peer_index == -1:
            return config_text[:start_index]

        return config_text[:peer_index]

    def extract_from_config(self, config_file_path: str) -> str:
        """
        Извлекает peer-информацию из конфигурационного файла и возвращает JSON-строку.
        """
        result = []
        current_peer = None
        allowed_ips = None

        try:
            with open(config_file_path, "r", encoding="utf-8") as config_file:
                for line in config_file:
                    line = line.strip()

                    if not line:
                        continue

                    if line.startswith("[Peer]"):
                        if current_peer and allowed_ips:
                            result.append(current_peer)

                        current_peer = {
                            "ip_address": None,
                            "peer_info": {
                                "name": "No name",
                                "date_range": {
                                    "start_date": "не указано",
                                    "end_date": "не указано",
                                },
                                "comment": "",
                            },
                        }
                        allowed_ips = None

                    elif line.startswith("AllowedIPs"):
                        allowed_ips = line.split("=")[1].strip()
                        if current_peer:
                            current_peer["ip_address"] = allowed_ips

                    elif line.startswith("#") and current_peer:
                        if "name:" in line:
                            current_peer["peer_info"]["name"] = line.split("name:")[1].strip()
                        elif "date:" in line:
                            date_range = line.split("date:")[1].strip()
                            if " - " in date_range:
                                start_date, end_date = date_range.split(" - ", 1)
                                current_peer["peer_info"]["date_range"]["start_date"] = start_date.strip()
                                current_peer["peer_info"]["date_range"]["end_date"] = end_date.strip()
                        elif "comment:" in line:
                            current_peer["peer_info"]["comment"] = line.split("comment:")[1].strip()

                if current_peer and allowed_ips:
                    result.append(current_peer)

        except OSError as e:
            raise RuntimeError(
                f"Не удалось извлечь данные из конфигурации: {config_file_path}"
            ) from e

        return json.dumps(result, ensure_ascii=False, indent=4)

    def get_wg_peers_json(self, interface: str = "wg0") -> str:
        """
        Получает информацию о пирах WireGuard и возвращает её в формате JSON.
        """
        try:
            output = subprocess.check_output(
                ["wg", "show", interface],
                text=True,
                encoding="utf-8",
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Не удалось выполнить команду wg show {interface}"
            ) from e
        except FileNotFoundError as e:
            raise RuntimeError("Команда 'wg' не найдена в системе") from e

        peer_pattern = re.compile(
            r"peer: (.+?)\n\s+endpoint: (.+?)\n\s+allowed ips: (.+?)\n\s+latest handshake: (.+?)\n\s+transfer: (.+?) received, (.+?) sent"
        )

        peers = peer_pattern.findall(output)

        result = []
        for peer in peers:
            peer_info = {
                "ip_address": peer[2],
                "peer_info": {
                    "latest_handshake": peer[3],
                    "transfer": {
                        "received": peer[4],
                        "sent": peer[5],
                    },
                },
            }
            result.append(peer_info)

        return json.dumps(result, ensure_ascii=False, indent=4)

    def combo_json(self, json_1: str, json_2: str) -> str:
        """
        Объединяет два JSON-представления peer-информации.
        """
        data1 = json.loads(json_1)
        data2 = json.loads(json_2)

        combined_data = {}

        for item in data1:
            ip_address = item["ip_address"]
            combined_data[ip_address] = item

        for item in data2:
            ip_address = item["ip_address"]
            if ip_address in combined_data:
                combined_data[ip_address]["peer_info"].update(item["peer_info"])
            else:
                combined_data[ip_address] = item

        return json.dumps(
            list(combined_data.values()),
            ensure_ascii=False,
            indent=4,
        )
