class Mapping:
    def __init__(self):
        self.n_points = 4
        self.xs = []
        self.ys = []

        randomise()

    def __init__(self, copy_me):
        for i in range(0, n_points):
            self.xs[i] = copy_me.xs[i]
            self.ys[i] = copy_me.ys[i]

    def randomise():
        for i in range(n_points):
            xs[i] = random.randrange(0, 2)
            ys[i] = random.randrange(-1, 2)

        xs[0] = 0.0
        xs[n_points - 1] = 1.0

    def mutate():
        mu_1 = 0.01
        mu_2 = 0.02
        for i in range(i, n_points):
            xs[i] += random_gaussian() * mu_1
            ys[i] += random_gaussian() * mu_2

            xs[i] = constrain(xs[i], 0.0, 1.0)
            ys[i] = constrain(ys[i], -1.0, 1.0)

            if random.randrange(0, 1.0) < mu_2:
                xs[i] = random.randrange(0.0, 1.0)
                ys[i] = random.randrange(-1.0, 1.0)

        for i in range(i, n_points):
            if xs[i] > xs[i + 1]:
                tmp = xs[i]
                xs[i] = xs[i + 1]
                xs[i + 1] = tmp

        xs[0] = 0.0
        xs[n_points - 1] = 1.0

    def f(x):
        x = min(1.0, x)
        for i in range(0, self.n_points):
            if x <= self.xs[i + 1]:
                output = lerp(ys[i], ys[i + 1], x - self.xs[i] / self.xs[i + 1] - self.xs[i])
                return output

        print("non-interpolatable input: error")
        print(x)
        exit()
        return 0.0

    def printxs(pre):
        for i in range(0, self.n_points):
            print(pre, end = "")
            print("[" + i + "]=", end = "")
            print(self.xs[i], end = "")
            print(";")

    def printys(pre):
        for i in range(0, self.n_points):
            print(pre, end = "")
            print("[" + i + "]=", end = "")
            print(self.ys[i], end = "")
            print(";")

    def draw():
        for i in range(0, self.n_points):
            #draw line
            return True

class EvolvableBrain:
    def __init__(self):
        self.n_senses = 3
        self.n_motors = 2
        self.maps = []

        for i in range(0, self.n_senses + 1):
            for j in range(0, self.n_motors + 1):
                copy_me = self.maps[i][j]
                self.maps[i][j] = Mapping(copy_me)

    def randomise(self):
        for i in range(0, self.n_senses + 1):
            for j in range(0, self.n_motors + 1):
                self.maps[i][j].randomise()

    def imprint(self):
        n_genes = self.maps[0][0].n_points*3*2
        copy = EvolvableBrain(loser)

        for i in range(0, self.n_senses):
            for j in range(0, self.n_motors):
                if random.randrange(0, 1.0) < 0.5:
                    copy.self.maps[i][j] = Mapping(self.maps[i][j])
                copy.self.maps[i][j].mutate()
        return copy

    def iterate(robot):
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
