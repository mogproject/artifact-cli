def assert_type(value, class_or_type_or_tuple):
    s = "Return type of %r is not %r but %s."
    assert isinstance(value, class_or_type_or_tuple), s % (value, class_or_type_or_tuple, type(value))
    return value