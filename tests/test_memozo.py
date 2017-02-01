import os
import unittest
import codecs
import pickle

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


class TestMemozoCodecs(unittest.TestCase):

    def test_no_cache_output(self):
        base_path = './tests/resources'
        m = Memozo(base_path)

        @m.codecs('codecs_test', encoding='utf-8')
        def codecs_test_func():
            return ['This\n', 'is\n', 'test.\n']

        expected = ['This\n', 'is\n', 'test.\n']
        actual = codecs_test_func()
        self.assertEqual(expected, actual)

        sha1 = utils.get_hash('codecs_test', 'codecs_test_func', '')
        file_path = os.path.join(base_path, "{}_{}.{}".format('codecs_test', sha1, 'file'))
        os.remove(file_path)

    def test_data_has_cached_collectly(self):
        # TODO(sotetsuk): WRITE THIS TEST
        pass

    def test_load_data_from_cache(self):
        # TODO(sotetsuk): WRITE THIS TEST
        pass


class TestMemozoGenerator(unittest.TestCase):

    def test_no_cache_output(self):
        base_path = './tests/resources'
        m = Memozo(base_path)

        @m.generator('gen_test')
        def gen_test_func():
            for i in range(10):
                if i % 3 == 0:
                    yield "{}\n".format(i)

        gen = gen_test_func()
        for i in gen:
            self.assertTrue(int(i.strip('\n')) % 3 == 0)

        sha1 = utils.get_hash('gen_test', 'gen_test_func', '')
        file_path = os.path.join(base_path, "{}_{}.{}".format('gen_test', sha1, 'file'))
        os.remove(file_path)

    def test_data_cached_collectly(self):
        base_path = './tests/resources'
        m = Memozo(base_path)
        sha1 = utils.get_hash('gen_test', 'gen_test_func', '')
        file_path = os.path.join(base_path, "{}_{}.{}".format('gen_test', sha1, 'file'))

        @m.generator('gen_test')
        def gen_test_func():
            for i in range(10):
                if i % 3 == 0:
                    yield "{}\n".format(i)

        gen1 = gen_test_func()
        for _ in gen1:
            continue

        with codecs.open(file_path, 'r', 'utf-8') as f:
            for line in f:
                self.assertTrue(int(line.strip('\n')) % 3 == 0)

        os.remove(file_path)

    def test_load_data_from_cache(self):
        # TODO(sotetsuk): WRITE THIS TEST
        pass

    def test_no_cache_output_tuple(self):
        base_path = './tests/resources'
        m = Memozo(base_path)

        @m.generator('gen_test', line_type='tuple')
        def gen_test_func():
            for i in range(10):
                if i % 3 == 0:
                    yield (str(i), str(i + 1))

        gen = gen_test_func()
        for i in gen:
            self.assertTrue(int(i[0]) % 3 == 0)

        sha1 = utils.get_hash('gen_test', 'gen_test_func', '')
        file_path = os.path.join(base_path, "{}_{}.{}".format('gen_test', sha1, 'file'))
        os.remove(file_path)


class TestMemozoPickle(unittest.TestCase):

    def test_no_cache_output(self):
        base_path = './tests/resources'
        m = Memozo(base_path)

        @m.pickle('pickle_test', protocol=pickle.HIGHEST_PROTOCOL)
        def pickle_test_func():
            return {'a': 3, 'b': 5}

        expected = {'a': 3, 'b': 5}
        actual = pickle_test_func()
        self.assertTrue(actual == expected)

        sha1 = utils.get_hash('pickle_test', 'pickle_test_func', '')
        file_path = os.path.join(base_path, "{}_{}.{}".format('pickle_test', sha1, 'pickle'))
        os.remove(file_path)

    def test_data_cached_collectly(self):
        # TODO(sotetsuk): WRITE THIS TEST
        pass

    def test_load_data_from_cache(self):
        # TODO(sotetsuk): WRITE THIS TEST
        pass
