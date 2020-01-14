import queue
import Particle


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

        if self == particle:
            return

        for m in particle.moleculesA:
            self.moleculesA.append(m)

        for m in particle.moleculesB:
            self.moleculesB.append(m)

        # particle = self

    def move(self, new_location):
        self.location = new_location

    def split(self, molecule1, molecule2):

        molecule1.bonds.remove(molecule2)
        molecule2.bonds.remove(molecule1)

        # searched dictionary
        searched = [{}, {}]
        for m in self.moleculesA:
            searched[0][m] = False
            searched[1][m] = False
        for m in self.moleculesB:
            searched[0][m] = False
            searched[1][m] = False

        # molecules to search
        q = queue.Queue()
        q.put([molecule1, 0])
        q.put([molecule2, 1])

        while not q.empty():
            molecule, component = q.get()
            opposite_component = component ^ 1

            if searched[opposite_component][molecule]:
                # we have found a connection
                # so no need to stop and just remove the single bond

                return [self]

            elif searched[component][molecule]:
                # we already found this molecule in the current component
                # this means we just continue to the next iteration

                continue

            else:
                # this means that we need to add the new molecule to the queue
                searched[component][molecule] = True
                for m in molecule.bonds:
                    q.put([m, component])

        # we now know that we have separate components
        p0 = Particle.Create(None, None, self.location)
        p1 = Particle.Create(None, None, self.location)

        for m in searched[0]:
            if searched[0][m]:

                if m.kind == 'A':
                    p0.moleculesA.append(m)

                elif m.kind == 'B':
                    p0.moleculesB.append(m)

        for m in searched[1]:
            if searched[0][m]:

                if m.kind == 'A':
                    p1.moleculesA.append(m)

                elif m.kind == 'B':
                    p1.moleculesB.append(m)

        return [p0, p1]

    def __repr__(self):
        # return "location: {}, \n_moleculesA: {}, \n_moleculesB: {}"\
        #     .format( self.location, self.moleculesA, self.moleculesB)

        return "{}{}" \
            .format(self.moleculesA, self.moleculesB)
