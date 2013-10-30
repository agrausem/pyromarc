import unittest
import os
import json
from pyromarc.core import MIR
import pprint


class TestIso2709(unittest.TestCase):
    """
    """

    def setUp(self):
        path = os.path.dirname(__file__)
        with open(os.path.join(path, 'data/example.iso2709'), 'r+b') as example:
            self.data = example.read().split(b'\x1d')


    def test_parsing(self):
        for index, record_data in enumerate(self.data):
            try:
                record = MIR(record_data)
            except:
                print('Index : %s\n' % index)
                print(record_data)
                raise
            self.assertIn('200', record.tags)
            pprint.pprint(record)
