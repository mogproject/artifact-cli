from abc import ABCMeta, abstractmethod


class BaseInfo(object):
    __metaclass__ = ABCMeta

    def __init__(self, klass, keys):
        self.klass = klass
        self.keys = keys

    def __eq__(self, other):
        return isinstance(other, self.klass) and all(getattr(self, k) == getattr(other, k) for k in self.keys)

    def __ne__(self, other):
        return not self == other