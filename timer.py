import time

def display_time(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print(f'Total run time: {t2 - t1:.4}s')
        return result
    return wrapper

@display_time
def f():
    print(1)


print(f())