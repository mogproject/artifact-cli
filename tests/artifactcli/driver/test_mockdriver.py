import unittest

from artifactcli.driver.mockdriver import MockDriver


class TestMockDriver(unittest.TestCase):
    def setUp(self):
        pass

    def test_read_index(self):
        # read empty
        m = MockDriver()
        self.assertEqual(m.read_index(), '')

    def test_write_index(self):
        # write some index data then read it
        s = u'index1\nindex2\nindex3'
        m = MockDriver()
        m.write_index(s)
        self.assertEqual(m.read_index(), s)

    def test_upload(self):
        m = MockDriver()
        m.upload('/path/to/the/art-test-0.0.1.jar', 'a/b/c/d/art-test-0.0.1', None)
        m.upload('/path/to/the/art-test-0.0.1.jar', 'a/b/c/d/art-test-0.0.1', 'ffffeeeeddddccccbbbbaaaa99998888')

    def test_download(self):
        m = MockDriver()
        self.assertRaises(ValueError,
                          lambda: m.download('a/b/c/d/art-test-0.0.1', '/path/to/the/art-test-0.0.1.jar', None))
        m.upload('/path/to/the/art-test-0.0.1.jar', 'a/b/c/d/art-test-0.0.1', None)
        m.download('a/b/c/d/art-test-0.0.1', '/path/to/the/art-test-0.0.1.jar', None)

        m.upload('/path/to/the/art-test-0.0.1.jar', 'a/b/c/d/art-test-0.0.1', 'ffffeeeeddddccccbbbbaaaa99998888')
        self.assertRaises(AssertionError,
                          lambda: m.download('a/b/c/d/art-test-0.0.1', '/path/to/the/art-test-0.0.1.jar', 'xxx'))
        m.download('a/b/c/d/art-test-0.0.1', '/path/to/the/art-test-0.0.1.jar',
                   'ffffeeeeddddccccbbbbaaaa99998888')
