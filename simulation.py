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

_x, _y, _z = (2, 2, 2)
number_cubes = _x * _y * _z

_in_assoc = 0.6  # inherent association probability
_in_dissoc = 0.1  # inherent dissociation probability
_valency = 3  # available sites on each molecule (a.k.a. free domains)
_num_molecules = 3
_species = 2

# each molecule is described by an index and value gives it the free bonds
molecules = _valency * np.ones([_num_molecules, _species], dtype=object)

# each complex is described by an id from a set of id's
free = set([i for i in range(_num_molecules * _species)])
used = set()


complexes = {}
for i in range(_species):
    for j in range(_num_molecules):
        id = free.pop()
        complexes[id] = np.array([i, j])
        used.add(id)

# this contains lists of the complexes in each container
cubes = np.empty([_x, _y, _z], dtype=object)
for i in range(_x):
    for j in range(_y):
        for k in range(_z):
            cubes[i, j, k] = []


def extract_complex(x, y, z):
    return cubes[x, y, z]


def extract_molecules(x, y, z):
    nearby_complexes = extract_complex(x, y, z)
    nearby_molecules = []
    for c in nearby_complexes:
        for m in complexes[c]:
            nearby_molecules.append(m)

    return nearby_molecules


# def extract_sites(x, y, z):
#     nearby_molecules = extract_molecules(x, y, z)
#     nearby sites =
#     for m in nearby_molecules:
#         molecules[m[0], m[1]]
#

def prob_association(alpha, beta):
    return _in_assoc * (1 - _in_dissoc) * 20 / (20 + alpha + beta)


def prob_diffusion(alpha, beta):
    return 1 / 6 * 1 / np.sqrt(alpha + beta)


def prob_dissociation(alpha, beta):
    return _in_dissoc * (1 - _in_assoc)


# Initially, randomly distribute alpha and beta complexes
for i in complexes.keys():
    x = np.random.choice(range(_x))
    y = np.random.choice(range(_y))
    z = np.random.choice(range(_z))
    cubes[x, y, z].append(i)

# print('cubes: ',cubes)

# go through association then diffusion then dissociation


# association of complexes (in each cube)
