import re
import smc.bibencodings
from .utils import chunkify
from .mir import MIR, Field, SubField


class MARCSerializer(object):
    """
    """

    def load(self, filepath, chunk_size):
        raise NotImplementedError()

    def dump(self, filepath, mir):
        raise NotImplementedError()


class ISO2709(MARCSerializer):
    """
    """

    def __init__(self, end_of_record=b'\x1d', end_of_field=b'\x1e',
            end_of_subfield=b'\x1f'):
        self.end_of_record = end_of_record
        self.end_of_field = end_of_field
        self.end_of_subfield = end_of_subfield
        self.subfield_parser = re.compile(self.end_of_subfield + b'(.)')

    def load(self, filepath, chunk_size=1024):
        with open(filepath, 'rb') as file_handler:
            chunk = file_handler.read(chunk_size)
            while chunk:
                if self.end_of_record in chunk:
                    record, _, chunk = chunk.partition(self.end_of_record)
                    leader, fields = self._parse(record)
                    yield MIR(leader, fields)
                    if not chunk:
                        chunk = file_handler.read(chunk_size)
                else:
                    chunk += file_handler.read(chunk_size)

    def _decode(self, *strings):
        if len(strings) == 1:
            return strings[0].decode('mab2')
        return [string.decode('mab2') for string in strings]

    def _parse(self, record):
        head, *raw_fields = record[:-1].split(self.end_of_field)

        head_length = len(head)
        if head_length < 24 or head_length % 12 != 0:
            raise BadHeaderException(head)

        leader = self._decode(head[:24])

        fields = []
        for name, value in zip(chunkify(head[24:], 3, slicing=12), raw_fields):
            chunks = self.subfield_parser.split(value)
            if len(chunks) == 1:
                name, value = self._decode(name, value)
                fields.append(Field(name, value=value))
            else:
                subfields = []
                indicators = self._decode(chunks.pop(0))
                for sub_name, sub_value in chunkify(chunks, 2):
                    sub_name, sub_value = self._decode(sub_name, sub_value)
                    subfields.append(SubField(sub_name, sub_value))
                name = self._decode(name)
                fields.append(Field(name,
                                    indicators=indicators,
                                    subfields=subfields
                                    ))
        return leader, fields
        

    def dump(self, filepath, mir):
        pass


class BadHeaderException(Exception):

    def __init__(self, header, *args, **kwargs):
        super(BadHeaderException, self).__init__(*args, **kwargs)
        self.header = header

    def __str__(self):
        return '{} is not a valid header'.format(self.header)


def UnrecognizedFormat(Exception):

    def __init__(self, serializer, *args, **kwargs):
        super(UnrecognizedFormat, self).__init__(*args, **kwargs)
        self.serializer = repr(serializer)

    def _format_available(self):
        return [format_ for format_ in dir(__import__(__name__))
                if issubclass(format_, MARCSerializer)]

    def __str__(self):
        return '{} is not a valid format. Formats available are {} :\n'.format(
                self.serializer,
                '\n'.join(self_format_available()))
