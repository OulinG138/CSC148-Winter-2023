import time

def display_time(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print(f'Total run time of {func.__name__}: {t2 - t1:.8f}s')
        return result
    return wrapper
