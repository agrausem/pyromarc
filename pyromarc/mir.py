""" The implementation of the MARC:MIR specification. This module handles
in-memory representation of a MARC record
"""


class MIR(list):
    """ MARC Internal Representation
    """

    def __init__(self, leader, fields):
        """
        :param leader: record's leader (24 characters) 
        :type leader: str
        :param fields: record's fields
        :type fields: list of ~pyromarc.mir.Field 
        """
        list.__init__(self)
        self.append(leader)
        if isinstance(fields[0], Field):
            self.extend(fields)
        else:
            for field in fields:
                if len(field) == 2:
                    pyrofield = Field(field[0], value=field[1])
                else:
                    pyrofield = Field(field[0], 
                                      subfields=field[1],
                                      indicators=field[2])
                self.append(pyrofield)

    @property
    def tags(self):
        """ All record field tags

        :rtype: generator of string
        """
        return (field.tag for field in self.fields)

    @property
    def leader(self):
        """ Record's leader
        """
        return self[0]

    @property
    def fields(self):
        """ Record's fields
        """
        return self[1:]

    def field(self, tag):
        """ Get first record's field with specified tag
        
        :param tag: the tag to search in fields
        :type tag: str
        :return: a field
        :rtype: ~pyromarc.mir.Field
        :raises: ValueError when tag does not exist
        """
        return self[self.index(tag)]


class BaseField(list):
    """ Base class for record's field and subfield
    """

    def __init__(self, tag):
        list.__init__(self)
        self.append(tag)

    @property
    def tag(self):
        """ Tag of the field
        """
        return self[0]

    def __str__(self):
        return self.tag

    def __eq__(self, field):
        if isinstance(field, str):
            return self.tag == field
        elif isinstance(field, self.__class__):
            return field.tag == self.tag
        return False


class Field(BaseField):
    """ A field that has subfields or is a control field
    """

    def __init__(self, tag, value='', indicators=None, subfields=None):
        """
        :param tag: field's tag
        :type tag: str
        :param value: field's value
        :type value: str
        :param indicators: field's indicators
        :type indicators: list
        :param subfields: field's subfields
        :type subfields: list of ~pyromarc.mir.SubField
        """
        super(Field, self).__init__(tag)
        if value:
            self.append(value)
        if subfields is not None:
            if isinstance(subfields[0], SubField):
                self.append(subfields)
            else:
                self.append([SubField(tag, value) for tag, value in subfields])
        if indicators is not None:
            self.append(indicators)

    @property
    def value(self):
        """ Value of the field if the field is a control field

        :rtype: str if value exists else None
        """
        if self.is_control():
            return self[1]

    @property
    def indicators(self):
        """ Indicators of the field if it's not a control field

        :rtype: a list or None
        """
        return self[2] if not self.is_control() else None

    def is_control(self):
        """ The field is a control field

        :rtype: bool
        """
        return not isinstance(self[1], list) and len(self) == 2

    @property
    def subfields(self):
        """ Subfields the field it is not a control field 

        :rtype: list of ~pyromarc.mir.Subfield or None
        """
        if not self.is_control():
            return self[1]

    def subfield(self, tag):
        """ Get first field's subfield with specified tag
        
        :param tag: the tag to search in fields
        :type tag: str
        :return: a field
        :rtype: ~pyromarc.mir.SubField
        :raises: ValueError when tag does not exist
        """
        if self.subfields:
            return self.subfields[self.subfields.index(tag)]


class SubField(BaseField):
    """ Subfield of a field
    """

    def __init__(self, tag, value):
        """
        :param tag: subfield's tag
        :type tag: str
        :param value: subfield's value
        :type value: str
        """
        super(SubField, self).__init__(tag)
        self.append(value)

    @property
    def value(self):
        """ Subfield's value
        """
        return self[1]
