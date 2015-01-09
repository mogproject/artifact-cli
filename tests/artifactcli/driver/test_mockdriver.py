import unittest

from artifactcli.driver.mockdriver import MockDriver


class TestMockDriver(unittest.TestCase):
    def setUp(self):
        pass

    def test_read_index(self):
        # read empty
        m = MockDriver()
        self.assertEqual(m.read_index('test-artifact'), '')

    def test_write_index(self):
        # write some index data then read it
        s = u'index1\nindex2\nindex3'
        m = MockDriver()
        m.write_index('test-artifact', s)
        self.assertEqual(m.read_index('test-artifact'), s)

    def test_upload(self):
        m = MockDriver()
        m.upload('/path/to/art-test-0.0.1.jar', 'a/b/c/d/art-test-0.0.1', None)
        self.assertEqual(m.uploaded_data, {'a/b/c/d/art-test-0.0.1': ('/path/to/art-test-0.0.1.jar', 'example_md5')})

        m.upload('/path/to/art-test-0.0.1.jar', 'a/b/c/d/art-test-0.0.1', 'ffffeeeeddddccccbbbbaaaa99998888')
        self.assertEqual(m.uploaded_data, {
            'a/b/c/d/art-test-0.0.1': ('/path/to/art-test-0.0.1.jar', 'ffffeeeeddddccccbbbbaaaa99998888')
        })

    def test_download(self):
        m = MockDriver()
        self.assertRaises(ValueError, m.download, 'a/b/c/d/art-test-0.0.1', '/path/to/art-test-0.0.1.jar', None)
        m.upload('/path/to/art-test-0.0.1.jar', 'a/b/c/d/art-test-0.0.1', None)
        m.download('a/b/c/d/art-test-0.0.1', '/path/to/art-test-0.0.1.jar', None)
        self.assertEqual(m.downloaded_data, {'/path/to/art-test-0.0.1.jar': ('a/b/c/d/art-test-0.0.1', 'example_md5')})

        m.upload('/path/to/art-test-0.0.1.jar', 'a/b/c/d/art-test-0.0.1', 'ffffeeeeddddccccbbbbaaaa99998888')
        self.assertRaises(AssertionError, m.download, 'a/b/c/d/art-test-0.0.1', '/path/to/art-test-0.0.1.jar', 'xxx')
        m.download('a/b/c/d/art-test-0.0.1', '/path/to/art-test-0.0.1.jar', 'ffffeeeeddddccccbbbbaaaa99998888')
        self.assertEqual(m.downloaded_data, {
            '/path/to/art-test-0.0.1.jar': ('a/b/c/d/art-test-0.0.1', 'ffffeeeeddddccccbbbbaaaa99998888')
        })

    def test_delete(self):
        m = MockDriver()
        self.assertRaises(ValueError, m.delete, '/path/to/art-test-0.0.1.jar', None)
        m.upload('/path/to/art-test-0.0.1.jar', 'a/b/c/d/art-test-0.0.1', None)
        m.delete('a/b/c/d/art-test-0.0.1', None)
        self.assertEqual(m.uploaded_data, {})

        m.upload('/path/to/art-test-0.0.1.jar', 'a/b/c/d/art-test-0.0.1', 'ffffeeeeddddccccbbbbaaaa99998888')
        self.assertRaises(AssertionError, m.delete, 'a/b/c/d/art-test-0.0.1', 'xxx')
        m.delete('a/b/c/d/art-test-0.0.1', 'ffffeeeeddddccccbbbbaaaa99998888')
        self.assertEqual(m.uploaded_data, {})
