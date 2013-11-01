"""
"""

from . import format as format_


def reader(filepath, serializer, chunk_size=1024, **serializer_kwargs):
    serializer = _get_serializer(serializer, **serializer_kwargs)
    for element in serializer.load(filepath, chunk_size=chunk_size):
        yield element


def writer(filepath, mir):
    pass


def _get_serializer(serializer, **kwargs):
    if isinstance(serializer, str):
        try:
            return getattr(format_, serializer)(**kwargs)
        except AttributeError:
            raise format_.UnrecognizedFormat(serializer)
    elif issubclass(serializer, format_.MARCSerializer):
        return serializer(**kwargs)
    elif isinstance(serializer, format._MARCSerializer):
        return serializer
    raise format_.UnrecognizedFormat(serializer)
