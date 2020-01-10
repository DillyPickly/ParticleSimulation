import Box
import Particle
import Molecule


def test_init():
    box = Box.Create((1, 3, 2))
    print(box)

def test_add_particle():
    box = Box.Create((1, 3, 2))

    m0 = Molecule.Create('A', 10)
    m1 = Molecule.Create('B', 2)
    m2 = Molecule.Create('A', 4)

    p0 = Particle.Create(m0, m1, (0, 0, 1))
    p1 = Particle.Create(m2, None, (0, 0, 0))

    box.add_particle(p0)
    box.add_particle(p1)

    print(box)

def test_move_particle():
    box = Box.Create((1, 3, 2))

    m0 = Molecule.Create('A', 10)
    m1 = Molecule.Create('B', 2)
    m2 = Molecule.Create('A', 4)

    p0 = Particle.Create(m0, m1, (0, 0, 1))
    p1 = Particle.Create(m2, None, (0, 0, 0))

    box.add_particle(p0)
    box.add_particle(p1)

    print(box.box)

    box.box[0, 0, 0].append(box.box[0, 0, 1][0])
    box.box[0, 0, 1].remove(box.box[0, 0, 1][0])

    print(box)

def main():
    # test_init()
    # test_add_particle()
    test_move_particle()

if __name__ == '__main__':
    main()
