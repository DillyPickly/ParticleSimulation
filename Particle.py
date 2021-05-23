class Particle :
    affinity = 1
    aversion = 1
    interaction_chance = 0.05
    cramming_chance = 0.5

    def __init__(self, type = 0) -> None:
        self.type = type
        self.movement = [0,0]
        self.stay = 0

    def is_type(self, type):
        return self.type == type

    def reset(self):
        self.movement = [0,0]
        self.stay = 0
        return self

    def __repr__(self) -> str:
        return "Type: {} \nAffinity: {} \nAversion {}".format(self.type, self.affinity, self.aversion)

    # def interact():


if __name__ == "__main__":
    test_particle = Particle(1)
    print(test_particle)