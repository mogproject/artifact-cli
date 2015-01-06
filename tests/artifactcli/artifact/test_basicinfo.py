import unittest
from artifactcli.artifact import BasicInfo


class TestBasicInfo(unittest.TestCase):
    def setUp(self):
        self.test_data = [
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None),
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1.2', 'zip', 345),
        ]

    class A(object):
        pass

    def test_eq(self):
        self.assertTrue(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None) ==
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None))
        self.assertTrue(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) ==
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123))
        self.assertFalse(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None) ==
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'zip', None))
        self.assertFalse(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) ==
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None))
        self.assertFalse(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) ==
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 124))
        self.assertFalse(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) ==
            BasicInfo('com.github.mogprojectX', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123))
        self.assertFalse(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) ==
            BasicInfo('com.github.mogproject', 'xxx-yyy-assemblyX', '0.1-SNAPSHOT', 'jar', 123))
        self.assertFalse(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) ==
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOTX', 'jar', 123))
        self.assertFalse(BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) == 123)

    def test_ne(self):
        self.assertFalse(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None) !=
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None))
        self.assertFalse(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) !=
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123))
        self.assertTrue(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None) !=
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'zip', None))
        self.assertTrue(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) !=
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None))
        self.assertTrue(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) !=
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 124))
        self.assertTrue(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) !=
            BasicInfo('com.github.mogprojectX', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123))
        self.assertTrue(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) !=
            BasicInfo('com.github.mogproject', 'xxx-yyy-assemblyX', '0.1-SNAPSHOT', 'jar', 123))
        self.assertTrue(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) !=
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOTX', 'jar', 123))
        self.assertTrue(BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) != 123)

    def test_lt(self):
        self.assertFalse(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None) <
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None))
        self.assertTrue(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None) <
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 10))
        self.assertFalse(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 10) <
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None))
        self.assertFalse(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 1) <
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 1))
        self.assertFalse(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 10) <
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 1))
        self.assertTrue(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 1) <
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 10))
        self.assertFalse(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) <
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 10))
        self.assertTrue(BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) < 123)
        self.assertTrue(BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) < '123')
        self.assertFalse(BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) < self.A())

    def test_le(self):
        self.assertTrue(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None) <=
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None))
        self.assertTrue(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None) <=
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 10))
        self.assertFalse(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 10) <=
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None))
        self.assertTrue(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 1) <=
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 1))
        self.assertFalse(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 10) <=
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 1))
        self.assertTrue(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 1) <=
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 10))
        self.assertFalse(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) <=
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 10))
        self.assertTrue(BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) <= 123)
        self.assertTrue(BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) <= '123')
        self.assertFalse(BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) <= self.A())

    def test_gt(self):
        self.assertFalse(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None) >
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None))
        self.assertFalse(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None) >
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 10))
        self.assertTrue(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 10) >
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None))
        self.assertFalse(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 1) >
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 1))
        self.assertTrue(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 10) >
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 1))
        self.assertFalse(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 1) >
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 10))
        self.assertTrue(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) >
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 10))
        self.assertFalse(BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) > 123)
        self.assertFalse(BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) > '123')
        self.assertTrue(BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) > self.A())

    def test_ge(self):
        self.assertTrue(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None) >=
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None))
        self.assertFalse(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None) >=
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 10))
        self.assertTrue(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 10) >=
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', None))
        self.assertTrue(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 1) >=
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 1))
        self.assertTrue(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 10) >=
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 1))
        self.assertFalse(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 1) >=
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 10))
        self.assertTrue(
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) >=
            BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 10))
        self.assertFalse(BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) >= 123)
        self.assertFalse(BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) >= '123')
        self.assertTrue(BasicInfo('com.github.mogproject', 'xxx-yyy-assembly', '0.1-SNAPSHOT', 'jar', 123) >= self.A())

    def test_str_type(self):
        self.assertTrue(all(isinstance(x.__str__(), str) for x in self.test_data))

    def test_repr(self):
        self.assertEqual(
            repr(self.test_data[0]),
            "BasicInfo(group_id='com.github.mogproject', artifact_id='xxx-yyy-assembly'," +
            " version='0.1-SNAPSHOT', packaging='jar', revision=None)")
        self.assertEqual(
            repr(self.test_data[1]),
            "BasicInfo(group_id='com.github.mogproject', artifact_id='xxx-yyy-assembly'," +
            " version='0.1.2', packaging='zip', revision=345)")

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

    def test_from_path_error(self):
        self.assertRaises(ValueError, BasicInfo.from_path, 'a', 'zip')
        self.assertRaises(ValueError, BasicInfo.from_path, 'b', '.zip')
        self.assertRaises(ValueError, BasicInfo.from_path, 'c', '0.1.2.zip')
        self.assertRaises(ValueError, BasicInfo.from_path, 'd', 'a-b-c.zip')
        self.assertRaises(ValueError, BasicInfo.from_path, 'e', 'a-b-c-0')
        self.assertRaises(ValueError, BasicInfo.from_path, 'f', 'a-b-c-0.1.2.')

    def test_s3_path(self):
        self.assertEqual(self.test_data[1].s3_path(),
                         'com.github.mogproject/xxx-yyy-assembly/0.1.2/345/xxx-yyy-assembly-0.1.2.zip')

    def test_s3_path_error(self):
        self.assertRaises(ValueError, self.test_data[0].s3_path)

    def test_dict_conversions(self):
        self.assertEqual(BasicInfo.from_dict(self.test_data[0].to_dict()), self.test_data[0])
        self.assertEqual(BasicInfo.from_dict(self.test_data[1].to_dict()), self.test_data[1])
