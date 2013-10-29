import re
from .utils import chunkify
from . import END_OF_RECORD, END_OF_FIELD, END_OF_SUBFIELD


class Iso2709Reader(object):
    def __init__(self, filepath, **kwargs):
        self.filepath = filepath
        self.chunk_size = kwargs.get('chunk_size', 1024)

    def __iter__(self):
        with open(self.filepath, 'rb') as fhandler:
            record = b''

            cur_bytes = fhandler.read(self.chunk_size)
            while cur_bytes:
                if END_OF_RECORD in cur_bytes:
                    cur_records = cur_bytes.split(END_OF_RECORD)
                    record += cur_records.pop(0)
                    yield record
                    for r in cur_records[:-1]:
                        yield r
                    record = cur_records[-1] if cur_records else b''
                cur_bytes = fhandler.read(self.chunk_size)


class Iso2709(list):
    """
    """

    def __init__(self, raw, end_of_field=END_OF_FIELD):
        """
        """
        list.__init__(self)
        head, *fields = raw[:-1].split(end_of_field)

        if not head:
            raise Exception('No record')

        if not fields:
            raise Exception('No fields')

        head_length = len(head)
        if head_length < 24 or head_length % 12 != 0:
            raise Exception('Bad format for head: %s' % head)

        leader = head[:24].decode('utf-8')
        self.append(leader)
        self.extend([Field(name, value) for name, value in
                zip(chunkify(head[24:], 3, slicing=12), fields)])


    def __repr__(self):
        return '<Iso2709: %s>' % self.leader

    @property
    def tags(self):
        return [field[0] for field in self[1:]]

    @property
    def leader(self):
        return self[0]

    @property
    def fields(self):
        return self[1:]

    def field(self, tag):
        return self[self.index(tag)]


class Field(list):
    """
    """

    def __init__(self, name, value, end_of_subfield=END_OF_SUBFIELD):
        """
        """
        list.__init__(self)
        self.append(name.decode('utf-8'))
        chunks = re.split(b'\x1f(.)', value)
        if len(chunks) == 1:
            self.append(value)
            self.append('')
        else:
            indicators = chunks.pop(0).decode('utf-8')
            self.extend([Field(name, value, end_of_subfield) for name, value
                in chunkify(chunks, 2)])
            self.append(indicators)

    @property
    def name(self):
        return self[0]

    @property
    def value(self):
        return self[1]

    @property
    def indicators(self):
        return self[2]

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

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
