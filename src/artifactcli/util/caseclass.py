from functools import total_ordering
from collections import Hashable


@total_ordering
class CaseClass(object):
    """
    Implementation like Scala's case class
    """

    def __init__(self, keys):
        """
        :param keys: list of attribute names
        """
        self.__keys = keys

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            # compare with class names
            return self.__class__.__name__ == other.__class__.__name__

        for k in self.__keys:
            a, b = getattr(self, k), getattr(other, k)
            if a != b:
                return False
        return True

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            # compare with class names
            return self.__class__.__name__ < other.__class__.__name__

        for k in self.__keys:
            a, b = getattr(self, k), getattr(other, k)
            try:
                # None is always less than any datatype
                if a is None and b is not None:
                    return True
                elif a is not None and b is None:
                    return False
                elif a < b:
                    return True
                elif a > b:
                    return False
            except TypeError:
                a, b = self.__to_comparable(a), self.__to_comparable(b)
                if a < b:
                    return True
                elif a > b:
                    return False
        return False

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, ', '.join('%s=%r' % (k, getattr(self, k)) for k in self.__keys))

    def __to_comparable(self, value):
        if isinstance(value, Hashable):
            return hash(value)
        return repr(value)
