import re
import smc.bibencodings
import json
import msgpack
from .utils import chunkify
from .mir import MIR, Field, SubField


class MARCSerializer(object):
    """
    """

    binary_mode = False

    def load(self, buffer):
        raise NotImplementedError()

    def _deserialize(self, callable, *args, **kwargs):
        for leader, *fields in callable(*args, **kwargs):
            yield MIR(leader, fields)

    def dump(self, buffer, mirs):
        raise NotImplementedError()


class ISO2709(MARCSerializer):
    """ ISO2709 format
    """

    binary_mode = True

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
            header = self._format_header(mir)
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

    def _format_header(self, mir):
        length_format = lambda field_length: '{:0<4}'.format(field_length)
        address_format = lambda position: '{:0<5}'.format(position)
        position = 0    
        header = mir.leader

        for field in mir.fields:
            header += field.tag
            if field.is_control():
                field_length = len(field.value) + 1
            else:
                lindicators = len(field.indicators)
                lsubfields = sum([len(sub.tag) + len(sub.value) for sub in
                    field.subfields])
                field_length = lindicators + lsubfields + 1
            header += length_format(field_length)
            header += address_format(position)
            position += field_length

        return header


class MsgPack(MARCSerializer):
    """ msgpack format
    """

    binary_mode = True
    
    def load(self, buffer):
        return self._deserialize(msgpack.Unpacker, buffer, encoding='utf-8')

    def dump(self, buffer, mirs):
        for mir in mirs:
            buffer.write(msgpack.packb(mir, use_bin_type=True))


class Json(MARCSerializer):
    """ json format
    """

    def __init__(self, indent=None):
        self.indent = indent

    def load(self, buffer):
        return self._deserialize(json.load, buffer)

    def dump(self, buffer, mirs):
        mirs = list(mirs)
        for chunk in json.JSONEncoder(indent=self.indent).iterencode(mirs):
            buffer.write(chunk)


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


class BadIOMode(Exception):
    """ File handler has a bad opening mode
    """

    def __init__(self, serializer, open_mode, *args, **kwargs):
        super(BadIOMode, self).__init__(*args, **kwargs)
        self.serializer = serializer.__class__.__name__
        self.open_mode = open_mode

    def __str__(self):
        return 'Bad opening mode {0.open_mode} for {0.serializer}'.format(self)
