import unittest
from src.artima import BasicInfo


class TestBasicInfo(unittest.TestCase):
    def setUp(self):
        self.test_data = [
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None),
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1.2', 'zip', 345),
        ]

    def test_eq(self):
        self.assertEqual(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None),
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None))
        self.assertEqual(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123),
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123))

    def test_ne(self):
        self.assertNotEqual(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None),
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'zip', None))
        self.assertNotEqual(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123),
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None))
        self.assertNotEqual(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123),
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 124))

    def test_filename(self):
        self.assertEqual(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None).filename(),
            'xxx-yyy-assembly-0.1-SNAPSHOT.jar')
        self.assertEqual(
            BasicInfo('GROUP_ID', 'xxxxxx', '1.2.3', 'zip', 123).filename(),
            'xxxxxx-1.2.3.zip')

    def test_is_version_like(self):
        self.assertEqual(BasicInfo._is_version_like('0'), True)
        self.assertEqual(BasicInfo._is_version_like('1'), True)
        self.assertEqual(BasicInfo._is_version_like('0.2'), True)
        self.assertEqual(BasicInfo._is_version_like('0.0.3'), True)
        self.assertEqual(BasicInfo._is_version_like('1.2.3.4'), True)
        self.assertEqual(BasicInfo._is_version_like(''), False)
        self.assertEqual(BasicInfo._is_version_like('a'), False)
        self.assertEqual(BasicInfo._is_version_like('.'), False)
        self.assertEqual(BasicInfo._is_version_like('0.'), False)
        self.assertEqual(BasicInfo._is_version_like('0.1.'), False)
        self.assertEqual(BasicInfo._is_version_like('0..1'), False)
        self.assertEqual(BasicInfo._is_version_like('1.2.3.4.a'), False)

    def test_from_path(self):
        self.assertEqual(BasicInfo.from_path('a', '/home/user/xxx-yyy-assembly-0.1.0-SNAPSHOT.jar'),
                         BasicInfo('a', 'xxx-yyy-assembly', '0.1.0-SNAPSHOT', 'jar', None))
        self.assertEqual(BasicInfo.from_path('b', '/home/user/xxx-yyy-assembly-0.1.jar'),
                         BasicInfo('b', 'xxx-yyy-assembly', '0.1', 'jar', None))
        self.assertEqual(BasicInfo.from_path('c', '/a/b/c/d/dist/d-0.1.0.zip'),
                         BasicInfo('c', 'd', '0.1.0', 'zip', None))
        self.assertEqual(BasicInfo.from_path('d', 'a/b/c/d/target/universal/d-2.0-1.0-SNAPSHOT.zip'),
                         BasicInfo('d', 'd-2.0', '1.0-SNAPSHOT', 'zip', None))

    def test_dict_conversions(self):
        self.assertEqual(BasicInfo.from_dict(self.test_data[0].to_dict()), self.test_data[0])
        self.assertEqual(BasicInfo.from_dict(self.test_data[1].to_dict()), self.test_data[1])
