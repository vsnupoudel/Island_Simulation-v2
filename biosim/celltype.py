# -*- coding: utf-8 -*-

__author__ = 'bipo@nmbu.no'

import numpy as np
from biosim.animal import Herbivore, Carnivore


class CellType:
    _params = {'fodder': 0}

    @classmethod
    def set_parameters(cls, params):
        """Set parameters for class."""
        cls._params.update(params)

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self._herb_list = []
        self._carn_list = []
        self.fodder = self._params['fodder']

    @property
    def herb_list(self):
        return self._herb_list

    @property
    def carn_list(self):
        return self._carn_list

    def place_animals_in_list(self, list_of_diction):
        for animal in list_of_diction:
            if animal['species'] == "Herbivore":
                self._herb_list.append(Herbivore(age=animal['age'], weight=animal['weight']))
            if animal['species'] == "Carnivore":
                self._carn_list.append(Carnivore(age=animal['age'], weight=animal['weight']))

    def herbs_eat(self):
        np.random.shuffle(self._herb_list)
        for herb in self._herb_list:
            self.fodder -= herb.eat(self.fodder)

    def carns_hunt(self):
        self._herb_list.sort(key=lambda x: x.fitness())
        self._carn_list.sort(key=lambda x: x.fitness(), reverse=True)
        carns_num_eating = 0
        for anim in self._carn_list:
            dead_herbs = anim.hunts(self._herb_list)
            if len(dead_herbs) >= 1:
                carns_num_eating += 1
            self._herb_list = list(set(self._herb_list) - set(dead_herbs))
            self._herb_list.sort(key=lambda x: x.fitness())

        # print(carns_num_eating, ' out of ', len(self._carn_list), ' ate this year')

    def make_animals_eat(self):
        self.herbs_eat()
        self.carns_hunt()

    def make_animals_reproduce(self):
        newborn_list = []
        len_list = len(self._herb_list)
        for anim in self._herb_list:
            new_born = anim.gives_baby(len_list)
            if new_born is not None:
                newborn_list.append(new_born)
        self._herb_list = self._herb_list + newborn_list

        newcarn_list = []
        len_list = len(self._carn_list)
        for anim in self._carn_list:
            new_born = anim.gives_baby(len_list)
            if new_born is not None:
                newcarn_list.append(new_born)
        self._carn_list = self._carn_list + newcarn_list

    def make_animals_die(self):
        death_list = []
        for anim in self._herb_list:
            if anim.dies():
                death_list.append(anim)
        self._herb_list = list(set(self._herb_list) - set(death_list))

        carn_death_list = []
        for anim in self._carn_list:
            if anim.dies():
                carn_death_list.append(anim)
        self._carn_list = list(set(self._carn_list) - set(carn_death_list))

    def make_animals_age(self):
        for anim in self._herb_list:
            anim.get_older()
        for anim in self._carn_list:
            anim.get_older()

    def migration_prepare_cell(self): # to be called once for all cell at the beginning
        for anim in self._herb_list + self._carn_list:
            anim.has_migrated = False

    def migration_master(self, object_matrix):
        if not isinstance(self, Water):
            adjacent_cells = self.adjacent_cells( object_matrix)
            dict_of_migrants = self.emigrants_list(adjacent_cells)

            for migrating_cell, values in dict_of_migrants.items():
                if not isinstance(migrating_cell, Water) and values:
                    migrating_cell.add_immigrants(values)
                    self.remove_emigrants(values)

    def adjacent_cells(self, object_matrix):
        x = self.row
        y = self.col
        adjacent_cells = []
        for i in (-1, 1):
            adjacent_cells.append(object_matrix[x + i][y])
            adjacent_cells.append(object_matrix[x][y + i])

        return adjacent_cells

    def emigrants_list(self, adjacent_cells): #takes in adjacent cells
        dct = {}
        listofanim =  [anim for anim in self._carn_list + self._herb_list if anim.migrates() and
                       anim.has_migrated == False]
        np.random.shuffle(listofanim)
        chunks = np.array_split(np.asarray(listofanim), 4)
        for cell, animlist in zip(adjacent_cells, chunks):
            aslist = list(animlist)
            for anim in aslist:
                anim.has_migrated = True
            dct[cell] = aslist

        return dct

    def add_immigrants(self, listofanim):
        herbs = [anim for anim in listofanim if anim.__class__.__name__ == 'Herbivore']
        carns = [anim for anim in listofanim if anim.__class__.__name__ == 'Carnivore']
        self._herb_list.extend(herbs)
        self._carn_list.extend(carns)


    def remove_emigrants(self, listof):
        self._herb_list = list(set(self._herb_list) - set(listof))
        self._carn_list = list(set(self._carn_list) - set(listof))

class Water(CellType):
    is_migratable = False
    _params = {'fodder': 0}

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
    _params = {'fodder': 800}

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
    # make them eat
    l.make_animals_eat()
    # for herb in l._herb_list:
    #     print(herb.fitness(), end=',')

    # make them reproduce
    print("")
    print(len(l._herb_list))
    l.make_animals_reproduce()
    print(len(l._herb_list))

    # make them die
    l.make_animals_die()
    print(len(l._herb_list))

    # get older and continue the cycle for next year
    l.make_animals_age()
    for anim in l._herb_list:
        print(anim.age, end=',')
