import subprocess
from typing import Optional


def run_system_command(command: str) -> Optional[str]:
    """Выполняет системную команду и возвращает её вывод.
    :param command: Системная команда для выполнения.
    :return: Вывод команды или None, если произошла ошибка.
    """
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            text=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды '{command}': {e.stderr}")
        return None


def restart_service(service_name: str) -> bool:
    """Перезапускает указанный сервис с помощью systemctl.
    :param service_name: Имя сервиса для перезапуска.
    :return: True, если сервис успешно перезапущен, иначе False.
    """
    command = f"systemctl restart {service_name}"
    output = run_system_command(command)
    
    if output is not None:
        print(f"Сервис {service_name} успешно перезапущен.")
        return True
    else:
        print(f"Не удалось перезапустить сервис {service_name}.")
        return False


def reload_daemon():
    """Основная функция скрипта,
    которая перезапускает сервисы bind9 и wg-quick@wg0.service.
    """
    services_to_restart = ["bind9", "wg-quick@wg0.service"]
    
    for service in services_to_restart:
        if not restart_service(service):
            print(f"Прерывание выполнения из-за ошибки в сервисе {service}.")
            return

    print("Все сервисы успешно перезапущены.")