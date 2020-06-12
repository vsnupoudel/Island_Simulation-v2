# -*- coding: utf-8 -*-

import pytest
from biosim.animal import Herbivore
from scipy.stats import binom_test
import scipy.stats as stats

SEED = 12345678  # random seed for tests
ALPHA = 0.01  # significance level for statistical tests


class TestAnimal:

    @pytest.fixture(autouse=True)
    def create_herb(self):
        """Creates a Herbivore object"""
        self.herb1 = Herbivore(5, 10)
        self.herb2 = Herbivore(5, 10)
        _w = Herbivore._params['zeta'] * (Herbivore._params['w_birth'] +
                                          Herbivore._params['sigma_birth'])
        self.enuf_weight_for_mum = _w
        self.mum_check_herb = Herbivore(5, self.enuf_weight_for_mum)
        self.death_prob_herb1 = Herbivore._params['omega'] * (1 - self.herb1.fitness())

    def test_animal_fitness(self):
        f1 = self.herb1.fitness()
        f2 = self.herb2.fitness()
        assert f1 == pytest.approx(f2), "fitness should be same for same age and weight"

    def test_animal_dies(self):
        death_prob = self.death_prob_herb1
        print('\n\n Death Probability: ', death_prob)
        N = 500
        n_deaths = sum(self.herb1.dies() for _ in range(N))
        print("Number of deaths:", n_deaths)

        assert binom_test(n_deaths, N, death_prob) > ALPHA
