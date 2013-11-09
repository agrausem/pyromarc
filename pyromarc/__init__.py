"""
"""

from pyromarc import format as format_


def reader(filepath, serializer, **serializer_kwargs):
    """ Read records from a filepath given a serializer

    :param filepath: path to the file containing records
    :type filepath: string
    :param serializer: the serializer to deserialize records
    :type serializer: see :py:func:"~pyromarc._get_serializer"
    :return: :py:class:~pyromarc.mir.MIR objects
    :rtype: generator
    """
    serializer = _get_serializer(serializer, **serializer_kwargs)
    read_mode = 'rb+' if serializer.binary_mode else 'r+' 
    with open(filepath, read_mode) as fhandler:
        for element in serializer.load(fhandler):
            yield element


def readerb(fhandler, serializer, **serializer_kwargs):
    """ Read records from a file handler given a serializer

    :param fhandler: a file handler
    :type fhandler: ~io.BufferedReader or ~io.TextWrapperReader
    :param serializer: the serializer to deserialize records
    :type serializer: see :py:func:"~pyromarc._get_serializer"
    :return: :py:class:~pyromarc.mir.MIR objects
    :rtype: generator
    """
    serializer = _get_serializer(serializer, **serializer_kwargs)
    if serializer.binary_mode:
        fhandler = fhandler.buffer if not 'b' in fhandler.mode  else fhandler
    elif 'b' in fhandler.mode:
        raise format_.BadIOMode(serializer, fhandler.mode)
    for element in serializer.load(fhandler):
        yield element


def writer(filepath, mirs, serializer, **serializer_kwargs):
    """ Write records to a filepath given a serializer

    :param filepath: path to the file to write records
    :type filepath: string
    :param serializer: the serializer to serialize records
    :type serializer: see :py:func:"~pyromarc._get_serializer"
    :return: :py:class:~pyromarc.mir.MIR objects
    :rtype: generator
    """
    serializer = _get_serializer(serializer, **serializer_kwargs)
    write_mode = 'w+b' if serializer.binary_mode else 'w+' 
    with open(filepath, write_mode) as fhandler:
        serializer.dump(fhandler, mirs)


def writerb(fhandler, mirs, serializer, **serializer_kwargs):
    """ Write records to a file handler given a serializer

    :param fhandler: file handler to write records
    :type fhandler: ~io.BufferedWriter or ~io.TextWrapperWriter
    :param serializer: the serializer to serialize records
    :type serializer: see :py:func:"~pyromarc._get_serializer"
    :return: :py:class:~pyromarc.mir.MIR objects
    :rtype: generator
    """
    serializer = _get_serializer(serializer, **serializer_kwargs)
    if serializer.binary_mode:
        fhandler = fhandler.buffer if not 'b' in fhandler.mode  else fhandler
    elif 'b' in fhandler.mode:
        raise format_.BadIOMode(serializer, serializer)
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
