import Molecule


def test_init():
    m = Molecule.Create('A', 10)
    if m.kind != 'A' or m.bonds != 10:
        print('Failed')
    else:
        print('Passed')
        print(m)


def main():
    test_init()


if __name__ == '__main__':
    main()
