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
        self.end_of_record = end_of_record.decode('mab2')
        self.end_of_field = end_of_field.decode('mab2')
        self.end_of_subfield = end_of_subfield.decode('mab2')
        self.subfield_parser = re.compile(self.end_of_subfield + '(.)')

    def load(self, filepath, chunk_size=1024):
        with open(filepath, 'rb') as file_handler:
            chunk = file_handler.read(chunk_size).decode('mab2')
            while chunk:
                if self.end_of_record in chunk:
                    record, _, chunk = chunk.partition(self.end_of_record)
                    leader, fields = self._parse(record)
                    yield MIR(leader, fields)
                    if not chunk:
                        chunk = file_handler.read(chunk_size).decode('mab2')
                else:
                    chunk += file_handler.read(chunk_size).decode('mab2')


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
                indicators = chunks.pop(0)
                subfields = [SubField(name, value) for name, value in
                        chunkify(chunks, 2)]
                field = Field(name, indicators=indicators, subfields=subfields)
            fields.append(field)

        return leader, fields
        

    def dump(self, filepath, mir):
        pass


class BadHeaderException(Exception):

    def __init__(self, header, *args, **kwargs):
        super(BadHeaderException, self).__init__(*args, **kwargs)
        self.header = header

    def __str__(self):
        return '{} is not a valid header'.format(self.header)


class UnrecognizedFormat(Exception):

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
