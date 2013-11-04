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
        return [field.name for field in self.fields]

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

    def __init__(self, name):
        list.__init__(self)
        self.append(name)

    @property
    def name(self):
        return self[0]

    def __str__(self):
        return self.name

    def __eq__(self, field):
        if isinstance(field, str):
            return self.name == field
        elif isinstance(field, self.__class__):
            return field.name == self.name
        return False


class Field(BaseField):
    """
    """

    def __init__(self, name, value='', indicators=None, subfields=None):
        """
        """
        super(Field, self).__init__(name)
        if not subfields:
            self.append(value)
        else:
            self.append(subfields)
        self.append(indicators or [])

    @property
    def value(self):
        if not self.has_subfields():
            return self[1]
        return None

    @property
    def indicators(self):
        return self[2]

    def has_subfields(self):
        return isinstance(self.value, list)

    @property
    def subfields(self):
        if self.has_subfields():
            return [field.name for field in self.value]
        return None

    def subfield(self, tag):
        try:
            return self.subfields[self.subfields.index(tag)]
        except IndexError:
            return None


class SubField(BaseField):
    """
    """

    def __init__(self, name, value):
        super(SubField, self).__init__(name)
        self.append(value)
