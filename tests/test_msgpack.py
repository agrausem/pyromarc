import unittest
import os
from itertools import islice
from io import BytesIO
from pyromarc import reader
from pyromarc.format import MsgPack


class TestMsgPack(unittest.TestCase):

    
    def setUp(self):
        path = 'data/example.iso2709'
        self.path = os.path.join(os.path.dirname(__file__), path)


    def test_symetrical(self):
        take = lambda n, iterable: list(islice(iterable, n))

        with open(self.path, 'r+b') as buffer:
            records = take(5, reader(buffer, 'ISO2709'))

        buf = BytesIO()

        serializer = MsgPack()
        serializer.dump(buf, records)

        buf.seek(0)
        mirs = list(serializer.load(buf))
        self.assertEqual(records, mirs)
