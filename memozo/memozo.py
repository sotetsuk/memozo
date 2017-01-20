import os
import functools
import inspect
import codecs
import pickle

from . import utils


class Memozo(object):

    def __init__(self, path='./'):
        self.base_path = path

    def __call__(self, name=None, ext='file'):

        def wrapper(func):
            _name = func.__name__ if name is None else name

            @functools.wraps(func)
            def _wrapper(*args, **kwargs):
                args = utils.get_bound_args(func, *args, **kwargs)
                args_str = utils.get_args_str(args)
                sha1 = utils.get_hash(_name, func.__name__, args_str)
                file_path = os.path.join(self.base_path, "{}_{}.{}".format(_name, sha1, ext))

                if utils.log_exisits(self.base_path, _name, func.__name__, args_str) and os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        obj = f.readlines()
                    return obj

                obj = func(*args, **kwargs)

                with open(file_path, 'w') as f:
                    f.writelines(obj)
                utils.write(self.base_path, _name, func.__name__, args_str)

                return obj

            return _wrapper

        return wrapper
