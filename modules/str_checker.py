import sys
def is_ascii(s):
    '''Проверяет, состоит ли строка только из символов ASCII.
    '''
    if all(ord(c) < 128 for c in s):
        return True
    else:
        print(f"Параметр - {s}, не соответствует ASCII")
        return False

def get_client_name(args):
    """
    Получить имя клиента из аргументов или
    использовать значение по умолчанию.
    """
    if args.name:
        if not is_ascii(args.name):
            sys.exit(1)
        return args.name
    return 'noName'