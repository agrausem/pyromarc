"""
"""

from pyromarc import format as format_


def reader(buffer, serializer, **serializer_kwargs):
    serializer = _get_serializer(serializer, **serializer_kwargs)
    for element in serializer.load(buffer):
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
