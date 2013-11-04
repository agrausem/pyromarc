"""
pyromarc.utils
~~~~~~~~~~~~~~

Utility functions for the pyromarc library
"""


def chunkify(iterable, per_chunk, slicing=None):
    """
    Explodes an iterable into chunks

    :param iterable: an iterable
    :param per_chunk: length of the wanted chunks
    :type per_chunk: integer
    :param slicing: slicing for iterate an iterable
    :type slicing: integer

    >>> list(chunkify(range(0, 10), per_chunk=3))
    [range(0, 3), range(3, 6), range(6, 9), range(9, 10)]
    >>> list(chunkify(range(0, 10), per_chunk=3, slicing=4))
    [range(0, 3), range(4, 7), range(8, 10)]
    """
    if slicing is None:
        slicing = per_chunk
    for index in range(0, len(iterable), slicing):
        yield iterable[index:index + per_chunk]
