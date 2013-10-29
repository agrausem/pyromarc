import unittest
import os
import json
from pyromarc.core import Iso2709


class TestIso2709(unittest.TestCase):
    """
    """

    def setUp(self):
        path = os.path.dirname(__file__)
        with open(os.path.join(path, 'data/example.iso2709'), 'r+b') as example:
            self.data = example.read().split(b'\x1d')


    def test_parsing(self):
        for record_data in self.data:
            record = Iso2709(record_data)
            self.assertIn('200', record.tags)
            print(record_data)
            json.dumps(record)
