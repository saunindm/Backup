from datetime import datetime


def log_func(file_name, data):
    '''Метод для записи логов.
    '''
    with open(file_name, 'a') as file:
        result = f'{datetime.now()} | {data} \n'
        file.write(result)
    return f'...'
