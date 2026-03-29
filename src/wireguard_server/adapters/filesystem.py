import os
import shutil


class FileSystemAdapter:
    def __init__(self, work_dir: str, configs_dir: str, wg0: str, conf_ext: str):
        self.work_dir = work_dir
        self.configs_dir = configs_dir
        self.wg0 = wg0
        self.conf_ext = conf_ext

    def dir_creator(self, path: str, name: str) -> None:
        full_path = os.path.join(path, name)
        try:
            os.makedirs(full_path, exist_ok=True)
        except OSError as e:
            raise RuntimeError(f"Не удалось создать директорию: {full_path}") from e

    def pre_start_checks(self) -> None:
        if not os.path.isdir(self.work_dir):
            raise FileNotFoundError(f"WORK_DIR не найден: {self.work_dir}")

        conf_path = f"{self.work_dir}{self.wg0}{self.conf_ext}"
        if not os.path.isfile(conf_path):
            raise FileNotFoundError(f"Конфиг не найден: {conf_path}")

        configs_path = f"{self.work_dir}{self.configs_dir}"
        if not os.path.isdir(configs_path):
            self.dir_creator(self.work_dir, self.configs_dir)

    def path_worker(self, name: str) -> None:
        if os.path.isdir(self.work_dir + name):
            raise FileExistsError("Директория уже существует")

        if os.path.isfile(f"{self.work_dir}{name}/{name}{self.conf_ext}"):
            raise FileExistsError("Конфигурация уже существует")

        self.dir_creator(self.work_dir + self.configs_dir, name)

    def dir_remover(self, name: str) -> None:
        path = os.path.join(self.work_dir, self.configs_dir, name)
        try:
            shutil.rmtree(path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Директория не найдена: {path}")
        except OSError as e:
            raise RuntimeError(f"Ошибка при удалении: {path}") from e
