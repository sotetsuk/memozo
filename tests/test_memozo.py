import os
import unittest

from memozo import Memozo, utils


class TestMemozoCall(unittest.TestCase):

    def setUp(self):
        self.base_path = './tests/resources/'
        self.m = Memozo(self.base_path)
        self.dummy_data = ['This\n', 'is\n', 'a\n', 'test.\n']

    def test_call(self):

        @self.m()
        def create_dummy_data():
            """create dummy data"""
            return self.dummy_data

        # testing save and load
        file_path = os.path.join(self.base_path, 'create_dummy_data_' +
                                 utils.get_hash('create_dummy_data', 'create_dummy_data', '') + '.file')
        self.assertFalse(os.path.exists(file_path))
        data = create_dummy_data()
        self.assertTrue(data == self.dummy_data)
        self.assertTrue(os.path.exists(file_path))
        self.dummy_data += ['extra line\n']
        data = create_dummy_data()
        self.assertFalse(data == self.dummy_data)

        os.remove(file_path)

    def test_doc_string(self):
        @self.m()
        def create_dummy_data():
            """create dummy data"""
            return self.dummy_data

        # testing doc string
        self.assertTrue(create_dummy_data.__doc__ == "create dummy data")

    def test_set_name(self):
        name = 'call_test'

        @self.m(name=name)
        def create_dummy_data():
            """create dummy data"""
            return self.dummy_data

        create_dummy_data()
        file_path = os.path.join(self.base_path, 'call_test_' +
                                 utils.get_hash('call_test', 'create_dummy_data', '') + '.file')
        self.assertTrue(os.path.exists(file_path))

        os.remove(file_path)

    def test_args(self):
        name = 'test_args'

        @self.m(name=name)
        def create_dummy_data(param):
            """create dummy data"""
            return self.dummy_data

        args_str = utils.get_args_str({'param': 3})
        file_path = os.path.join(self.base_path, name + '_' +
                                 utils.get_hash(name, 'create_dummy_data', args_str) + '.file')
        self.assertFalse(os.path.exists(file_path))
        create_dummy_data(3)
        self.assertTrue(os.path.exists(file_path))

        os.remove(file_path)