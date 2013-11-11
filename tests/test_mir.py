import os
import unittest

from pyromarc import reader
from pyromarc.mir import Field
from pyromarc.mir import SubField


class TestMir(unittest.TestCase):
    """
    """

    def setUp(self):
        path = os.path.join('data', 'record.iso2709')
        self.mir = list(reader(os.path.join(os.path.dirname(__file__), path),
                          'ISO2709'))[0]

    def test_mir_leader(self): 
        self.assertEqual(self.mir.leader, " 1560cam0 2200469   450 ")

    def test_mir_tags(self):
        expected = set(["001", "003", "005", "035", "100", "101", "102", "105",
                "106", "200", "205", "210", "215", "225", "320", "410", "606",
                "676", "680", "700", "801", "930"])
        self.assertSetEqual(set(self.mir.tags), expected)

        self.assertEqual(len([tag for tag in self.mir.tags if tag == '035']),
                         9)

    def test_mir_fields(self):
        self.assertEqual(len(self.mir.fields), 37)


    def test_from_tag(self):
        self.assertEqual(self.mir.field("001"),
                         Field("001", value="002117770"))
        subfields = [SubField("a", "021020922"), SubField("9", "sudoc")],
        self.assertEqual(self.mir.field("035"), Field("035",
                                                      subfields=subfields,
                                                      indicators=[" ", " "]))

    def test_from_absent_tag(self):
        with self.assertRaises(ValueError):
            self.mir.field("002")
    

    def test_field_with_value(self):
        field = self.mir.fields[0]
        self.assertTrue(field.is_control())
        self.assertEqual(field.value, "002117770")
        self.assertIsNone(field.subfields)
        self.assertIsNone(field.indicators)

    def test_field_with_subfields(self):
        field = self.mir.field("035")
        self.assertFalse(field.is_control())
        subfields = [SubField("a", "021020922"), SubField("9", "sudoc")]
        self.assertEqual(len(field.subfields), 2)
        self.assertListEqual(field.subfields, subfields)
        self.assertIsNone(field.value)
        self.assertListEqual(field.indicators, [" ",  " "])

    def test_subfield_from_tag(self):
        field = self.mir.field("035")
        self.assertEqual(field.subfield("a"), SubField("a", "021020922"))

    def test_from_absent_subfield(self):
        field = self.mir.field("035")
        with self.assertRaises(ValueError):
            field.subfield("b")
        
    def test_field_representation(self):
        self.assertEqual(str(self.mir.fields[0]), "001")

    def test_field_equality_with_tag(self):
        field = self.mir.fields[3]
        self.assertTrue(field == "035")

    def test_field_equality_with_field(self):
        field = self.mir.fields[3]
        field2 = Field("035")
        self.assertTrue(field == field2)

    def test_field_difference_with_tag(self):
        field = self.mir.fields[3]
        self.assertFalse(field == "100")

    def test_field_difference_with_field(self):
        field = self.mir.fields[3]
        field2 = Field("100")
        self.assertFalse(field == field2)

    def test_field_difference_with_bad_type(self):
        field = self.mir.fields[3]
        self.assertFalse(field == 35)
