import unittest
import os
from io import BytesIO
from pyromarc import reader
from pyromarc.format import MsgPack


class TestIso2709(unittest.TestCase):
    """
    """

    def setUp(self):
        path = 'data/example.iso2709'
        self.path = os.path.join(os.path.dirname(__file__), path)


    def test_read(self):
        with open(self.path, 'r+b') as example:
            data = example.read().split(b'\x1d')[:-1]
        with open(self.path, 'r+b') as buffer:
            records = list(reader(buffer, 'ISO2709', chunk_size=1024))
        self.assertEqual(len(list(records)), len(data))


    def test_parsing(self):
        with open(self.path, 'r+b') as buffer:
            for index, mir in enumerate(reader(buffer, 'ISO2709')):
                self.assertIn('200', mir.tags)


    def test_msgpack(self):
        with open(self.path, 'r+b') as buffer:
            records = list(reader(buffer, 'ISO2709', chunk_size=1024))[0:5]

        buf = BytesIO()

        serializer = MsgPack()
        serializer.dump(buf, records)

        buf.seek(0)
        mirs = list(serializer.load(buf))
        self.assertEqual(records, mirs)


