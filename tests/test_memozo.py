import os
import unittest

from memozo import Memozo


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
        path = os.path.join(self.base_path, 'create_dummy_data')
        if os.path.exists(path):
            os.remove(path)
        self.assertFalse(os.path.exists(path))
        data = create_dummy_data()
        self.assertTrue(data == self.dummy_data)
        self.assertTrue(os.path.exists(path))
        self.dummy_data += ['extra line\n']
        data = create_dummy_data()
        self.assertFalse(data == self.dummy_data)

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

        self.assertTrue(os.path.exists(os.path.join(self.base_path, name)))
