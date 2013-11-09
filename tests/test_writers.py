from itertools import islice
import io
import os
import unittest
from pyromarc import reader, readerb, writer, writerb
from pyromarc.format import BadIOMode
from pyromarc.mir import MIR


class TestWriter(unittest.TestCase):
    """
    """

    def setUp(self):
        iso2709path = os.path.join('data', 'example.iso2709')
        self.iso2709path = os.path.join(os.path.dirname(__file__), iso2709path)
        self.take = lambda n, iterable: list(islice(iterable, n))
        self.mirs = self.take(5, reader(self.iso2709path, 'ISO2709'))
        self.fhandlerb = io.BufferedWriter(io.FileIO("buffer", "wb"))
        self.rfhandlerb = io.BufferedReader(io.FileIO("buffer", "rb+"))
        self.fhandler = io.TextIOWrapper(io.BufferedWriter(io.FileIO("file",
            "w+")))
        self.fhandler.mode = 'w'
        self.rfhandler = io.TextIOWrapper(io.BufferedReader(io.FileIO("file",
            "r+")))
        self.rfhandler.mode = 'r'

    def test_writer_rb(self):
        writer('/tmp/iso2709', self.mirs, 'ISO2709') 
        mirs = reader('/tmp/iso2709', 'ISO2709')
        self.assertTrue(all([isinstance(mir, MIR) for mir in mirs]))

    def test_writerb_rb(self):
        for io_type, io_rtype in zip( (self.fhandler, self.fhandlerb),
                (self.rfhandler, self.rfhandlerb)):
            writerb(io_type, self.mirs, 'ISO2709')
            io_type.seek(0)
            mirs = readerb(io_rtype, 'ISO2709')
            self.assertTrue(all([isinstance(mir, MIR) for mir in mirs]))

    def test_writer_r(self):
        writer('/tmp/json', self.mirs, 'Json')
        mirs = reader('/tmp/json', 'Json')
        self.assertTrue(all([isinstance(mir, MIR) for mir in mirs]))
        
    def test_writerb_r(self):
        writerb(self.fhandler, self.mirs, 'Json')
        self.fhandler.seek(0)
        mirs = readerb(self.rfhandler, 'Json')
        self.assertTrue(all([isinstance(mir, MIR) for mir in mirs]))

        with self.assertRaises(BadIOMode) as cm:
            print(self.fhandlerb.mode)
            writerb(self.fhandlerb, self.mirs, 'Json')

        error = cm.exception
        expected = 'Bad opening mode wb for Json'
        self.assertEqual(str(error), expected) 
