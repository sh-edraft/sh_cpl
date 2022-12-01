class User:

    def __init__(self, name, address):
        self.name = name
        self.address = address

    def __repr__(self):
        return f'<{type(self).__name__} {self.name} {self.address}>'


class Address:

    def __init__(self, street, nr):
        self.street = street
        self.nr = nr

    def __repr__(self):
        return f'<{type(self).__name__} {self.street} {self.nr}>'
