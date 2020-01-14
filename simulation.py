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
_num_B_molecules = 15
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
                if len(box.box[i, j, k]) is 0:
                    # print('Here, {}{}{}:'.format(i,j,k))
                    continue

                A_sites = []
                B_sites = []

                for particle in box.box[i, j, k]:

                    for moleculeA in particle.moleculesA:
                        if moleculeA.full():
                            continue
                        A_sites.extend(moleculeA.n_empty() * [[moleculeA, particle]])

                    for moleculeB in particle.moleculesB:
                        if moleculeB.full():
                            continue
                        B_sites.extend(moleculeB.n_empty() * [[moleculeB, particle]])

                if B_sites == 0 or A_sites == 0:
                    continue

                np.random.shuffle(A_sites)
                np.random.shuffle(B_sites)

                prob = prob_association(len(A_sites), len(B_sites))
                p = [prob, 1 - prob]

                if len(A_sites) < len(B_sites):
                    for a_site in A_sites:
                        for b_index in range(len(B_sites)):
                            assoc = np.random.choice(2, p=p)
                            if assoc:
                                b_site = B_sites.pop(b_index)
                                b_site[0].join(a_site[0])
                                # decrement the number of bonds on each molecule

                                if a_site[1] != b_site[1]:
                                    box.box[i, j, k].remove(b_site[1])
                                    b_site[1] = a_site[1]

                                a_site[1].join(b_site[1])

                                break
                else:
                    for b_site in B_sites:
                        for a_index in range(len(A_sites)):
                            assoc = np.random.choice(2, p=p)
                            if assoc:
                                a_site = A_sites.pop(a_index)
                                a_site[0].join(b_site[0])
                                # decrement the number of bonds on each molecule

                                if a_site[1] != b_site[1]:
                                    print(a_site[1])
                                    print(box.box[i, j, k])
                                    box.box[i, j, k].remove(a_site[1])
                                    a_site[1] = b_site[1]

                                b_site[1].join(a_site[1])

                                break
    return box


# TODO def diffusion
def diffusion(box):
    new_box = Box.Create(_box_dimensions)

    x, y, z = _box_dimensions
    for i in range(x):
        for j in range(y):
            for k in range(z):
                if len(box.box[i, j, k]) is 0:
                    # print('Here, {}{}{}:'.format(i,j,k))
                    continue

                print("here0")
                for particle in box.box[i, j, k]:
                    prob = prob_diffusion(len(particle.moleculesA), len(particle.moleculesB))
                    p = [prob, 1 - prob]
                    diffuse = np.random.choice([1, 0], p=p)

                    if not diffuse:
                        new_box.add_particle(particle)

                    else:
                        new_x, new_y, new_z = np.random.choice([-1, 1], size=3, p=p)
                        try:
                            print('here1')
                            print((i+new_x, j+new_y, k+new_z))
                            particle.move((i+new_x, j+new_y, k+new_z))
                            new_box.add_particle(particle)

                        except IndexError:
                            print("here2")
                            pass
    return new_box




# TODO def dissociation


def main():
    b = initialize_simulation();
    print(b)
    a = association(b)
    # a = diffusion(b)
    print(a)


if __name__ == '__main__':
    main()
