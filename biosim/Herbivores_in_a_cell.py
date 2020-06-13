# -*- coding: utf-8 -*-
__author__ = 'bipo@nmbu.no'

from biosim.celltype import Lowland
import matplotlib.pyplot as plt
import numpy as np
np.random.seed(1)
listof = [{'species': 'Herbivore','age': 5,'weight': 20} for _ in range(50)]
listofcarns = [{'species': 'Carnivore','age': 5,'weight': 20} for _ in range(20)]
#create a Lowland Object
l = Lowland(1, 1)

# place them in list in l
l.place_animals_in_list(listof)
l.place_animals_in_list(listofcarns)

# Making figure
# fig = plt.figure(figsize=(8, 6.4))
# plt.plot(0, len(l.herb_list),  '*-', color='g', lw=0.5)
# plt.plot(0, len(l.carn_list),  '*-', color='r', lw=0.5)
# plt.draw()
# plt.pause(0.001)

# count list
count_herb = [len(l.herb_list)]
count_carn = [len(l.carn_list)]
# for i in range(10):
#     # np.random.seed(i)
for i in range(200):
    # grow fodder at the beginning
    l.grow_fodder_each_year()
    # make them eat
    l.make_animals_eat()
    # make them reproduce
    l.make_animals_reproduce()
    # get older and continue the cycle for next year
    l.make_animals_age()
    # make them die
    l.make_animals_die()

    count_herb.append(len(l.herb_list))
    count_carn.append(len(l.carn_list))
    # plotting
    # plt.plot( list(range(i + 2)),  count_herb, '*-', color='g', lw=0.5)
    # plt.plot(list(range(i + 2)), count_carn, '*-', color='r', lw=0.5)
    # plt.draw()
    # plt.pause(0.001)

    #     print(i, " Year End Herb numbers :-", len(l.herb_list))
    #     print(i, " Year End Carn numbers :-", len(l.carn_list))
    #
    # print( i, " Year End Herb numbers :-", len(l.herb_list))
    # print(i, " Year End Carn numbers :-", len(l.carn_list))

    # print('average, std herbivores , min:', np.mean(count_herb),  np.std(count_herb) ,
    #       np.min(count_herb))
    # print('average, std carnivores, min :', np.mean(count_carn) , np.std(count_carn),
    #       np.min(count_carn))
    # plt.show()


