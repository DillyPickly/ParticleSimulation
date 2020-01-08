import numpy as np


class Create:
    def __init__(self, size_x, size_y, size_z):
        self.dimensions = (size_x, size_y, size_z)
        self.box = np.empty(shape=(size_x, size_y, size_z), dtype=object)
        for i in range(size_x):
            for j in range(size_y):
                for k in range(size_z):
                    self.box[i, j, k] = []

    def add_particle(self, particle):
        x, y, z = particle.location
        self.box[x, y, z].append(particle)

    # def move_particle(self, particle0, new_location):
    #     if np.any(new_location >= self.dimensions):
    #         return
    #
    #     if np.any(new_location < 0):
    #         return



    def __repr__(self):
        return "{}".format(self.box)
