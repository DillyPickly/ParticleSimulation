import Molecule
import Particle

moleculeA = []
moleculeB = []
for i in range(10):
    moleculeA.append(Molecule.Create('A', 10))
    moleculeB.append(Molecule.Create('B', 10))


def test_init():
    p = Particle.Create(moleculeA, moleculeB, (0, 0, 0))

    if p.moleculesA != moleculeA or p.moleculesB != moleculeB:
        print('Failed')
    elif p.location != (0, 0, 0):
        print('Failed')
    else:
        print('Passed')
        print(p)


def test_join():
    m0 = Molecule.Create('A', 10)
    m1 = Molecule.Create('B', 2)
    m2 = Molecule.Create('A', 4)

    p0 = Particle.Create(m0, m1, (0, 0, 0))
    p1 = Particle.Create(m2, None, (0, 0, 0))

    print(p0)

    p1.join(p0)

    print(p0)
    print(p1)


def main():
    # test_init()
    test_join()


if __name__ == '__main__':
    main()
