def assert_type(value, class_or_type_or_tuple):
    """
    Ensure the type of the value is as expected, then return the value.

    :param value: value of any type
    :param class_or_type_or_tuple: expected type
    :return: value of expected type
    """
    s = "Value type of %r is not %r but %s."
    assert isinstance(value, class_or_type_or_tuple), s % (value, class_or_type_or_tuple, type(value))
    return value
