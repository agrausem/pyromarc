"""
"""

from pyromarc import format as format_


def reader(buffer, serializer, chunk_size=1024, **serializer_kwargs):
    serializer = _get_serializer(serializer, **serializer_kwargs)
    for element in serializer.load(buffer, chunk_size=chunk_size):
        yield element


def writer(buffer, mirs, serializer, **serializer_kwargs):
    serializer = _get_serializer(serializer, **serializer_kwargs)
    serializer.dump(buffer, mirs)


def _get_serializer(serializer, **kwargs):
    """
    Retrieve and initialize the serializer passed as arguments

    :param serializer: the serializer
    :type serializer: a string, a subclass of MARCSerializer or an instance of
    a subclass of MARCSerializer
    :param kwargs: parameters to instantiate the serializer
    :raises: ~pyromarc.format.UnrecognizedFormat when a bad serializer is
    passed

    >>> # from a string representing the format
    >>> import smc.bibencodings
    >>> serializer = _get_serializer('ISO2709', end_of_field=b'\x1e')
    >>> type(serializer)
    <class 'pyromarc.format.ISO2709'>
    >>> end_of_field = b'\x1e'.decode('mab2')
    >>> serializer.end_of_field == end_of_field
    True


    >>> # directly from a class subclassing MARCSerializer
    >>> from pyromarc.format import ISO2709
    >>> serializer = _get_serializer(ISO2709, end_of_subfield=b'\x1e')
    >>> end_of_subfield = b'\x1e'.decode('mab2')
    >>> end_of_subfield == serializer.end_of_subfield
    True

    >>> # directly from an instance
    >>> serializer = ISO2709()
    >>> _get_serializer(serializer) #doctest: +ELLIPSIS
    <pyromarc.format.ISO2709 object at 0x...>

    >>> # unrecognized format
    >>> serializer = _get_serializer('MARCXML')
    Traceback (most recent call last):
        ...
    pyromarc.format.UnrecognizedFormat: 'MARCXML' is not a valid format.

    """
    if isinstance(serializer, str):
        try:
            return getattr(format_, serializer)(**kwargs)
        except AttributeError:
            raise format_.UnrecognizedFormat(serializer)
    elif isinstance(serializer, format_.MARCSerializer):
        return serializer
    elif issubclass(serializer, format_.MARCSerializer):
        return serializer(**kwargs)
    raise format_.UnrecognizedFormat(serializer)
