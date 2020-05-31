import random
import numpy

class Mapping:
    def __init__(self, copy_me=None):
        self.n_points = 4
        self.xs = []
        self.ys = []

        if copy_me is None:
            self.randomise()
        else:
            self.xs = copy_me.xs.copy()
            self.ys = copy_me.ys.copy()

    def randomise(self):
        self.xs = [random.randrange(0, 2) for i in range(self.n_points)]
        self.ys = [random.randrange(-1, 2) for i in range(self.n_points)]
        self.xs[0] = 0.0
        self.xs[self.n_points - 1] = 1.0
        # TODO (Ernest): I believe xs and ys needs to be sorted via xs as required for interpolation

    def mutate(self):
        xs = self.xs
        ys = self.ys
        n_points = self.n_points

        mu_1 = 0.01
        mu_2 = 0.02
        for i in range(0, self.n_points):
            xs[i] += random.gauss() * mu_1
            ys[i] += random.gauss() * mu_2

            xs[i] = numpy.clip(xs[i], 0.0, 1.0)
            ys[i] = numpy.clip(ys[i], -1.0, 1.0)

            if random.randrange(0, 1.0) < mu_2:
                xs[i] = random.randrange(0.0, 1.0)
                ys[i] = random.randrange(-1.0, 1.0)

        # TODO (Ernest): I believe this attempted sorting is insufficient.
        for i in range(i, n_points):
            if xs[i] > xs[i + 1]:
                tmp = xs[i]
                xs[i] = xs[i + 1]
                xs[i + 1] = tmp

        xs[0] = 0.0
        xs[n_points - 1] = 1.0
        self.xs = xs
        self.ys = ys

    def f(self, x):
        x = min(1.0, x)
        xs = self.xs
        ys = self.ys
        n_points = self.n_points

        for i in range(0, n_points):
            if x <= xs[i + 1]:
                output = numpy.interp(ys[i], ys[i + 1], x - xs[i] / xs[i + 1] - xs[i])
                return output

        print("non-interpolatable input: error")
        print(self)
        exit()
        return 0.0

    def printxs(self, pre):
        for i in range(0, self.n_points):
            print(pre, end = "")
            print("[" + i + "]=", end = "")
            print(self.xs[i], end = "")
            print(";")

    def printys(self, pre):
        for i in range(0, self.n_points):
            print(pre, end = "")
            print("[" + i + "]=", end = "")
            print(self.ys[i], end = "")
            print(";")

    def draw(self):
        for i in range(0, self.n_points):
            #draw line
            return True

class EvolvableBrain:
    def __init__(self, copy_me=None):
        self.n_senses = 3
        self.n_motors = 2
        self.maps = [[0] * self.n_motors] * self.n_senses
        if copy_me is None:
            for i in range(0, self.n_senses):
                for j in range(0, self.n_motors):
                    self.maps[i][j] = Mapping()
        else:
            for i in range(0, self.n_senses):
                for j in range(0, self.n_motors):
                    self.maps[i][j] = Mapping(copy_me.maps[i][j])


    def randomise(self):
        for i in range(0, self.n_senses):
            for j in range(0, self.n_motors):
                self.maps[i][j].randomise()

    def imprint(self, loser):
        n_genes = self.maps[0][0].n_points*3*2
        copy = EvolvableBrain(loser)

        for i in range(0, self.n_senses):
            for j in range(0, self.n_motors):
                if random.randrange(0, 1.0) < 0.5:
                    copy.self.maps[i][j] = Mapping(self.maps[i][j])
                copy.self.maps[i][j].mutate()
        return copy

    def iterate(self, robot):
        lm_accum = 0.5
        rm_accum = -0.5

        for sensor_i in range(0, self.n_senses):
            leftm_ipsi = self.maps[sensor_i][0].f(robot.sensor_values[sensor_i][0])
            right_ipsi = self.maps[sensor_i][0].f(robot.sensor_values[sensor_i][1])

            leftm_contra = self.maps[sensor_i][1].f(robot.sensor_values[sensor_i][1])
            rightm_contra = self.maps[sensor_i][1].f(robot.sensor_values[sensor_i][0])

            lm_accum += leftm_ipsi + leftm_contra
            rm_accum += right_ipsi + rightm_contra
        robot.l_motor = lm_accum / 6.0
        robot.r_motor = rm_accum / 6.0
