import math
import random
from operator import attrgetter
import itertools
from enum import Enum
import typing
import copy
import json

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
            self[key].crossover(source[key])

    def flatten(self):
        return {key: self[key].flatten() for key in self}

    def from_flattened(self, flattened):
        for key in flattened:
            self[key].from_flattened(flattened[key])

    def to_json(self):
        return json.dumps(self.flatten())

    def from_json(self, json_string):
        self.from_flattened(json.loads(json_string))

    def dump(self, indent=0):
        message = ""
        first_indent_ignored = False
        for key in self:
            line = f" -> {key}"
            if first_indent_ignored:
                message += " " * indent
            first_indent_ignored = True
            message += line
            message += self[key].dump(indent + len(line))
            if message[-1] != "\n":
                message += "\n"
        return message


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

    def flatten(self):
        return self.value

    def from_flattened(self, flattened):
        self.value = flattened

    def dump(self, indent=0):
        return f" = {self.value}"

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

    def flatten(self):
        return [item.flatten() for item in self.list]

    def from_flattened(self, flattened):
        for (item, flattened_item) in zip(self.list, flattened):
            item.from_flattened(flattened_item)


class SmellSignatureGene(ListGene):
    NUM_DIMENSIONS = 5
    BOUNDS = (-1.0, 1.0)
    MAX_INCOMPATIBILITY = NUM_DIMENSIONS * ((BOUNDS[1] - BOUNDS[0]) ** 2)

    def __init__(self):
        super().__init__()
        self.list = [FloatGene(bounds=self.BOUNDS) for _ in range(self.NUM_DIMENSIONS)]

    def incompatibility_with(self, other_smell_signature):
        euclidean_distance_squared = 0
        for i in range(self.NUM_DIMENSIONS):
            euclidean_distance_squared += (self.list[i].value - other_smell_signature.list[i].value) ** 2
        return euclidean_distance_squared


class DynamicListGene(ListGene):
    def __init__(self, element_class, addition_probability=0.001, removal_probability=0.001, init_size_range=(0, 10)):
        self.elementClass = element_class
        self.additionProbability = addition_probability
        self.removalProbability = removal_probability
        self.initSizeRange = init_size_range
        super().__init__()

    def randomise(self):
        self.list = [self.elementClass() for _ in range(random.randrange(*self.initSizeRange))]
        super().randomise()

    def mutate(self):
        super().mutate()
        if random.random() < self.removalProbability:
            self.list.pop(random.randrange(0, len(self.list)))
        if random.random() < self.additionProbability:
            # Note: Using randint to allow appending after last element.
            self.list.insert(random.randint(0, len(self.list)), self.elementClass())

    def crossover(self, source):
        # First, pre-compute all the incompatibility values between each element.
        ours_to_consider = set(range(len(self.list)))
        theirs_to_consider = set(range(len(source.list)))
        incompatibility = np.zeros((len(ours_to_consider), len(theirs_to_consider)))
        for (ours, theirs) in itertools.product(ours_to_consider, theirs_to_consider):
            incompatibility[ours][theirs] = self.list[ours].incompatibility_with(source.list[theirs])

        # Next, approximate the solution to the Assignment Problem by greedily choosing the best pair each time.
        while ours_to_consider and theirs_to_consider:
            best_ours = None
            best_theirs = None
            min_incompatibility = math.inf
            for ours in ours_to_consider:
                theirs = min(theirs_to_consider, key=incompatibility[ours].__getitem__)
                if incompatibility[ours][theirs] < min_incompatibility:
                    best_ours = ours
                    best_theirs = theirs
                    min_incompatibility = incompatibility[ours][theirs]
            self.list[best_ours].crossover(source.list[best_theirs])
            ours_to_consider.remove(best_ours)
            theirs_to_consider.remove(best_theirs)

        # Append their remaining elements
        for theirs in theirs_to_consider:
            self.list.append(copy.deepcopy(source.list[theirs]))

    def incompatibility_with(self, other_dynamic_list):
        incompatibility = 0
        for (ours, theirs) in zip(self.list, other_dynamic_list.list):
            incompatibility += ours.incompatibility_with(theirs)
        return incompatibility

    def from_flattened(self, flattened):
        self.list = []
        for flattened_item in flattened:
            item = self.elementClass()
            item.from_flattened(flattened_item)
            self.list.append(item)


class PiecemealPoint(Genetic):
    def __init__(self):
        super().__init__()
        self.x = FloatGene()
        self.y = FloatGene()


class PiecemealMappingGene(DynamicListGene):
    def __init__(self, crossover_probability=0.01, addition_probability=0.001, removal_probability=0.001):
        self.crossoverProbability = crossover_probability
        super().__init__(
            element_class=PiecemealPoint,
            addition_probability=addition_probability,
            removal_probability=removal_probability,
            init_size_range=(2, 5)
        )
        self.randomise()

    def randomise(self):
        super().randomise()
        self.__normalise()

    def mutate(self):
        super().mutate()
        self.__normalise()

    def crossover(self, source):
        if random.random() < self.crossoverProbability:
            self.list = []
            for point in source.list:
                self.list.append(copy.deepcopy(point))

    def __normalise(self):
        self.list.sort(key=attrgetter('x.value'))
        if len(self.list) < 2:
            self.list += [PiecemealPoint() for _ in range(2 - len(self.list))]
        self.list[0].x.value = 0.0
        self.list[-1].x.value = 1.0


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

    def flatten(self):
        return self.laterality.name

    def from_flattened(self, flattened):
        self.laterality = Laterality[flattened]

    def dump(self, indent=0):
        return f" = {self.laterality.name}"


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
        laterality_incompatibility = (
            0 if self.motorSide.laterality == other_sensor.motorSide.laterality
            else SmellSignatureGene.MAX_INCOMPATIBILITY
        )
        return laterality_incompatibility + self.smellSignature.incompatibility_with(other_sensor.smellSignature)


class RobotGenome(Genetic):
    def __init__(self):
        super().__init__()
        self.sensors = DynamicListGene(SensorGene)


def full_examples():
    environment_genome = EnvironmentGenome()
    robot_genome = RobotGenome()

    def print_state(header):
        print(f"\n{header}\n{'=' * len(header)}\n")
        print("environment_genome:")
        print(environment_genome.dump())
        print("robot_genome:")
        print(robot_genome.dump())

    print_state("Initial")

    environment_genome.randomise()
    robot_genome.randomise()
    print_state("Randomised")

    environment_genome.mutate()
    robot_genome.mutate()
    print_state("Mutated")

    environment_genome2 = EnvironmentGenome()
    robot_genome2 = RobotGenome()

    environment_genome.crossover(environment_genome2)
    robot_genome.crossover(robot_genome2)
    print_state("Crossovered with new initial genomes")

    environment_genome2.randomise()
    robot_genome2.randomise()
    environment_genome.crossover(environment_genome2)
    robot_genome.crossover(robot_genome2)
    print_state("Crossovered with new randomised genomes")


def gene_examples(gene1, gene2):
    print("=" * 80)
    print(gene1.__class__.__name__)
    print(gene2.__class__.__name__)
    print("Initial:")
    print(f"gene1:{gene1.dump(6)}")
    print(f"gene2:{gene2.dump(6)}")

    print("Randomise:")
    gene1.randomise()
    gene2.randomise()
    print(f"gene1:{gene1.dump(6)}")
    print(f"gene2:{gene2.dump(6)}")

    for _ in range(6):
        print("Mutated:")
        gene1.mutate()
        gene2.mutate()
        print(f"gene1:{gene1.dump(6)}")
        print(f"gene2:{gene2.dump(6)}")

    for _ in range(3):
        print("Crossover:")
        gene1.crossover(gene2)
        print(f"gene1:{gene1.dump(6)}")
        print(f"gene2:{gene2.dump(6)}")

    print("Randomise a copy (ensure that copy doesn't affect original):")
    clone = copy.deepcopy(gene1)
    clone.randomise()
    print(f"gene1:{gene1.dump(6)}")
    print(f"copy: {clone.dump(6)}")

    print("JSON:")
    print(gene1.to_json())
    print(gene2.to_json())

    print("To JSON and back again, swapped:")
    gene1.randomise()
    gene2.randomise()
    print("Before swap:")
    print(f"gene1:{gene1.dump(6)}")
    print(f"gene2:{gene2.dump(6)}")
    json1 = gene1.to_json()
    json2 = gene2.to_json()
    gene2.from_json(json1)
    gene1.from_json(json2)
    print("After swap:")
    print(f"gene1:{gene1.dump(6)}")
    print(f"gene2:{gene2.dump(6)}")


def run_examples():
    # full_examples()
    pairs_to_test = [
        (
            FloatGene(randomise_probability=0.0, crossover_probability=1.0),
            FloatGene(randomise_probability=0.0, crossover_probability=1.0)
        ),
        (
            SmellSignatureGene(),
            SmellSignatureGene()
        ),
        (
            PiecemealPoint(),
            PiecemealPoint()
        ),
        (
            ThingGene(),
            ThingGene()
        ),
        (
            LateralityGene(crossover_probability=1.0),
            LateralityGene(crossover_probability=1.0)
        ),
        (
            PiecemealMappingGene(crossover_probability=1.0, addition_probability=0.3, removal_probability=0.3),
            PiecemealMappingGene(crossover_probability=1.0, addition_probability=0.3, removal_probability=0.3)
        ),
        (
            EnvironmentGenome(),
            EnvironmentGenome()
        ),
        (
            SensorGene(),
            SensorGene()
        ),
        (
            RobotGenome(),
            RobotGenome()
        ),
    ]
    for pair in pairs_to_test:
        gene_examples(*pair)

    goodbye = "Examples have finished executing. Please manually inspect the output above for correctness."
    print("^" * len(goodbye))
    print(goodbye)


if __name__ == "__main__":
    run_examples()
