class Particle:
    def __init__(self, molecules, types, location):
        self.molecules = [m for m in molecules]
        self.types = [t for t in types]
        self.location = location

    def join(self, particle):
        for m in particle.molecules:
            self.molecules.append(m)

        for t in particle.types:
            self.molecules.append(t)
                    
