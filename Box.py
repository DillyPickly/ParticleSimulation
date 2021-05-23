import random

from numpy.lib.nanfunctions import _replace_nan

import helpers
import numpy as np
from Particle import Particle
from Partition import Partition


class Box :

    def __init__(self, shape = (0,0)) -> None:
        self.shape = shape

        self.partitions = []
        for i in range(shape[0]):
            row = []
            for j in range(shape[1]):
                row.append(Partition((i,j)))
            self.partitions.append(row)

    def partition_interaction(self):
        """
        Partitions will only interact with themselves and 8 adjacent partitions (including diagonals)
        """
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                # print('index: (',i,j,') : particles = ', self.partitions[i][j].num_particles() )
                for p in self.partitions[i][j].particle_list:
                    
                    
                    for m in range(max(i-1,0),min(i+2,self.shape[0])):
                        for n in range(max(j-1,0),min(j+2,self.shape[1])):
                            # print("i,j :",i,j)
                            # Figure out where the particle is being pushed to
                            if p.is_type(0):
                                same_type = self.partitions[m][n].count_particle_type(0)
                                oppo_type = self.partitions[m][n].count_particle_type(1)
                            else:
                                oppo_type = self.partitions[m][n].count_particle_type(0)
                                same_type = self.partitions[m][n].count_particle_type(1)

                            same_type *= np.random.binomial(same_type,p.interaction_chance)
                            oppo_type *= np.random.binomial(oppo_type,p.interaction_chance)
                            
                            direction = (m-i, n-j) # if m is 2 and i is 1 then the direction is 1 and the direction is downwards
                            # print("m,n :",m,n)
                            
                            if direction[0] == 0 and direction[1] == 0:
                                # print('index: (',i,j,') : same interaction')
                                direction = random.choice([(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)])
                              
                                p.stay += p.affinity*same_type -1
                                p.movement[0] += direction[0]*( p.aversion*oppo_type)
                                p.movement[1] += direction[1]*( p.aversion*oppo_type)

                            p.movement[0] += direction[0]*(p.affinity*same_type - p.aversion*oppo_type)
                            p.movement[1] += direction[1]*(p.affinity*same_type - p.aversion*oppo_type)
                    
        next_box = self.new_box()
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                for p in self.partitions[i][j].particle_list:
                    
                    new_row = i
                    new_col = j

                    if abs(p.movement[0]) > p.stay:

                        if p.movement[0] < 0:
                            new_row -= 1
                        elif p.movement[0] > 0:
                            new_row += 1
                        
                    if abs(p.movement[1]) > p.stay:

                        if p.movement[1] < 0:
                            new_col -= 1
                        elif p.movement[1] > 0:
                            new_col += 1

                    if new_row < 0:
                        new_row = 0
                    if new_row > self.shape[0]-1:
                        new_row = self.shape[0]-1
                    if new_col < 0:
                        new_col = 0
                    if new_col > self.shape[1]-1:
                        new_col = self.shape[1]-1

                    next_box[new_row][new_col].add_particle(p.reset())
        self.partitions = next_box

        # add a cramming property that a has a chance to throw particles in random directions if more than a certain number of particles occupy a partition.
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                particles_over = self.partitions[i][j].num_particles() - Partition.threshold
                if particles_over > 0:
                    for p in np.random.choice(self.partitions[i][j].particle_list, particles_over, replace = False):
                        if random.random() < Particle.cramming_chance:
                            p.movement = random.choice([(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)])

                        
        final_box = self.new_box()
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                for p in self.partitions[i][j].particle_list:
                    
                    new_row = i
                    new_col = j

                    if abs(p.movement[0]) > 0 :

                        if p.movement[0] < 0:
                            new_row -= 1
                        elif p.movement[0] > 0:
                            new_row += 1
                        
                    if abs(p.movement[1]) > 0:

                        if p.movement[1] < 0:
                            new_col -= 1
                        elif p.movement[1] > 0:
                            new_col += 1

                    if new_row < 0:
                        new_row = 0
                    if new_row > self.shape[0]-1:
                        new_row = self.shape[0]-1
                    if new_col < 0:
                        new_col = 0
                    if new_col > self.shape[1]-1:
                        new_col = self.shape[1]-1

                    final_box[new_row][new_col].add_particle(p.reset())
        self.partitions = final_box  

        return final_box

    def add_new_particles(self,type0 = 1,type1 = 1):
        """
        type0 is the number of type0 particles
        type1 is the number of type1 particles
        This function randomly picks partitions adding particles to the partitions it picks
        """
        for t in range(type0):
            row = random.randint(0,self.shape[0]-1)
            col = random.randint(0,self.shape[1]-1)
            self.partitions[row][col].add_new_particle(type = 0)

        for t in range(type1):
            row = random.randint(0,self.shape[0]-1)
            col = random.randint(0,self.shape[1]-1)
            self.partitions[row][col].add_new_particle(type = 1)

        return

    def new_box(self):
        output = []
        for i in range(self.shape[0]):
            row = []
            for j in range(self.shape[1]):
                row.append(Partition((i,j)))
            output.append(row)
        return output

    def image_out(self, name = 'image.png'):
        pixels = []
        for i in range(self.shape[0]):
            row = []
            for j in range(self.shape[1]): 
                n = self.partitions[i][j].num_particles()
                type0 = self.partitions[i][j].count_particle_type(0)
                type1 = self.partitions[i][j].count_particle_type(1)
                # print(type0,type1,n)
                if n != 0:
                    # if particles are all type1 then the color then input is 1 if all type 0 input is 0
                    pixels.append( helpers.colormap(type1/n) )
                else:
                    pixels.append( (127,127,127) )

            # pixels.append(row)

        helpers.make_image(self.shape[1],self.shape[0],pixels,name=name)


    def __repr__(self) -> str:
        output = 'shape: {} \nPartitions: \n'.format(self.shape)
        for row in self.partitions:
            output=output+str(row)+'\n'
        return output

if __name__ == "__main__":
    shape = (2,2)
    test_box = Box(shape)
    print(test_box)

    particles_per_box = 4
    particles_0 = int(particles_per_box*shape[0]*shape[1]/2)
    particles_1 = int(particles_per_box*shape[0]*shape[1]/2)
    test_box.add_new_particles(particles_0,particles_1)
    print(test_box)

    test_box.partition_interaction()
    print(test_box)

    test_box.image_out('000.png')

    ### full test
    # shape = (200,200)
    # box = Box(shape)

    # particles_per_box = 4
    # particles_0 = int(particles_per_box*shape[0]*shape[1]/2)
    # particles_1 = int(particles_per_box*shape[0]*shape[1]/2)
    # box.add_new_particles(particles_0,particles_1)

    # for i in range(10):
    #     box.image_out('test/sim_{:03d}.png'.format(i))
    #     box.partition_interaction()
