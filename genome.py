import math
import random
import numpy as np


class Genetic:
    def __init__(self):
        pass

    def __iter__(self):
        return vars(self).__iter__()

    def __getitem__(self, item):
        return vars(self)[item]

    def __setitem__(self, key, value):
        vars(self)[key] = value

    def randomise(self):
        for key in self:
            self[key].randomise()

    def mutate(self):
        for key in self:
            self[key].mutate()

    def crossover(self, source):
        for key in source:
            if key in self:
                self[key].crossover(source[key])
            else:
                self[key] = source[key]


class FloatGene(Genetic):
    def __init__(self, mutation_args=None, randomise_probability=0.001, crossover_probability=0.5, bounds=(0, 1), wrap=False):
        super().__init__()
        if mutation_args is None:
            mutation_args = {"mu": 0.0, "sigma": 0.01}
        self.value = 0.0
        self.mutationArgs = mutation_args
        self.randomiseProbability = randomise_probability
        self.crossoverProbability = crossover_probability
        self.bounds = bounds
        self.wrap = wrap
        self.randomise()

    def randomise(self):
        self.value = random.uniform(*self.bounds)

    def mutate(self):
        self.value += random.gauss(**self.mutationArgs)
        if random.random() < self.randomiseProbability:
            self.randomise()
        self.__normalise()

    def crossover(self, source):
        if random.random() < self.crossoverProbability:
            self.value = source.value
        self.__normalise()

    def __normalise(self):
        if self.wrap:
            self.value -= self.bounds[0]
            self.value %= self.bounds[1] - self.bounds[0]
            self.value += self.bounds[0]
        else:
            self.value = np.clip(self.value, *self.bounds)


class ListGene(Genetic):
    def __init__(self):
        super().__init__()
        self.list = []

    def __iter__(self):
        return range(len(self.list))

    def __getitem__(self, item):
        return self.list[item]

    def __setitem__(self, key, value):
        self.list[key] = value


SIGNATURE_NUM_DIMENSIONS = 5


class SmellSignatureGene(ListGene):
    def __init__(self):
        super().__init__()
        self.list = [FloatGene(bounds=(-1.0, 1.0)) for _ in range(SIGNATURE_NUM_DIMENSIONS)]


class DynamicListGene(ListGene):
    def __init__(self, element_class, addition_probability=0.001, removal_probability=0.001, init_size_range=(0, 10)):
        self.elementClass = element_class
        self.additionProbability = addition_probability
        self.removalProbability = removal_probability
        self.initSizeRange = init_size_range
        super().__init__()

    def __setitem__(self, key, value):
        if key >= len(self.list):
            self.list += [self.elementClass() for _ in range(len(self.list), key + 1)]
        super().__setitem__(key, value)

    def randomise(self):
        self.list = [self.elementClass() for _ in range(random.uniform(*self.initSizeRange))]
        super().randomise()

    def mutate(self):
        super().mutate()
        if random.random() < self.additionProbability:
            self.list.pop(random.randrange(0, len(self.list)))
        if random.random() < self.additionProbability:
            # Note: Using randint to allow appending after last element.
            self.list.insert(random.randint(0, len(self.list)), self.elementClass())

    # TODO: Cross over alignment / pairing
    def crossover(self, source):
        super().crossover(source)


class PiecemealPoint(Genetic):
    def __init__(self):
        self.x = FloatGene()
        self.y = FloatGene()


class PiecemealMappingGene(DynamicListGene):
    def __init__(self):
        super().__init__(PiecemealPoint)
        self.randomise()

    def mutate(self):
        super().mutate()
        self.__normalise()

    def crossover(self, source):
        super().crossover(source)
        self.__normalise()
        # TODO: Crossover granularity

    def __normalise(self):
        # TODO: sort by x and ensure first and last are 0.0 and 1.0
        pass


class ThingGene(Genetic):
    def __init__(self):
        super().__init__()
        self.amount = FloatGene()
        self.smellSignature = SmellSignatureGene()


class EnvironmentGenome(Genetic):
    def __init__(self):
        super().__init__()
        self.waterGenes = DynamicListGene(ThingGene)
        self.foodGenes = DynamicListGene(ThingGene)
        self.hazardGenes = DynamicListGene(ThingGene)


class SensorGene(Genetic):
    def __init__(self):
        super().__init__()
        self.threshold = FloatGene()
        self.angle = FloatGene(bounds=(0.0, 2.0 * math.pi), wrap=True)
        self.smellSignature = SmellSignatureGene()


class RobotGenome(Genetic):
    def __init__(self):
        super().__init__()
        self.sensors = DynamicListGene(SensorGene)
