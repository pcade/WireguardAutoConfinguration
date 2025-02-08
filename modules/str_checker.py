def is_ascii(s):
    '''Проверяет, состоит ли строка только из символов ASCII.
    '''
    if all(ord(c) < 128 for c in s):
        return True
    else:
        print(f"Параметр - {s}, не соответствует ASCII")
        return False