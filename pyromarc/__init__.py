"""
"""

from pyromarc import format as format_


def reader(filepath, serializer, **serializer_kwargs):
    serializer = _get_serializer(serializer, **serializer_kwargs)
    with open(filepath, serializer.read_mode) as fhandler:
        for element in serializer.load(fhandler):
            yield element


def readerb(fhandler, serializer, **serializer_kwargs):
    serializer = _get_serializer(serializer, **serializer_kwargs)
    if serializer.read_mode == 'rb':
        fhandler = fhandler.buffer
    for element in serializer.load(fhandler):
        yield element


def writer(filepath, mirs, serializer, **serializer_kwargs):
    serializer = _get_serializer(serializer, **serializer_kwargs)
    with open(filepath, serializer.write_mode) as fhandler:
        serializer.dump(fhandler, mirs)


def writerb(fhandler, mirs, serializer, **serializer_kwargs):
    serializer = _get_serializer(serializer, **serializer_kwargs)
    if serializer.write_mode == 'wb':
        fhandler = fhandler.buffer
    serializer.dump(fhandler, mirs)


def _get_serializer(serializer, **kwargs):
    """
    Retrieve and initialize the serializer passed as arguments

    :param serializer: the serializer
    :type serializer: a string, a subclass of MARCSerializer or an instance of
    a subclass of MARCSerializer
    :param kwargs: parameters to instantiate the serializer
    :raises: ~pyromarc.format.UnrecognizedFormat when a bad serializer is
    passed
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
