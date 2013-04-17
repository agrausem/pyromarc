
def chunkify(iterable, per_chunk, slicing=None):
    """
    """
    if slicing is None:
        slicing = per_chunk
    for index in range(0, len(iterable), slicing):
        yield iterable[index:index + per_chunk]
