from datetime import datetime


def log(*args, **kwargs):
    dt_formatter = "%Y/%m/%d %H:%M:%S >> "
    dt = datetime.now().strftime(dt_formatter)
    print(dt, args, kwargs.keys())


def rect_intersects(a, b):
    return a.x < b.x < a.x+a.width and a.y < b.y < a.y+a.height


def __test():
    log()

if __name__ == '__main__':
    log()
