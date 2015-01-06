class CaseClass(object):
    """
    Implementation like Scala's case class
    """

    def __init__(self, keys):
        """
        :param keys: list of attribute names
        """
        self.__keys = keys

    def __cmp__(self, other):
        if not isinstance(other, self.__class__):
            # compare with class names
            return cmp(self.__class__.__name__, other.__class__.__name__)

        for k in self.__keys:
            a, b = getattr(self, k), getattr(other, k)
            if a < b:
                return -1
            if a > b:
                return 1
        return 0

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, ', '.join('%s=%r' % (k, getattr(self, k)) for k in self.__keys))
