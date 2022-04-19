import json
import math
from dataclasses import dataclass, astuple


@dataclass
class TwoBodyModel:
    positions: [[float]]


class TwoBodyController:
    m1 = 1
    m2 = 0.5
    m12 = 1.5
    position_a_planet = [1, 0]
    position_b_planet = [0, 0]

    def __init__(self, model, T, delta_t, mass_ratio, eccentricity, method):
        self.delta_t = delta_t
        self.T = T
        self.mass_ratio = mass_ratio
        self.eccentricity = eccentricity
        self.method = method
        self.model = model
        self.u = [1, 0, 0, self.initial_velocity()]

    def run(self):
        for _ in range(int(self.T / self.delta_t)):
            self.update_position()

    def derivative(self):
        new_positions = [0, 0, 0, 0]
        parsed_positions = self.u[0: 2]
        distance_between_planets = math.sqrt(math.pow(parsed_positions[0], 2) + math.pow(parsed_positions[1], 2))

        for i in range(2):
            new_positions[i] = self.u[i + 2]
            new_positions[i + 2] = -(1 + self.mass_ratio) * parsed_positions[i] / math.pow(distance_between_planets, 3)

        return new_positions

    def runge_kutta_calculation(self):
        a = [self.delta_t / 2, self.delta_t / 2, self.delta_t, 0]
        b = [self.delta_t / 6, self.delta_t / 3, self.delta_t / 3, self.delta_t / 6]
        u0 = []
        ut = []
        dimensions = len(self.u)

        for i in range(dimensions):
            u0.append(self.u[i])
            ut.append(0)

        for j in range(4):
            der = self.derivative()
            for i in range(dimensions):
                self.u[i] = u0[i] + a[j] * der[i]
                ut[i] = ut[i] + b[j] * der[i]

        for i in range(dimensions):
            self.u[i] = u0[i] + ut[i]

    def euler_calculation(self):
        dimensions = len(self.u)
        der = self.derivative()
        for i in range(dimensions):
            self.u[i] = self.u[i] + self.delta_t * der[i]

    def calculate_new_position(self):
        r = 1

        a1 = (self.m2 / self.m12) * r
        a2 = (self.m1 / self.m12) * r

        self.position_a_planet = [-a2 * self.u[0], -a2 * self.u[1]]
        self.position_b_planet = [a1 * self.u[0], a1 * self.u[1]]

    def initial_velocity(self):
        return math.sqrt((1 + self.mass_ratio) * (1 + self.eccentricity))

    def update_position(self):
        if self.method == "runge-kutta":
            self.runge_kutta_calculation()
        elif self.method == "euler":
            self.euler_calculation()
        self.calculate_new_position()
        self.model.positions.append(self.get_positions())

    def get_positions(self):
        return [self.position_a_planet[0], self.position_a_planet[1], self.position_b_planet[0],
                self.position_b_planet[1]]

    def get_step(self):
        return self.T


class TwoBodyApp:

    def __init__(self):
        self.model = TwoBodyModel([])
        self.controller = None

    def run(self):
        T = int(input("Enter T: "))
        delta_t = float(input("Enter δt: "))
        mass_ratio = float(input("Enter mass ratio: "))
        eccentricity = float(input("Enter eccentricity: "))
        method = input("Enter calculation method: ")
        self.controller = TwoBodyController(self.model, T, delta_t, mass_ratio, eccentricity, method)
        self.controller.run()
        self.save()

    def save(self):
        with open('positions_log.txt', 'w') as outfile:
            json.dump(astuple(self.controller.model), outfile)


if __name__ == "__main__":
    TwoBodyApp().run()
