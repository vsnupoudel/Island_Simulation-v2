# -*- coding: utf-8 -*-

__author__ = 'bipo@nmbu.no'

import numpy as np
import pytest


class CellType:
    pass


class Water(CellType):
    pass


class Desert(CellType):
    pass


class Lowland(CellType):
    pass


class Highland(CellType):
    pass

if __name__ == "__main__":
    a = {'foo': 1.00000000001, 'bar': 2}
    b = {'foo': 1, 'bar': 2}
    print(a == b)
    print(a== pytest.approx(b))
