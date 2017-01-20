import os
import unittest
import inspect

from memozo import utils


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.base_path = 'tests/resources'
        self.memozo_path = os.path.join(self.base_path, utils.MEMOZO_FILE_NAME)

    def test_get_args_str(self):
        """This test is really important. We check if the two args are equal by comparing args_str"""
        # TODO(sotetsuk): MORE TESTS!! e.g., 1e6, 0.003, ...

        args_str1 = utils.get_args_str({'a': '3', 'b': '4'})
        args_str2 = utils.get_args_str({'a': '3', 'b': 4})

        self.assertNotEqual(args_str1, args_str2)

    def test_hash(self):
        name = "test_hash"
        func_name = "test_func"

        args1 = utils.get_args_str({'a': '3', 'b': '4'})
        args2 = utils.get_args_str({'a': '3', 'b': '4'})
        args3 = utils.get_args_str({'a':'3', 'b': 4})

        sha1 = utils.get_hash(name, func_name, args1)
        sha2 = utils.get_hash(name, func_name, args2)
        sha3 = utils.get_hash(name, func_name, args3)

        self.assertEqual(sha1, sha2)
        self.assertNotEqual(sha1, sha3)

    def test_write(self):
        name = "test_write"
        func_name = "test_func"

        args1 = utils.get_args_str({'a': '3', 'b': '4'})
        utils.write(self.base_path, name, func_name, args1)

        args2 = utils.get_args_str({'a': '3', 'b': 4})
        utils.write(self.base_path, name, func_name, args2)

        os.remove(self.memozo_path)

    def test_exists(self):
        name = "test_exists"
        func_name = "test_func"

        args1 = utils.get_args_str({'a': '3', 'b': '4'})
        args2 = utils.get_args_str({'a': '3', 'b': '4', 'c': '5'})

        utils.write(self.base_path, name, func_name, args1)
        self.assertTrue(utils.exists(self.base_path, name, func_name, args1))
        self.assertFalse(utils.exists(self.base_path, name, func_name, args2))

        os.remove(self.memozo_path)

    def test_get_bound_args(self):

        def func(a, b, c=3):
            return a + b + c

        expected = {'a': 3, 'b': 4, 'c': 5}

        args = (3, 4)
        kwargs = {'c': 5}
        actual = utils.get_bound_args(func, *args, **kwargs)

        self.assertEqual(expected, actual)
