import unittest
import os
from pyromarc import reader


class TestIso2709(unittest.TestCase):
    """
    """

    def setUp(self):
        path = 'data/example.iso2709'
        self.path = os.path.join(os.path.dirname(__file__), path)
        with open(self.path, 'r+b') as example:
            self.data = example.read().split(b'\x1d')[:-1]


    def test_read(self):
        records = list(reader(self.path, 'ISO2709', chunk_size=1024))
        self.assertEqual(len(list(records)), len(self.data))


    def test_parsing(self):
        for index, mir in enumerate(reader(self.path, 'ISO2709')):
            self.assertIn('200', mir.tags)
