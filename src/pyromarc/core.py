import re

def from_iso2709(raw):
    """
    """
    head, *fields = raw[:-1].split("\x1e")

    if not fields:
        raise Exception('No fields')

    head_length = len(head)
    if head_length < 24 or head_length % 12 != 0 or not head.isdigit():
        raise Exception('Bad format for head')

    leader, head = head[:24], head[24:]
    tags = chunkify(head, 3, slicing=12)
    return leader, zip(tags, map(_extract_subs, fields))


def _extract_subs(field):
    """
    """
    chunks = re.split("\x1f(.)", field)
    if len(chunks) == 1:
        return (chunks, )
    indicators = list(chunks.pop(0))
    subfields = chunkify(chunks, 2)
    return subfields, indicators


def chunkify(iterable, per_chunk, slicing=None):
    """
    """
    slicing = slicing if slicing is not None else per_chunk
    for index in range(0, len(iterable), slicing):
        yield iterable[index:index + per_chunk]


class Iso2709(object):
    """
    """

    def __init__(self, raw):
        """
        """
        head, *fields = raw[:-1].split("\x1e")

        if not fields:
            raise Exception('No fields')

        head_length = len(head)
        if head_length < 24 or head_length % 12 != 0 or not head.isdigit():
            raise Exception('Bad format for head')

        self.leader = head[:24]
        self.fields = [Field(name, value) for name, value in 
                zip(chunkify(head[24:], 3, slicing=12), fields)]


    def __repr__(self):
        return '<Iso2709: %s>' % self.leader

    @property
    def tags(self):
        return [field.name for field in self.fields]

    def field(self, tag):
        return self.fields[self.fields.index(tag)]


class Field(object):
    """
    """

    def __init__(self, name, value):
        """
        """
        self.name = name
        chunks = re.split("\x1f(.)", value)
        if len(chunks) == 1:
            self.value = value
            self.indicators = []
        else:
            self.indicators = list(chunks.pop(0))
            self.value = [Field(name, value) for name, value in
                    chunkify(chunks, 2)]

    def __eq__(self, field):
        if isinstance(field, str):
            return self.name == field
        elif isinstance(field, Field):
            return field.name == self.name

    def has_subfields(self):
        return isinstance(self.value, list)

    def subfields(self):
        if self.has_subfields():
            return [field.name for field in self.value]
        return []

    def subfield(self, tag):
        try:
            return self.subfields[self.subfields.index(tag)]
        except IndexError:
            return None

