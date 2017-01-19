import os
import unittest

from memozo import Memozo


class TestMemozo(unittest.TestCase):

    def setUp(self):
        self.base_path = './tests/resources/'
        self.m = Memozo(self.base_path)

    def test_call(self):
        dummy_data = ['This\n', 'is\n', 'a\n', 'test.\n']

        @self.m()
        def create_dummy_data():
            """create dummy data"""
            return dummy_data

        # testing save and load
        path = os.path.join(self.base_path, 'create_dummy_data')
        if os.path.exists(path):
            os.remove(path)
        self.assertFalse(os.path.exists(path))
        data = create_dummy_data()
        self.assertTrue(data == dummy_data)
        self.assertTrue(os.path.exists(path))
        dummy_data += ['extra line\n']
        data = create_dummy_data()
        self.assertFalse(data == dummy_data)

    def test_doc_string(self):
        dummy_data = ['This\n', 'is\n', 'a\n', 'test.\n']

        @self.m(name='call_test')
        def create_dummy_data():
            """create dummy data"""
            return dummy_data

        # testing doc string
        self.assertTrue(create_dummy_data.__doc__ == "create dummy data")
