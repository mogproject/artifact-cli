from unicodedata import east_asian_width
from asserttype import assert_type


def to_str(s, encoding='utf-8'):
    """
    Safe str/unicode to str conversion

    :param s: string in str or unicode
    :param encoding: encoding
    :return: str
    """
    if isinstance(s, str):
        return s
    if isinstance(s, unicode):
        return s.encode(encoding)
    raise ValueError('Failed to convert to str: %r' % s)


def to_unicode(s, encoding='utf-8'):
    """
    Safe str/unicode to unicode conversion

    :param s: string in str or unicode
    :param encoding: encoding
    :return: unicode string
    """
    if isinstance(s, str):
        return unicode(s, encoding)
    if isinstance(s, unicode):
        return s
    raise ValueError('Failed to convert to unicode: %r' % s)


def unicode_char_width(unichr):
    """
    Return width of one unicode character
    i.e. Hankaku -> count as 1, Zenkaku -> count as 2

    :param unichr: unicode character
    :return: width
    """
    return {'F': 2, 'H': 1, 'W': 2, 'Na': 1, 'A': 2, 'N': 1}[east_asian_width(unichr)]


def unicode_width(s):
    """
    Count total width of unicode string

    :param s: unicode string
    :return: total width
    """
    return sum(map(unicode_char_width, to_unicode(s)))


def __unicode_justify(s, width, fillchar, f):
    if len(fillchar) != 1:
        raise TypeError('must be char, not str')

    l, r = f(max(0, width - unicode_width(s)) / unicode_width(fillchar))
    return fillchar * l + to_unicode(s) + fillchar * r


def unicode_ljust(s, width, fillchar=' '):
    """
    Return left-justified in a unicode string of length width.

    :param s: string in str or unicode
    :param width: minimum width of the result string
    :param fillchar: fill character for padding (default: space)
    :return: padded unicode string
    """
    return __unicode_justify(s, width, fillchar, lambda x: (0, x))


def unicode_rjust(s, width, fillchar=' '):
    """
    Return right-justified in a unicode string of length width.

    :param s: string in str or unicode
    :param width: minimum width of the result string
    :param fillchar: fill character for padding (default: space)
    :return: padded unicode string
    """
    return __unicode_justify(s, width, fillchar, lambda x: (x, 0))


def unicode_center(s, width, fillchar=' '):
    """
    Return center-justified in a unicode string of length width.

    :param s: string in str or unicode
    :param width: minimum width of the result string
    :param fillchar: fill character for padding (default: space)
    :return: padded unicode string
    """
    return __unicode_justify(s, width, fillchar, lambda x: (x / 2, x - x / 2))
