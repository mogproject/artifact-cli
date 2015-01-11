import unittest
from StringIO import StringIO
import time
from artifactcli.util.progressbar import ProgressBar


class TestProgressBar(unittest.TestCase):
    def test_progress_bar(self):
        fp = StringIO()
        p = ProgressBar(0.6, fp)
        time.sleep(1)
        p.stop()
        s = fp.getvalue()
        fp.close()
        self.assertEqual(s, '..\n')

    def test_progress_bar_with(self):
        fp = StringIO()
        with ProgressBar(0.6, fp):
            time.sleep(1)
        s = fp.getvalue()
        fp.close()
        self.assertEqual(s, '..\n')

    def test_progress_bar_runtime_error(self):
        fp = StringIO()
        try:
            with ProgressBar(0.6, fp):
                time.sleep(1)
                raise RuntimeError
        except RuntimeError:
            pass

        time.sleep(0.5)
        s = fp.getvalue()
        fp.close()
        self.assertEqual(s, '..\n')

    def test_progress_bar_io_error(self):
        fp = StringIO()
        p = ProgressBar(0.6, fp)
        time.sleep(1)
        fp.close()
        time.sleep(1)

        self.assertRaises(ValueError, p.stop)
