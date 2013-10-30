import unittest
import os
import json
from pyromarc.core import MIR
from pyromarc.core import Iso2709Reader


class TestIso2709(unittest.TestCase):
    """
    """

    def setUp(self):
        path = os.path.dirname(__file__)
        with open(os.path.join(path, 'data/example.iso2709'), 'r+b') as example:
            self.data = example.read().split(b'\x1d')


    def test_read(self):
        filepath = os.path.join(
            os.path.dirname(__file__), 'data', 'example.iso2709')
        records = Iso2709Reader(filepath)
        self.assertEqual(len(list(records)), 1190)


    def test_parsing(self):
        for index, record_data in enumerate(self.data):
            try:
                record = MIR(record_data)
            except:
                print('Index : %s\n' % index)
                print(record_data)
                raise
            self.assertIn('200', record.tags)
            print(record_data)
            json.dumps(record)
