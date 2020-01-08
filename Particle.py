class Create:
    def __init__(self, moleculesA, moleculesB, location):
        self.location = location
        self.moleculesB = []
        self.moleculesA = []

        if moleculesA is not None:
            try:
                self.moleculesA = [m for m in moleculesA]
            except TypeError:
                self.moleculesA = [moleculesA]

        if moleculesB is not None:
            try:
                self.moleculesB = [m for m in moleculesB]
            except TypeError:
                self.moleculesB = [moleculesB]

    def join(self, particle):

        if self.location != particle.location:
            return ArithmeticError

        for m in particle.moleculesA:
            self.moleculesA.append(m)

        for m in particle.moleculesB:
            self.moleculesB.append(m)

    def move(self, new_location):
        self.location = new_location

    def __repr__(self):
        # return "location: {}, \nmoleculesA: {}, \nmoleculesB: {}"\
        #     .format( self.location, self.moleculesA, self.moleculesB)

        return "{}{}"\
            .format(self.moleculesA, self.moleculesB)
