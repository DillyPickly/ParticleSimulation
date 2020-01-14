class Create:

    def __init__(self, kind, max_bonds):
        self.kind = kind
        self.max_bonds = max_bonds
        self.bonds = []

    def full(self):
        if len(self.bonds) >= self.max_bonds:
            return True
        else:
            return False

    def n_empty(self):
        return self.max_bonds - len(self.bonds)

    def join(self, molecule):
        if self.full():
            return

        self.bonds.append(molecule)
        molecule.bonds.append(self)

        return

    def __repr__(self):
        return "[{}:{}]".format(self.kind, len(self.bonds))
