import qrcode # type: ignore
from qrcode.constants import ERROR_CORRECT_L # type: ignore


def read_file_content(file_path: str) -> str:
    """Читает содержимое файла и возвращает его в виде строки.
    :param file_path: Путь к файлу.
    :return: Содержимое файла в виде строки.
    """
    with open(file_path, 'r') as file:
        return file.read()


def create_qr_code(data: str, error_correction_level: int = ERROR_CORRECT_L) -> qrcode.QRCode:
    """Создает QR-код на основе переданных данных.
    :param data: Данные для кодирования в QR-код.
    :param error_correction_level: Уровень коррекции ошибок (по умолчанию LOW).
    :return: Объект QRCode.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_correction_level,
        box_size=1,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr


def print_qr_code_to_console(qr: qrcode.QRCode) -> None:
    """Выводит QR-код в консоль.
    :param qr: Объект QRCode.
    """
    qr.print_ascii(tty=True)


def qr_main(file_path) -> None:
    """Основная функция для чтения файла,
    создания QR-кода и вывода его в консоль.
    """
    content = read_file_content(file_path)
    qr_code = create_qr_code(content)
    print_qr_code_to_console(qr_code)