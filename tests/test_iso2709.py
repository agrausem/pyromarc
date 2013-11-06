import unittest
import os
from pyromarc import reader


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
            records = list(reader(buffer, 'ISO2709'))
        self.assertEqual(len(list(records)), len(data))


    def test_parsing(self):
        with open(self.path, 'r+b') as buffer:
            for index, mir in enumerate(reader(buffer, 'ISO2709')):
                self.assertIn('200', mir.tags)
