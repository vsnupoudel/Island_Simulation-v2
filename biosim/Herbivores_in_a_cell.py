# -*- coding: utf-8 -*-

__author__ = 'bipo@nmbu.no'

from biosim.celltype import Lowland
import matplotlib.pyplot as plt

listof = [{'species': 'Herbivore',
           'age': 5,
           'weight': 25}
          for _ in range(800)]
l = Lowland(1, 1)
# place them in list in l
l.place_animals_in_list(listof)
print(0, " Year End Herb numbers :-", len(l.herb_list))

# Making figure
fig = plt.figure(figsize=(8, 6.4))
plt.plot(0, len(l.herb_list),  '*-', color='b', lw=0.5)
plt.draw()
plt.pause(0.001)

# count list
count_herb = [len(l.herb_list)]
for i in range(200):
    # grow fodder at the beginning
    l.grow_fodder_each_year()
    # make them eat
    l.make_animals_eat()
    l.make_animals_reproduce()
    # make them die
    l.make_animals_die()
    # get older and continue the cycle for next year
    l.make_animals_age()
    count_herb.append(len(l.herb_list))
    # plotting
    plt.xlim(-1, i+2)
    plt.plot(list(range(i + 2)), count_herb, '*-', color='b', lw=0.5)
    plt.draw()
    plt.pause(0.001)

plt.show()
