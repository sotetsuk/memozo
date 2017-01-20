import os
import codecs
import inspect
import hashlib
from datetime import datetime


MEMOZO_FILE_NAME = '.memozo'
ENCODING = 'utf-8'
N_DIGITS = 7


def get_memozo_filename(base_path):
    return os.path.join(base_path, MEMOZO_FILE_NAME)


def get_args_str(args):
    args_list = sorted(args.items())
    args_str = ', '.join(['{!r}: {!r}'.format(k, v) for k, v in args_list])
    return args_str


def get_hash(name, func_name, args_str):
    source = '/'.join(["memozo", name, func_name, args_str])
    sha1 = hashlib.sha1(source.encode('utf-8')).hexdigest()
    return sha1[:N_DIGITS]


def write(base_path, name, func_name, args_str):
    memozo_file = get_memozo_filename(base_path)
    sha1 = get_hash(name, func_name, args_str)

    with codecs.open(memozo_file, 'a', ENCODING) as f:
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write('{}\t{}\t{}\t{}\t{}\n'.format(time, sha1, name, func_name, args_str))


def log_exisits(base_path, name, func_name, args_str):
    memozo_file = get_memozo_filename(base_path)
    target_sha1 = get_hash(name, func_name, args_str)

    if not os.path.exists(memozo_file):
        return False

    with codecs.open(memozo_file, 'r', ENCODING) as f:
        for line in f:
            time, sha1, name, func_name, args_str = line.strip('\n').split('\t')
            if sha1 == target_sha1:
                return True

    return False


def get_bound_args(func, *args, **kwargs):
    sig = inspect.signature(func)
    bound_args = sig.bind(*args, **kwargs)
    args = dict(bound_args.arguments)

    return args
