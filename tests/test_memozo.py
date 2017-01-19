import os
import unittest

from memozo import Memozo


class TestMemozo(unittest.TestCase):

    def test_call(self):
        base_path = './tests/resources/'
        m = Memozo(base_path)

        @m
        def create_dummy_data():
            return dummy_data

        dummy_data = ['This\n', 'is\n', 'a\n', 'test.\n']
        path = os.path.join(base_path, 'test')
        if os.path.exists(path):
            os.remove(path)
        self.assertFalse(os.path.exists(path))
        data = create_dummy_data()
        self.assertTrue(data == dummy_data)
        self.assertTrue(os.path.exists(path))
        dummy_data += ['extra line\n']
        data = create_dummy_data()
        self.assertFalse(data == dummy_data)
