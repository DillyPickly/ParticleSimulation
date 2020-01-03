import numpy as np
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


def prob_association(alpha, beta):
    return _in_assoc * (1 - _in_dissoc) * 20 / (20 + alpha + beta)


def prob_diffusion(alpha, beta):
    return 1 / 6 * 1 / np.sqrt(alpha + beta)


def prob_dissociation(alpha, beta):
    return _in_dissoc * (1 - _in_assoc)


_x, _y, _z = (3, 3, 3)
number_cubes = _x * _y * _z

_in_assoc = 0.6  # inherent association probability
_in_dissoc = 0.1  # inherent dissociation probability
_valency = 3  # available sites on each molecule (a.k.a. free domains)
_num_molecules = 6
_species = 2

# each molecule is described by an index and value gives it the free bonds
molecules = _valency * np.ones([_species, _num_molecules], dtype=object)
molecules_bonds = np.empty([_species, _num_molecules], dtype=object)
for i in range(_species):
    for j in range(_num_molecules):
        molecules_bonds[i, j] = [_valency]
        # [ #free bonds, [number of bonds, [molecule id]], ... ]

# each complex is described by an id from a set of id's
free = set([i for i in range(_num_molecules * _species)])
used = set()

complexes = {}
for i in range(_species):
    for j in range(_num_molecules):
        id = free.pop()
        complexes[id] = [[i, j]]
        used.add(id)

# print(complexes)

# this contains lists of the complexes in each container
cubes = np.empty([_x, _y, _z], dtype=object)
for i in range(_x):
    for j in range(_y):
        for k in range(_z):
            cubes[i, j, k] = []


def extract_complex(x, y, z):
    return cubes[x, y, z]


def extract_molecules(x, y, z, complexes):
    nearby_complexes = extract_complex(x, y, z)

    if len(nearby_complexes) == 0:
        return None, None

    nearby_molecules = np.empty(_species, dtype=object)
    for i in range(_species):
        nearby_molecules[i] = []

    molecule_complex_relations = np.empty_like(molecules)
    for c in nearby_complexes:
        for m in complexes[c]:
            nearby_molecules[m[0]].append(m[1])
            # print('complex key:', c)
            molecule_complex_relations[m[0], m[1]] = c

    return nearby_molecules, molecule_complex_relations


# Initially, randomly distribute alpha and beta complexes
for i in complexes.keys():
    x = np.random.choice(range(_x))
    y = np.random.choice(range(_y))
    z = np.random.choice(range(_z))
    cubes[x, y, z].append(i)

# print('cubes: ',cubes)

# go through association then diffusion then dissociation
for i in range(_x):
    for j in range(_y):
        for k in range(_z):
            nearby_molecules, nearby_complexes = extract_molecules(i, j, k, complexes)
            if nearby_molecules is None:
                # print(i,j,k)
                continue
            elif len(nearby_molecules[0]) == 0:
                continue
            elif len(nearby_molecules[1]) == 0:
                continue

            # print(nearby_molecules[0])
            # print(nearby_molecules[1])

            total_sites = np.zeros(_species, dtype=int)
            # for kind in range(_species):
            #     total_sites[kind] = np.sum(molecules[kind, nearby_molecules[kind]])
            # print(total_sites)

            sites = np.zeros(_species, dtype=list)
            sites[0] = []
            sites[1] = []
            for kind in range(_species):
                for index, s in enumerate(molecules[kind, nearby_molecules[kind]]):
                    # print(s*[[kind, nearby_molecules[kind][index]]])
                    total_sites[kind] += s
                    for _ in range(s):
                        sites[kind].append([kind, nearby_molecules[kind][index]])
                    # sites[kind].append(s*[])

            # print(total_sites)
            # print(sites)

            prob = prob_association(total_sites[0], total_sites[1])
            p = [prob, 1 - prob]
            assoc = np.random.choice(2, total_sites, p=p)
            # print(assoc)

            new_bonds = []
            for m in range(total_sites[0]):
                for n in range(total_sites[1]):
                    if assoc[m, n] == 1:
                        assoc[:, n] = 0
                        assoc[m, :] = 0
                        assoc[m, n] = 1
                        new_bonds.append([m, n])
                        break

            for n in new_bonds:
                # print(n)
                # print(sites[0][n[0]])
                # print(sites[1][n[1]])

                molecules[sites[0][n[0]][0], sites[0][n[0]][1]] -= 1
                molecules[sites[1][n[1]][0], sites[1][n[1]][1]] -= 1

                complex_key_a = nearby_complexes[sites[0][n[0]][0], sites[0][n[0]][1]]
                complex_key_b = nearby_complexes[sites[1][n[1]][0], sites[1][n[1]][1]]
                # print('nearby_complexes', nearby_complexes)

                if complex_key_a != complex_key_b:
                    # print(complexes.keys())
                    # print('complex_key_b', complexes[complex_key_b])
                    # print('complex_key_a', complexes[complex_key_a])

                    complexes[complex_key_a] += complexes[complex_key_b]
                    used.remove(complex_key_b)
                    free.add(complex_key_b)
                    del complexes[complex_key_b]
                    cubes[i, j, k].remove(complex_key_b)
                    nearby_complexes[sites[1][n[1]][0], sites[1][n[1]][1]] = complex_key_a
                    # print(complexes[complex_key_a])

            # print(assoc)
            print('complexes', complexes)
            print('molecules', molecules)
            print('cubes', cubes)

            # now to do diffusion

            # choose the random direction for diffusion
            for index, c in enumerate(extract_complex(i, j, k)):
                # print(c)
                prob = prob_diffusion(len(complexes[c]), 0)
                p = [prob, 1-prob]
                if np.random.choice(2, p=p):
                    # choose the direction
                    dir = np.random.choice([-1, 1], size=3)
                    new_cube = [i, j, k] + dir
                    print('new_cube', new_cube)
                    if np.all(new_cube < [_x, _y, _z]) and np.all(new_cube > 0) :
                        cubes[new_cube[0], new_cube[1], new_cube[2]].append(c)
                        # print(index)
                        print('cubes[i,j,k]', cubes[i,j,k])
                        cubes[i, j, k].remove(c)


            print('cubes', cubes)

            # now to do dissociation
            # choose which complexes to dissociate

            print(cubes[i, j, k])
            for c in cubes[i, j, k]:
                if len(complexes[c]) < 2 :
                    continue
                for m in c:
                    for bond in molecules_bonds[m[0], m[1]][1:]:
                        print(m)
                        print(bond)

                print('complex',complexes[c])





# association of complexes (in each cube)
