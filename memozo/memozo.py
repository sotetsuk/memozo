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

    def codecs(self, name=None, ext='file', encoding=None):

        def wrapper(func):
            _name = func.__name__ if name is None else name

            @functools.wraps(func)
            def _wrapper(*args, **kwargs):
                args = utils.get_bound_args(func, *args, **kwargs)
                args_str = utils.get_args_str(args)
                sha1 = utils.get_hash(_name, func.__name__, args_str)
                file_path = os.path.join(self.base_path, "{}_{}.{}".format(_name, sha1, ext))

                if utils.log_exisits(self.base_path, _name, func.__name__, args_str) and os.path.exists(file_path):
                    with codecs.open(file_path, 'r', encoding) as f:
                        obj = f.readlines()
                    return obj

                obj = func(*args, **kwargs)

                with codecs.open(file_path, 'w', encoding) as f:
                    f.writelines(obj)
                utils.write(self.base_path, _name, func.__name__, args_str)

                return obj

            return _wrapper

        return wrapper

    def generator(self, name=None, ext='file'):

        def wrapper(func):
            _name = func.__name__ if name is None else name

            @functools.wraps(func)
            def _wrapper(*args, **kwargs):
                # get cached data path
                args = utils.get_bound_args(func, *args, **kwargs)
                args_str = utils.get_args_str(args)
                sha1 = utils.get_hash(_name, func.__name__, args_str)
                file_path = os.path.join(self.base_path, "{}_{}.{}".format(_name, sha1, ext))

                # if cached data exists, return generator using cached data
                if utils.log_exisits(self.base_path, _name, func.__name__, args_str) and os.path.exists(file_path):
                    def gen_cached_data():
                        with codecs.open(file_path, 'r', utils.ENCODING) as f:
                            for line in f:
                                yield line
                    return gen_cached_data

                gen = func(*args, **kwargs)

                # if no cached data exists, generator not only yield value but save value at each iteration
                def generator_with_cache(gen, file_path):
                    with codecs.open(file_path, 'w', utils.ENCODING) as f:
                        for e in gen:
                            f.write(e)
                            yield e

                return generator_with_cache(gen, file_path)

            return _wrapper

        return wrapper

    def pickle(self, name=None, ext='pickle', protocol=None):

        def wrapper(func):
            _name = func.__name__ if name is None else name

            @functools.wraps(func)
            def _wrapper(*args, **kwargs):
                args = utils.get_bound_args(func, *args, **kwargs)
                args_str = utils.get_args_str(args)
                sha1 = utils.get_hash(_name, func.__name__, args_str)
                file_path = os.path.join(self.base_path, "{}_{}.{}".format(_name, sha1, ext))

                if utils.log_exisits(self.base_path, _name, func.__name__, args_str) and os.path.exists(file_path):
                    with open(file_path, 'rb') as f:
                        obj = pickle.load(f)
                    return obj

                obj = func(*args, **kwargs)

                with open(file_path, 'wb') as f:
                    pickle.dump(obj, f, protocol=protocol)
                utils.write(self.base_path, _name, func.__name__, args_str)

                return obj

            return _wrapper

        return wrapper
