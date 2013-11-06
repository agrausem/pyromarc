"""
"""


class MIR(list):
    """
    """

    def __init__(self, leader, fields):
        """
        """
        list.__init__(self)
        self.append(leader)
        self.extend(fields)

    @property
    def tags(self):
        return (field.tag for field in self.fields)

    @property
    def leader(self):
        return self[0]

    @property
    def fields(self):
        return self[1:]

    def field(self, tag):
        return self[self.index(tag)]


class BaseField(list):
    """
    """

    def __init__(self, tag):
        list.__init__(self)
        self.append(tag)

    @property
    def tag(self):
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
    """
    """

    def __init__(self, tag, value='', indicators=None, subfields=None):
        """
        """
        super(Field, self).__init__(tag)
        if not subfields:
            self.append(value)
        else:
            self.append(subfields)
        if indicators:
            self.append(indicators)

    @property
    def value(self):
        if not self.has_subfields():
            return self[1]
        return None

    @property
    def indicators(self):
        return self[2] if not self.is_control() else None

    def is_control(self):
        return not self.has_subfields() and len(self) == 2

    def has_subfields(self):
        return isinstance(self.value, list)

    @property
    def subfields(self):
        if self.has_subfields():
            return [field.tag for field in self.value]
        return None

    def subfield(self, tag):
        try:
            return self.subfields[self.subfields.index(tag)]
        except IndexError:
            return None


class SubField(BaseField):
    """
    """

    def __init__(self, tag, value):
        super(SubField, self).__init__(tag)
        self.append(value)

    @property
    def value(self):
        return self[1]
