import sys
import threading
from Queue import Queue


class ProgressBar(object):
    """
    Print progress bar in the separated thread
    """

    def __init__(self, interval=1, fp=sys.stdout):
        """
        Start thread for progress bar
        :param interval: interval seconds to write dots
        :param fp: file pointer to write
        """
        self.interval = interval
        self.fp = fp
        self.ex_queue = Queue()  # store all exceptions raised in thread

        # create event for handling termination
        self.__stop_event = threading.Event()

        # create and start new thread
        self.thread = threading.Thread(target=lambda: self.__capture_exceptions(self.__target))
        self.thread.start()

    def stop(self):
        """
        Terminate progress bar thread
        """
        self.__stop_event.set()
        self.thread.join()

        # check thread's exceptions
        if not self.ex_queue.empty():
            raise self.ex_queue.get_nowait()

    def __capture_exceptions(self, f):
        """
        Wrapper function to capture all exceptions which are raised in the thread
        """
        try:
            f()
        except Exception as e:
            self.ex_queue.put(e)
            raise e

    def __target(self):
        """
        Inner method for writing dots in the separated thread
        """
        event = self.__stop_event

        while not event.is_set():
            self.fp.write('.')
            self.fp.flush()
            event.wait(self.interval)
        self.fp.write('\n')

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.stop()
