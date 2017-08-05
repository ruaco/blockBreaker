from datetime import datetime
import json


def log(*args, **kwargs):
    # dt_formatter = "%Y/%m/%d %H:%M:%S >> "
    # dt = datetime.now().strftime(dt_formatter)
    print(args, kwargs.keys())


def rect_intersects(a, b):
    o = a
    if o.y < b.y < o.y + o.height:
        if o.x < b.x < o.x + o.width:
            return True
    return False


def load_config_from_file():
    file_path = 'config.json'
    with open(file_path, 'r', newline='', encoding='utf-8') as f:
        return json.load(f)


class Rect:
    x = None
    y = None
    width = None
    height = None


def __test():
    a = Rect()
    setattr(a, 'x', 85)
    setattr(a, 'y', 101)
    setattr(a, 'width', 8)
    setattr(a, 'height', 8)
    b = Rect()
    setattr(b, 'x', 50)
    setattr(b, 'y', 100)
    setattr(b, 'width', 40)
    setattr(b, 'height', 19)
    log(rect_intersects(a, b) or rect_intersects(b, a))

if __name__ == '__main__':
    __test()
    print(load_config_from_file())
