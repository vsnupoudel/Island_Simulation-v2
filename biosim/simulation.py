# -*- coding: utf-8 -*-

__author__ = 'bipo@nmbu.no'

import numpy as np
import matplotlib.pyplot as plt
from biosim.island import Island
from biosim.visualization import Visualization
from biosim.animal import Herbivore, Carnivore
from biosim.celltype import Lowland, Highland

class BioSim:
    def __init__(self, island_map, ini_pop, seed,
        ymax_animals=None, cmax_animals=None, hist_specs=None,
        img_base=None, img_fmt='png'):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param hist_specs: Specifications for histograms, see below
        :param img_base: String with beginning of file name for figures, including path
        :param img_fmt: String with file type for figures, e.g. 'png'
        If ymax_animals is None, the y-axis limit should be adjusted automatically.
        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
        {'Herbivore': 50, 'Carnivore': 20}
        hist_specs is a dictionary with one entry per property for which a histogram shall be shown.
        For each property, a dictionary providing the maximum value and the bin width must be
        given, e.g.,
        {'weight': {'max': 80, 'delta': 2}, 'fitness': {'max': 1.0, 'delta': 0.05}}
        Permitted properties are 'weight', 'age', 'fitness'.
        If img_base is None, no figures are written to file.
        Filenames are formed as
        '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)
        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
        self.object_matrix = Island().create_map(island_map)
        self.rgb_map = Island().rgb_for_map(island_map)
        # print(self.rgb_map)
        self.add_population(ini_pop)
        self.current_year = 0
        self.x_axis_limit = 0

        # Set up visualization
        self.viz = Visualization()
        self.viz.set_plots_for_first_time(rgb_map = self.rgb_map)

    def set_animal_parameters(self, species, params):
        if species == "Herbivore":
            Herbivore.set_parameters(params)
        elif species == "Carnivore":
            Carnivore.set_parameters(params)

    def set_landscape_parameters(self, landscape, params):
        if landscape == "L":
            Lowland.set_parameters(params)
        elif landscape == "H":
            Highland.set_parameters(params)


    def simulate(self, num_years, vis_years=1, img_years=None):
        self.x_axis_limit += num_years

        for i in range(num_years):
            self.current_year += 1
            for cell in np.asarray(self.object_matrix).flatten():
                if cell.__class__.__name__  != "Water":
                    cell.grow_fodder_each_year()
                    # make them eat
                    cell.make_animals_eat()
                    # make them reproduce
                    cell.make_animals_reproduce()

            # Migration is at Island level
            Island().call_migration_helper(self.object_matrix)


            for cell in np.asarray(self.object_matrix).flatten():
                if cell.__class__.__name__ != "Water":
                    # get older and continue the cycle for next year
                    cell.make_animals_age()
                    # make them die
                    cell.make_animals_die()

            self.viz.update_plot(self.x_axis_limit,
                                 anim_distribution_dict= self.animal_distribution_in_cells
                                 , total_anim_dict= self.num_animals_per_species)
            self.viz.update_histogram(fit_list=self.fit_list, age_list= self.age_list,
                                      wt_list= self.weight_list)


        """
        Run simulation while visualizing the result.
        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)
        Image files will be numbered consecutively.
        """

    def add_population(self, population):
        """
        Add a population to the island

        :param population:  list, List of dictionaries specifying population
        """
        for one_location_list in population:
            x, y = one_location_list['loc'][0], one_location_list['loc'][1]
            self.object_matrix[x][y].place_animals_in_list(one_location_list['pop'])

    @property
    def year(self):
        """Last year simulated."""
        return self.current_year

    @property
    def fit_list(self):
        """Total number of animals on island."""
        return [ anim.fitness() for cell in np.asarray(self.object_matrix).flatten() for anim in
                 cell.herb_list+cell.carn_list ]

    @property
    def age_list(self):
        """Total number of animals on island."""
        return [anim.age for cell in np.asarray(self.object_matrix).flatten() for anim in
                cell.herb_list + cell.carn_list]

    @property
    def weight_list(self):
        """Total number of animals on island."""
        return [anim.weight for cell in np.asarray(self.object_matrix).flatten() for anim in
                cell.herb_list + cell.carn_list]

    @property
    def animal_distribution_in_cells(self):

        """        :return: A 2D list of number of animals in each cell.      """
        row_num = np.shape(self.object_matrix)[0]
        column_num = np.shape(self.object_matrix)[1]

        h_matrix = np.zeros((row_num, column_num))
        c_matrix = np.zeros((row_num, column_num))

        for cell in np.asarray(self.object_matrix).flatten():
            # print(cell.herb_list)
            h_matrix[cell.row][cell.col] = len(cell.herb_list)
            c_matrix[cell.row][cell.col] = len(cell.carn_list)

        animal_distribution_dict = {"Herbivore": h_matrix, "Carnivore": c_matrix}
        return animal_distribution_dict


    @property
    def num_animals_per_species(self):
        """
        Total number of herbivores and carnivores on island

        :return: animals_count_dict  dict, dictionary containing number of
                                     herbivores and carnivores on island
        """
        herb_total = sum( sum( self.animal_distribution_in_cells['Herbivore']))
        carn_total = sum( sum( self.animal_distribution_in_cells['Carnivore']))
        animal_count_dict = {"Herbivore": herb_total, "Carnivore": carn_total}
        return animal_count_dict

    def make_movie(self):
        pass
        """Create MPEG4 movie from visualization images saved."""

if __name__ == "__main__":
    pass
