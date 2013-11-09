from itertools import islice
import io
import os
import unittest
from pyromarc import reader, readerb
from pyromarc.format import BadIOMode
from pyromarc.mir import MIR


class TestReader(unittest.TestCase):
    """
    """

    def setUp(self):
        iso2709path = os.path.join('data', 'example.iso2709')
        jsonpath = os.path.join('data', 'example.json')
        self.iso2709path = os.path.join(os.path.dirname(__file__), iso2709path)
        self.jsonpath = os.path.join(os.path.dirname(__file__), jsonpath)
        self.take = lambda n, iterable: list(islice(iterable, n))

    def test_reader_rb(self):
        mirs = self.take(5, reader(self.iso2709path, 'ISO2709'))
        self.assertTrue(all([isinstance(mir, MIR) for mir in mirs]))

    def test_readerb_rb(self):
        for open_mode in ('r+', 'rb+'):
            with open(self.iso2709path, open_mode) as fhandler:
                mirs = self.take(5, readerb(fhandler, 'ISO2709'))
                self.assertTrue(all([isinstance(mir, MIR) for mir in mirs]))

    def test_reader_r(self):
        mirs = list(reader(self.jsonpath, 'Json'))
        self.assertTrue(all([isinstance(mir, MIR) for mir in mirs]))
        
    def test_readerb_r(self):
        with open(self.jsonpath, 'r+') as fhandler:
            mirs = readerb(fhandler, 'Json')
            self.assertTrue(all([isinstance(mir, MIR) for mir in mirs]))

        with open(self.jsonpath, 'rb+') as fhandler:
            with self.assertRaises(BadIOMode) as cm:
                self.take(5, readerb(fhandler, 'Json'))

            error = cm.exception
            expected = 'Bad opening mode rb+ for Json'
            self.assertEqual(str(error), expected) 
