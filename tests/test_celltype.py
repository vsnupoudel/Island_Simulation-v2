# -*- coding: utf-8 -*-

import pytest
from biosim.celltype import CellType
from scipy.stats import binom_test
import scipy.stats as stats

SEED = 12345678  # random seed for tests
ALPHA = 0.01  # significance level for statistical tests

