import unittest
import artifactcli.artifactcli


class TestArtifactCli(unittest.TestCase):
    def test_usage(self):
        self.assertEqual(artifactcli.artifactcli.main(), 1)
