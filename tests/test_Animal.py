# -*- coding: utf-8 -*-

__author__ = 'Hans Ekkehard Plesser'
__email__ = 'hans.ekkehard.plesser@nmbu.no'

from biosim.Animal import Animals
import pytest
from unittest import TestCase


def test_syntax():
    Animals()

def test_print_animal():
    assert 1 == 2
