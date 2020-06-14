# -*- coding: utf-8 -*-

__author__ = 'bipo@nmbu.no'

import numpy as np
from biosim.celltype import Water, Desert, Lowland, Highland


class Island:

    def create_map(self, geo_matrix_input_string):
        valid_landscape_list = ['W', 'L', 'H', 'D']
        lines = geo_matrix_input_string.splitlines()
        geo_list = [list(_) for _ in lines]  # each letter separated
        # print( list( set(np.asarray(geo_list).flatten()) ))
        geo_shape = np.shape(geo_list)

        # check if input characters are valid letters
        if  not set(np.asarray(geo_list).flatten()).issubset( set(valid_landscape_list ) ):
            raise ValueError(" Invalid Letters in the Input map ")
        # Check if all rows in map have equal length
        elif len(set([len(_) for _ in lines])) > 1:
            raise ValueError("The length of rows not equal")
        # check that water W is around all edges of map
        left_right = [row[0] for row in lines] + [row[-1] for row in lines]
        top_bottom = geo_list[0] + geo_list[-1]
        if set(top_bottom + left_right) != {'W'}:
            raise ValueError("Ocean not on the edges")

        object_matrix = []
        # Change the letters in Map to corresponding Objects
        dict_maps = {'W': Water, 'L': Lowland, 'H': Highland, 'D': Desert}
        for row_num in range(geo_shape[0]):
            object_matrix.append(
                [dict_maps[geo_list[row_num][column]](row_num, column)
                 for column in range(geo_shape[1])])

        return object_matrix

    def rgb_for_map(self, input_raw_string):
        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                     'L': (0.0, 0.6, 0.0),  # dark green
                     'H': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        kart_rgb = [[rgb_value[column] for column in row]
                    for row in input_raw_string.splitlines()]

        return kart_rgb

    def call_migration_helper(self, object_matrix):
        for cell in np.asarray(object_matrix).flatten():
            for anim in cell.herb_list + cell.carn_list:
                anim.has_migrated = False

        for cell in np.asarray(object_matrix).flatten():
            if cell.__class__.__name__ != 'Water':
                adjacent_cells = self.adjacent_cells(cell, object_matrix)
                dict_of_migrants = cell.emigrants_list(adjacent_cells)
                for key, values in dict_of_migrants.items():
                    if key.__class__.__name__ != 'Water' and values:
                        key.add_immigrants(values)
                        cell.remove_emigrants(values)

    @staticmethod
    def adjacent_cells( cell, object_matrix):
        x = cell.row;
        y = cell.col
        adjacent_cells = []
        for i in (-1, 1):
            adjacent_cells.append(object_matrix[x + i][y])
            adjacent_cells.append(object_matrix[x][y + i])
        return adjacent_cells


if __name__ == "__main__":
    f= ['L', 'H', 'W']
    g =  ['W', 'L', 'H', 'D']
    print( set(f) in set(g))

    # a = np.arange(201)
    # print(len(a))
    # chunks = np.array_split(a, 4)
    # for i , lists in  zip( np.arange(4) ,chunks):
    #     print(i, list(lists))
    #     print(type(list(lists)))
    # print(chunks)




