# -*- coding: utf-8 -*-

__author__ = 'bipo@nmbu.no'


import numpy as np
import matplotlib.pyplot as plt


class Visualization:

    def __init__(self):
        self.steps = 0

    def set_plots_for_first_time(self, rgb_map=None, herb_htmp_data= None, carn_htmp_data=None):
        self.fig = plt.figure(figsize=(15, 10))
        plt.axis('off')
        self.fit_ax = self.fig.add_subplot(6, 3, 16)
        self.fit_ax.title.set_text('Fitness Histogram')
        self.fit_axis = None
        self.age_ax = self.fig.add_subplot(6, 3, 17)
        self.age_ax.title.set_text('Age Histogram')
        self.wt_ax = self.fig.add_subplot(6, 3, 18)
        self.wt_ax.title.set_text('Weight Histogram')

        # # The HeatMaps
        self.herb_heatmap_ax = self.fig.add_axes([0.1,0.28,0.35,0.3])  # llx, lly, w, h
        self.herb_axis = None
        self.herb_heatmap_ax.title.set_text('Herb Heatmap')
        self.herb_heatmap_ax.set_yticklabels([])
        self.herb_heatmap_ax.set_xticklabels([])

        self.carn_heatmap_ax = self.fig.add_axes([0.55,0.28,0.35,0.3])  # llx, lly, w, h
        self.carn_axis = None
        self.carn_heatmap_ax.title.set_text('Carn Heatmap')
        self.carn_heatmap_ax.set_yticklabels([])
        self.carn_heatmap_ax.set_xticklabels([])

        # The island map
        self.island_ax =  self.fig.add_axes([0.1,0.65,0.35,0.3])  # llx, lly, w, h
        self.island_ax.title.set_text('Island Map')
        self.island_ax.set_yticklabels([])
        self.island_ax.set_xticklabels([])
        # Let us create island at the beginning since it is constant
        self.island_ax.imshow(rgb_map)

        # Line plot
        self.line_ax =  self.fig.add_axes([0.55,0.65,0.35,0.3])  # llx, lly, w, h
        self.line_ax.title.set_text('Herb and Carn Count in map')
        xlim = 110; ylim = 200
        self.line_ax.set_ylim(0, ylim)  # to be passed as variable
        self.line_ax.set_xlim(0, xlim)   # to be passed as variable
        self.line_ax.set_xlabel('Years')
        self.line_ax.set_ylabel('Number of Species')
        # Now we need to store the herb line and carn line separately
        herb_plot = self.line_ax.plot(np.arange(0, xlim),
                                       np.full(xlim, np.nan),
                                       label='Herbivore')
        self.herb_line = herb_plot[0]
        carn_plot = self.line_ax.plot(np.arange(0, xlim),
                                      np.full(xlim, np.nan),
                                      label='Carnivore')
        self.carn_line = carn_plot[0]
        self.line_ax.legend(loc="upper right")

        # Age count text
        self.year_txt = self.fig.add_axes([0.45, 0.95, 0.02, 0.02])
        self.year_txt.axis('off')
        self.changing_text = self.year_txt.text(0.2, 0.5, "Year: "+str(0))

        plt.pause(1e-6)

    def update_plot(self, year, anim_distribution_dict=None, total_anim_dict= None):
        self.steps += 1
        # Changing the Year in the text
        self.changing_text.set_text( "Year: "+str(self.steps))

        # Updating the herbivore heatmap

        if self.herb_axis is None:
            self.herb_axis = self.herb_heatmap_ax.imshow(anim_distribution_dict['Herbivore'],
                                                   interpolation='nearest',
                                                   cmap="Greens", vmin=0, vmax=80)
            self.herb_heatmap_ax.figure.colorbar(self.herb_axis, ax=self.herb_heatmap_ax,
                                          orientation='horizontal',
                                          fraction=0.07, pad=0.04)
        else:
             self.herb_axis.set_data(anim_distribution_dict['Herbivore'])

        # Updating the carnivore heatmap

        if self.carn_axis is None:
            self.carn_axis = self.carn_heatmap_ax.imshow(anim_distribution_dict['Carnivore'],
                                                   interpolation='nearest',
                                                   cmap="OrRd", vmin=0, vmax=40)
            self.carn_heatmap_ax.figure.colorbar(self.carn_axis, ax=self.carn_heatmap_ax,
                                          orientation='horizontal',
                                          fraction=0.07, pad=0.04)
        else:
             self.carn_axis.set_data(anim_distribution_dict['Carnivore'])

        # Updating the line graphs
        if year < self.steps:
            self.line_ax.set_xlim(0, self.steps +year)  # to be passed as variable
        ydata = self.herb_line.get_ydata()
        ydata[year] = total_anim_dict['Herbivore']
        self.herb_line.set_ydata(ydata)
        # for carnivore now
        ydata = self.carn_line.get_ydata()
        ydata[year] = total_anim_dict['Carnivore']
        self.carn_line.set_ydata(ydata)
        plt.pause(1e-6)

    def update_histogram(self, fit_list=None, age_list= None, wt_list= None):
        self.fit_ax.clear()
        self.fit_ax.title.set_text('Fitness Histogram')
        fit_hist = self.fit_ax.hist(fit_list, bins=10, histtype='step')
        print( fit_hist[0] )

        self.age_ax.clear()
        self.age_ax.title.set_text('Age Histogram')
        self.age_ax.hist(age_list, bins=10, histtype='step')
        self.wt_ax.clear()
        self.wt_ax.title.set_text('Weight Histogram')
        self.wt_ax.hist(wt_list, bins=10, histtype='step')


