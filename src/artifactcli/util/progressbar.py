import sys
import threading


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

        # create event for handling termination
        self.__stop_event = threading.Event()

        # create and start new thread
        self.thread = threading.Thread(target=self.__target)
        self.thread.start()

    def stop(self):
        """
        Terminate progress bar thread
        """
        self.__stop_event.set()
        self.thread.join()
        self.fp.write('\n')
        self.fp.flush()

    def __target(self):
        """
        Inner method for writing dots in the separated thread
        """
        event = self.__stop_event

        while not event.is_set():
            self.fp.write('.')
            self.fp.flush()
            event.wait(self.interval)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.stop()
