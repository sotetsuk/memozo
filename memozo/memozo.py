import os
import functools
import codecs
import pickle


class Memozo(object):

    def __init__(self, path='./'):
        self.base_path = path

    def __call__(self, func):
        file_path = os.path.join(self.base_path, 'test')

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    obj = f.readlines()
                return obj

            obj = func(*args, **kwargs)

            with open(file_path, 'w') as f:
                f.writelines(obj)

            return obj

        return wrapper
