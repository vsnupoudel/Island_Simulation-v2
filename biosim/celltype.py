# -*- coding: utf-8 -*-

__author__ = 'bipo@nmbu.no'

import numpy as np
import pytest
from biosim.animal import Herbivore, Carnivore


class CellType:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.herb_list = []
        self.carn_list = []

    def place_animals_in_list(self, list_of_diction):
        for animal in list_of_diction:
            if animal['species'] == "Herbivore":
                self.herb_list.append(Herbivore(age=animal['age'], weight=animal['weight']))
            if animal['species'] == "Carnivore":
                self.herb_list.append(Herbivore(age=animal['age'], weight=animal['weight']))

    def herbs_eat(self):
        np.random.shuffle(self.herb_list)
        for herb in self.herb_list:
            self.fodder -= herb.eat(self.fodder)

    def carns_hunt(self):
        pass

    def make_animals_eat(self):
        self.herbs_eat()
        self.carns_hunt()

    def make_animals_reproduce(self):
        newborn_list = []
        len_list = len(self.herb_list)
        for anim in self.herb_list:
            new_born = anim.gives_baby(len_list)
            if new_born is not None:
                newborn_list.append(new_born)
        self.herb_list = self.herb_list + newborn_list

    def make_animals_die(self):
        death_list = []
        for anim in self.herb_list:
            if anim.dies():
                death_list.append(anim)
        self.herb_list = list( set(self.herb_list) - set(death_list) )

    def make_animals_age(self):
        for anim in self.herb_list:
            anim.get_older()


class Water(CellType):
    is_migratable = False

    def __init__(self, row, col):
        super().__init__(row, col)



class Desert(CellType):
    is_migratable = True
    _params = {'fodder': 0}

    def __init__(self, row, col):
        super().__init__(row, col)
        self.fodder = self._params['fodder']

    def grow_fodder_each_year(self):
        self.fodder = self._params['fodder']


class Lowland(CellType):
    is_migratable = True
    _params = {'fodder':800}

    def __init__(self, row, col):
        super().__init__(row, col)
        self.fodder = self._params['fodder']

    def grow_fodder_each_year(self):
        self.fodder = self._params['fodder']


class Highland(CellType):
    is_migratable = True
    _params = {'fodder': 300}

    def __init__(self, row, col):
        super().__init__(row, col)
        self.fodder = self._params['fodder']

    def grow_fodder_each_year(self):
        self.fodder = self._params['fodder']


if __name__ == "__main__":
    listof = [{'species': 'Herbivore',
               'age': 5,
               'weight': 25}
              for _ in range(150)]
    l = Lowland(1, 1)
    print(l.fodder)
    # place them in list
    l.place_animals_in_list(listof)
    # for herb in l.herb_list:
    #     print(herb.fitness(), end=',')
    # make them eat
    l.make_animals_eat()
    # for herb in l.herb_list:
    #     print(herb.fitness(), end=',')

    # make them reproduce
    print("")
    print(len(l.herb_list))
    l.make_animals_reproduce()
    print(len(l.herb_list))

    # make them die
    l.make_animals_die()
    print(len(l.herb_list))

    # get older and continue the cycle for next year
    l.make_animals_age()
    for anim in l.herb_list:
        print(anim.age, end=',')
