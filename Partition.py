from Particle import Particle

class Partition :
    threshold = 5

    def __init__(self, index = (0,0)) -> None:
        self.index = index
        self.particle_list = []

    def num_particles(self):
        return len(self.particle_list)

    def add_particle(self, p = Particle()):
        self.particle_list.append(p)
        return

    def add_new_particle(self, type = 0):
        self.particle_list.append(Particle(type))
        return self

    def count_particle_type(self, type):
        count = 0
        for p in self.particle_list:
            if p.is_type(type):
                count += 1
        return count

    def __repr__(self) -> str:
        return 'N={}'.format(self.num_particles())

    def __str__(self) -> str:
        return 'Partition : {} \nNumber of Particles: {}'.format(self.index, self.num_particles())

if __name__ == "__main__":
    test_partition = Partition((1,1))
    print(test_partition)

    test_partition.add_new_particle(0)
    test_partition.add_new_particle(1)
    test_partition.add_new_particle(0)
    test_partition.add_new_particle(0)


    print('Total number of particles:',test_partition.num_particles())
    print('Number of 0 particles:',test_partition.count_particle_type(0))
    print('Number of 1 particles:',test_partition.count_particle_type(1))
