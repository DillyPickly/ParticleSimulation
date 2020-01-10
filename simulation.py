import numpy as np
import Molecule
import Particle
import Box
from collections import deque

'''
In this simulation, we start with alpha and beta molecules. 
The alpha molecules are groups of alpha particles.
The beta molecules are groups of beta particles.
The molecules then have a chance to bind with the other species as time goes on.
These combined molecules are referred to as a complex.
Each complex is described by its available alpha and beta bonding sites
Each molecule can then be described as a complex with only alpha sites or only beta sites.
(because we do not allow alpha-alpha or beta-beta bonding)
Finally, an alpha site contains an alpha particles and can bond to a beta molecule at that site.
'''

_in_assoc = 0.6  # inherent association probability
_in_dissoc = 0.1  # inherent dissociation probability

_valency = 3  # available sites on each molecule (a.k.a. free domains)
_num_A_molecules = 6
_num_B_molecules = 10
_box_dimensions = (3, 3, 3)


def prob_association(alpha, beta):
    return _in_assoc * (1 - _in_dissoc) * 20 / (20 + alpha + beta)


def prob_diffusion(alpha, beta):
    return 1 / 6 * 1 / np.sqrt(alpha + beta)


def prob_dissociation(alpha, beta):
    return _in_dissoc * (1 - _in_assoc)


def initialize_simulation():
    box = Box.Create(_box_dimensions)
    x, y, z = _box_dimensions
    for a in range(_num_A_molecules):
        i = np.random.choice(x)
        j = np.random.choice(y)
        k = np.random.choice(z)

        m = Molecule.Create('A', _valency)
        p = Particle.Create(m, None, (i, j, k))
        box.add_particle(p)

    for b in range(_num_B_molecules):
        i = np.random.choice(x)
        j = np.random.choice(y)
        k = np.random.choice(z)

        m = Molecule.Create('B', _valency)
        p = Particle.Create(None, m, (i, j, k))
        box.add_particle(p)

    return box


# TODO def association
def association(box):
    x, y, z = _box_dimensions
    for i in range(x):
        for j in range(y):
            for k in range(z):
                if len(box.box[i,j,k]) is 0:
                    # print('Here, {}{}{}:'.format(i,j,k))
                    continue

                A_molecules = []
                A_sites = 0
                B_molecules = []
                B_sites = 0

                for particle in box.box[i, j, k]:
                    for moleculeA in particle.moleculesA:

                        if moleculeA.bond <= 0:
                            continue

                        A_molecules.append([moleculeA, particle])
                        A_sites += moleculeA.bond

                    for moleculeB in particle.moleculesB:

                        if moleculeB.bond <= 0:
                            continue

                        B_molecules.append([moleculeB, particle])
                        B_sites += moleculeB.bond

                if B_sites == 0 or A_sites == 0:
                    continue

                prob = prob_association(A_sites, B_sites)
                p = [prob, 1 - prob]
                # assoc = np.random.choice(2, total_sites, p=p)
                #
                # if A_sites < B_sites:
                #     for m_a in A_molecules:
                #         for b in m_a[0].bonds:
                #
                # else:






    return box
# TODO def diffusion

# TODO def dissociation


def main():
    b = initialize_simulation();
    # print(b)
    a = association(b)
    # print(a)

if __name__ == '__main__':
    main()
