import math
import random
from operator import attrgetter
import itertools
from enum import Enum
import typing

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

    def print(self, indent=0):
        for key in self:
            print(" " * indent + "- " + key)
            self[key].print(indent + 1)


class FloatGene(Genetic):
    def __init__(self, mutation_args=None, randomise_probability=0.001,
                 crossover_probability=0.5, bounds=(0, 1), wrap=False):
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

    def print(self, indent=0):
        print(" " * indent + " = " + self.value)

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
        return iter(range(len(self.list)))

    def __getitem__(self, item):
        return self.list[item]

    def __setitem__(self, key, value):
        self.list[key] = value


SIGNATURE_NUM_DIMENSIONS = 5


class SmellSignatureGene(ListGene):
    def __init__(self):
        super().__init__()
        self.list = [FloatGene(bounds=(-1.0, 1.0)) for _ in range(SIGNATURE_NUM_DIMENSIONS)]

    def incompatibility_with(self, other_smell_signature):
        euclidean_distance_squared = 0
        for i in range(SIGNATURE_NUM_DIMENSIONS):
            euclidean_distance_squared += (self.list[i].value - other_smell_signature.list[i].value) ** 2
        return euclidean_distance_squared


class DynamicListGene(ListGene):
    def __init__(self, element_class, addition_probability=0.001, removal_probability=0.001,
                 init_size_range=(0, 10), init_list=None):
        if init_list is None:
            init_list = []
        self.elementClass = element_class
        self.additionProbability = addition_probability
        self.removalProbability = removal_probability
        self.initSizeRange = init_size_range
        super().__init__()
        self.list = init_list

    def __setitem__(self, key, value):
        if key >= len(self.list):
            self.list += [self.elementClass() for _ in range(len(self.list), key + 1)]
        super().__setitem__(key, value)

    def randomise(self):
        self.list = [self.elementClass() for _ in range(random.randrange(*self.initSizeRange))]
        super().randomise()

    def mutate(self):
        super().mutate()
        if random.random() < self.additionProbability:
            self.list.pop(random.randrange(0, len(self.list)))
        if random.random() < self.additionProbability:
            # Note: Using randint to allow appending after last element.
            self.list.insert(random.randint(0, len(self.list)), self.elementClass())

    def crossover(self, source):
        best_permutation = None
        min_incompatibility = math.inf
        for source_permutation in source.permutations():
            incompatibility = self.incompatibility_with(source_permutation) < min_incompatibility
            if incompatibility < min_incompatibility:
                best_permutation = source_permutation
                min_incompatibility = incompatibility
        super().crossover(best_permutation)

    def incompatibility_with(self, other_dynamic_list):
        incompatibility = 0
        for (ours, theirs) in zip(self.list, other_dynamic_list.list):
            incompatibility += ours.incompatibility_with(theirs)
        return incompatibility

    def permutations(self):
        for list_permutation in itertools.permutations(self.list):
            yield DynamicListGene(element_class=self.elementClass,
                                  addition_probability=self.additionProbability,
                                  removal_probability=self.removalProbability,
                                  init_size_range=self.initSizeRange,
                                  init_list=list_permutation)


class PiecemealPoint(Genetic):
    def __init__(self, point_to_copy=None):
        super().__init__()
        self.x = FloatGene()
        self.y = FloatGene()
        if point_to_copy is not None:
            self.x.value = point_to_copy.x.value
            self.y.value = point_to_copy.y.value


class PiecemealMappingGene(DynamicListGene):
    def __init__(self, crossover_probability=0.01):
        self.crossoverProbability = crossover_probability
        super().__init__(element_class=PiecemealPoint, init_size_range=(2, 5))
        self.randomise()

    def mutate(self):
        super().mutate()
        self.__normalise()

    def crossover(self, source):
        if random.random() < self.crossoverProbability:
            self.list = []
            for point in source.list:
                self.list.append(PiecemealPoint(point))

    def __normalise(self):
        self.list.sort(key=attrgetter('x'))
        if len(self.list) < 2:
            self.list += [PiecemealPoint() for _ in range(2 - len(self.list))]
        self.list[0].x = 0.0
        self.list[-1].x = 0.0


class ThingGene(Genetic):
    def __init__(self):
        super().__init__()
        self.amount = FloatGene()
        self.smellSignature = SmellSignatureGene()

    def incompatibility_with(self, other_thing):
        return self.smellSignature.incompatibility_with(other_thing.smellSignature)


class Laterality(Enum):
    LEFT = 1
    RIGHT = 2


# Enums are iterable. Suppress pycharm warnings by hinting it:
Laterality = Laterality  # type: typing.Union[typing.Type[Laterality], typing.Iterable]


class LateralityGene(Genetic):
    def __init__(self, randomise_probability=0.001, crossover_probability=0.001):
        self.laterality = Laterality.LEFT
        self.randomiseProbability = randomise_probability
        self.crossoverProbability = crossover_probability
        super().__init__()
        self.randomise()

    def randomise(self):
        self.laterality = random.choice(list(Laterality))

    def mutate(self):
        if random.random() < self.randomiseProbability:
            self.randomise()

    def crossover(self, source):
        if random.random() < self.crossoverProbability:
            self.laterality = source.laterality

    def print(self, indent=0):
        print(" " * indent + " = " + self.laterality.name)


class EnvironmentGenome(Genetic):
    def __init__(self):
        super().__init__()
        self.waterGenes = DynamicListGene(ThingGene)
        self.foodGenes = DynamicListGene(ThingGene)
        self.hazardGenes = DynamicListGene(ThingGene)


class SensorGene(Genetic):
    def __init__(self):
        super().__init__()

        # Either
        self.threshold = FloatGene()
        # or
        self.mapping = PiecemealMappingGene()

        self.angle = FloatGene(bounds=(0.0, 2.0 * math.pi), wrap=True)
        self.smellSignature = SmellSignatureGene()

        self.motorSide = LateralityGene()

    def incompatibility_with(self, other_sensor):
        return self.smellSignature.incompatibility_with(other_sensor.smellSignature)


class RobotGenome(Genetic):
    def __init__(self):
        super().__init__()
        self.sensors = DynamicListGene(SensorGene)


def run_examples():
    environment_genome = EnvironmentGenome()
    robot_genome = RobotGenome()

    def print_state():
        print("environment_genome:")
        environment_genome.print()
        print("robot_genome:")
        robot_genome.print()

    print_state()
    environment_genome.randomise()
    robot_genome.randomise()
    print_state()


if __name__ == "__main__":
    run_examples()
