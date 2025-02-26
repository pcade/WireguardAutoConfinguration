import qrcode  # type: ignore
from qrcode.constants import ERROR_CORRECT_L  # type: ignore
from PIL import Image  # type: ignore


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
        box_size=10,  # Увеличим размер для лучшей читаемости
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr


def save_qr_code_to_file(qr: qrcode.QRCode, file_path: str) -> None:
    """Сохраняет QR-код в файл.
    :param qr: Объект QRCode.
    :param file_path: Путь для сохранения файла с QR-кодом.
    """
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_path)


def qr_main(input_file_path: str, output_file_path: str) -> None:
    """Основная функция для чтения файла,
    создания QR-кода и сохранения его в файл.
    :param input_file_path: Путь к файлу с данными для QR-кода.
    :param output_file_path: Путь для сохранения файла с QR-кодом.
    """
    content = read_file_content(input_file_path)
    qr_code = create_qr_code(content)
    save_qr_code_to_file(qr_code, output_file_path)