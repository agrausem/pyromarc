"""
"""

import unittest

from pyromarc import _get_serializer
from pyromarc import format as format_


class TestSerializerFactory(unittest.TestCase):

    def test_from_string(self):
        serializer = _get_serializer('ISO2709', chunk_size=2048)
        self.assertIsInstance(serializer, format_.ISO2709)
        self.assertEquals(serializer.chunk_size, 2048)

        serializer = _get_serializer('MsgPack')
        self.assertIsInstance(serializer, format_.MsgPack)

    def test_from_class(self):
        serializer = _get_serializer(format_.ISO2709, encoding='utf-8')
        self.assertIsInstance(serializer, format_.ISO2709)
        self.assertEqual(serializer.encoding, 'utf-8')

    def test_from_instance(self):
        serializer = _get_serializer(format_.MsgPack())
        self.assertIsInstance(serializer, format_.MsgPack)

    def test_bad_from_string(self):
        with self.assertRaises(format_.UnrecognizedFormat) as cm:
            serializer = _get_serializer('MARCXML')

        error = cm.exception
        self.assertEqual(str(error), "'MARCXML' is not a valid format.")

    def test_bad_class(self):
        from json import JSONDecoder

        with self.assertRaises(format_.UnrecognizedFormat) as cm:
            serializer = _get_serializer(JSONDecoder)

        error = cm.exception
        self.assertEqual(str(error), "<class 'json.decoder.JSONDecoder'> is "
        "not a valid format.")
