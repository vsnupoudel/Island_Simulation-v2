# -*- coding: utf-8 -*-

__author__ = 'bipo@nmbu.no'

import numpy as np
import math


class Animal:
    _params = {}

    def __init__(self, age=0, weight=None):
        self.age = age
        birth_weight = np.random.normal(self._params['w_birth'], self._params['sigma_birth'])
        if weight is None:
            self.weight = birth_weight
        else:
            self.weight = weight

    def get_older(self):
        self.age += 1

    def weight_loss(self):
        self.weight *= 1. - self._params['eta']

    def _q(self, sgn, x, xhalf, phi):
        return 1. / (1. + math.exp(sgn * phi * (x - xhalf)))

    def fitness(self):
        """

        :return: fitness of the animal, value between 0 and 1
        """
        p = self._params

        if self.weight <= 0:
            return 0.
        else:
            return (self._q(+1, self.age, p['a_half'], p['phi_age']
                            ) * self._q(-1, self.weight, p['w_half'], p['phi_weight']))

    def eat(self, food_in_cell):
        """
        Eating method for each animal

        :param food_in_cell:         float, food_remaining_in_cell
        :return  eaten  :   float, food eaten by animal
        """
        if food_in_cell <= 0:
            eaten = 0
        elif food_in_cell < self._params['F']:
            eaten = food_in_cell
        else:
            eaten = self._params['F']

        self.weight += self._params['beta'] * eaten

        return eaten

    def dies(self):
        """
        :return: True if dies, false if not
        """
        fit = self.fitness()
        if fit <= 0:
            return True
        elif np.random.random() < self._params['omega'] * (1 - fit):
            return True
        else:
            return False

    def gives_baby(self, count_of_species_in_cell):
        pass


class Herbivore(Animal):
    _params = {'w_birth': 8.,
               'sigma_birth': 1.5,
               'beta': 0.9,
               'eta': 0.05,
               'a_half': 40.,
               'phi_age': 0.6,
               'w_half': 10.,
               'phi_weight': 0.1,
               'mu': 0.25,
               'gamma': 0.2,
               'zeta': 3.5,
               'xi': 1.2,
               'omega': 0.4,
               'F': 10.}

    def __init__(self, age=0, weight=None):
        super().__init__(age, weight)


class Carnivore(Animal):
    _params = {'w_birth': 6.,
               'sigma_birth': 1.0,
               'beta': 0.75,
               'eta': 0.125,
               'a_half': 40.,
               'phi_age': 0.3,
               'w_half': 4.,
               'phi_weight': 0.4,
               'mu': 0.4,
               'gamma': 0.8,
               'zeta': 3.5,
               'xi': 1.1,
               'omega': 0.8,
               'F': 50.,
               'DeltaPhiMax': 10.}

    def __init__(self, age=0, weight=None):
        super().__init__(age, weight)


if __name__ == "__main__":
    h= Herbivore()
    print(h.fitness())
    h.eat(100)
    print(h.fitness())
