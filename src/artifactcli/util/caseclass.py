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
        return isinstance(other, self.__class__) and all(getattr(self, k) == getattr(other, k) for k in self.__keys)

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, ', '.join('%s=%r' % (k, getattr(self, k)) for k in self.__keys))
