import re
import smc.bibencodings
from .utils import chunkify
from .mir import MIR, Field, SubField


class MARCSerializer(object):
    """
    """

    def load(self, buffer, **kwargs):
        raise NotImplementedError()

    def dump(self, buffer, mirs):
        raise NotImplementedError()


class ISO2709(MARCSerializer):
    """ ISO2709 format
    """

    def __init__(self, end_of_record=b'\x1d', end_of_field=b'\x1e',
            end_of_subfield=b'\x1f', chunk_size=1024, encoding='mab2'):
        self.chunk_size = chunk_size
        self.encoding = encoding
        self.end_of_record = self._decode(end_of_record)
        self.end_of_field = self._decode(end_of_field)
        self.end_of_subfield = self._decode(end_of_subfield)
        self.subfield_parser = re.compile(self.end_of_subfield + '(.)')

    def _decode(self, value):
        return value.decode(self.encoding)

    def _encode(self, value):
        return value.encode(self.encoding)

    def _read(self, buffer):
        return self._decode(buffer.read(self.chunk_size))

    def _write(self, buffer, value):
        buffer.write(self._encode(value))

    def load(self, buffer):
        chunk = self._read(buffer)
        while chunk:
            if self.end_of_record in chunk:
                record, _, chunk = chunk.partition(self.end_of_record)
                leader, fields = self._parse(record)
                yield MIR(leader, fields)
                if not chunk:
                    chunk = self._read(buffer)
            else:
                chunk += self._read(buffer)

    def _parse(self, record):
        head, *raw_fields = record[:-1].split(self.end_of_field)

        head_length = len(head)
        if head_length < 24 or head_length % 12 != 0:
            raise BadHeaderException(head)

        leader = head[:24]

        fields = []
        for name, value in zip(chunkify(head[24:], 3, slicing=12), raw_fields):
            chunks = self.subfield_parser.split(value)
            if len(chunks) == 1:
                field = Field(name, value=value)
            else:
                indicators = list(chunks.pop(0))
                subfields = [SubField(name, value) for name, value in
                        chunkify(chunks, 2)]
                field = Field(name, indicators=indicators, subfields=subfields)
            fields.append(field)

        return leader, fields
        
    def dump(self, buffer, mirs):
        field_format = lambda field: '{0.tag}{0.value}'.format(field)
        for mir in mirs:
            header = mir.leader
            header += ''.join('{:.<12}'.format(tag) for tag in mir.tags)
            self._write(buffer, header)
            self._write(buffer, self.end_of_field)
            for field in mir.fields:
                if field.is_control():
                    self._write(buffer, field.value)
                else:
                    self._write(buffer, ''.join(field.indicators))
                    self._write(buffer, self.end_of_subfield)
                    subfield = self.end_of_subfield.join(
                        field_format(subfield) for subfield in field.subfields)
                    self._write(buffer, subfield)
                self._write(buffer, self.end_of_field)
            self._write(buffer, self.end_of_record)


class MsgPack(MARCSerializer):
    """ msgpack format
    """

    def load(self, buffer, **kwargs):
        from msgpack import Unpacker

        for record in Unpacker(buffer, encoding='utf-8'):
            fields = []
            for field in record[1:]:
                if isinstance(field[1], list):
                    subfields = [SubField(name, value) for name, value
                            in field[1]]
                    fields.append(Field(field[0], subfields=subfields,
                        indicators=field[2]))
                else:
                    fields.append(Field(field[0], value=field[1]))
            yield MIR(record[0], fields)


    def dump(self, buffer, mirs):
        from msgpack import packb
        for mir in mirs:
            buffer.write(packb(mir, use_bin_type=True))


class BadHeaderException(Exception):
    """ Header does not match the MARC standard
    """

    def __init__(self, header, *args, **kwargs):
        super(BadHeaderException, self).__init__(*args, **kwargs)
        self.header = header

    def __str__(self):
        return '{} is not a valid header'.format(self.header)


class UnrecognizedFormat(Exception):
    """ The serializing format is not handled by pyromarc
    """

    def __init__(self, serializer, *args, **kwargs):
        super(UnrecognizedFormat, self).__init__(*args, **kwargs)
        self.serializer = repr(serializer)

    def __str__(self):
        return '{} is not a valid format.'.format(self.serializer)
