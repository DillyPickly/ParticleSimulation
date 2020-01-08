class Create:

    def __init__(self, kind, bonds):
        self.kind = kind
        self.bonds = bonds

    # def __init__(self, kind):
    #     self.kind = kind
    #     self.bonds = 6

    def __repr__(self):
        return "[{}:{}]".format(self.kind, self.bonds)
