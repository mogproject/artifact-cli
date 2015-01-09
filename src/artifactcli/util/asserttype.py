def assert_type(value, class_or_type_or_tuple):
    """
    Ensure the type of the value is as expected, then return the value.

    :param value: value of any type
    :param class_or_type_or_tuple: expected type
    :return: value of expected type
    """
    s = "%r must be %r, not %s."
    if not isinstance(value, class_or_type_or_tuple):
        raise TypeError(s % (value, class_or_type_or_tuple, type(value)))

    return value
