from io import BytesIO
from itertools import islice
import unittest
import os

from pyromarc import reader
from pyromarc.format import MsgPack


class TestMsgPack(unittest.TestCase):

    def setUp(self):
        path = 'data/example.iso2709'
        self.path = os.path.join(os.path.dirname(__file__), path)
        self.serializer = MsgPack()

    def test_symmetrical(self):
        take = lambda n, iterable: list(islice(iterable, n))

        with open(self.path, 'r+b') as buffer:
            records = take(5, reader(buffer, 'ISO2709'))

        buffer = BytesIO()
        self.serializer.dump(buffer, records)

        buffer.seek(0)
        mirs = list(self.serializer.load(buffer))
        self.assertEqual(records, mirs)
