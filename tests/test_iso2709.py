from io import BytesIO
from itertools import islice
import os
import unittest

from pyromarc.format import ISO2709


class TestIso2709(unittest.TestCase):
    """
    """

    def setUp(self):
        path = 'data/example.iso2709'
        self.path = os.path.join(os.path.dirname(__file__), path)
        self.serializer = ISO2709()


    def test_read(self):
        with open(self.path, 'r+b') as example:
            data = example.read().split(b'\x1d')[:-1]
        with open(self.path, 'r+b') as buffer:
            records = list(self.serializer.load(buffer))
        self.assertEqual(len(list(records)), len(data))


    def test_structure(self):
        with open(self.path, 'r+b') as buffer:
            for mir in self.serializer.load(buffer):
                self.assertIsInstance(mir.leader, str)
                self.assertIsInstance(mir.fields, list)
                for field in mir.fields:
                    self.assertIsInstance(field.tag, str)
                    if len(field) == 2:
                        self.assertIsInstance(field.value, str)
                    else:
                        self.assertIsInstance(field.subfields, list)
                        self.assertIsInstance(field.indicators, list)
                        for subfield in field.subfields:
                            self.assertIsInstance(subfield.tag, str)
                            self.assertIsInstance(subfield.value, str)

    def test_symmetrical(self):
        take = lambda n, iterable: list(islice(iterable, n))

        with open(self.path, 'r+b') as buffer:
            records = take(5, self.serializer.load(buffer))

        buffer = BytesIO()
        self.serializer.dump(buffer, records)

        buffer.seek(0)
        mirs = list(self.serializer.load(buffer))
        self.assertEqual(records, mirs)
