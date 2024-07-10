#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 7 13:29:07 2022

@author: gesine steudle
"""

from abc import ABC, abstractmethod

import tools
from inputs import Inputs


class MobilityType(ABC):
    """Base class for all kinds of Mobility Types."""

    @abstractmethod
    def get_convenience(self):
        pass


class CombustionCar(MobilityType):
    """Representation of a Combustion Car."""
    name = 'car'

    def __init__(self, density):
        self.density = density
        self.convenience = self.get_convenience()

    def get_convenience(self):
        mu = Inputs.pop_min
        sigma = (Inputs.pop_max - mu) / 2
        convenience = tools.gaussian(sigma, mu, self.density) * 100
        return convenience


class PublicTransport(MobilityType):
    """Representation of a Public Transport"""
    name = 'public'

    def __init__(self, density):
        self.density = density
        self.convenience = self.get_convenience()

    def get_convenience(self):
        mu = Inputs.pop_max
        sigma = (mu - Inputs.pop_min) / 2
        convenience = tools.gaussian(sigma, mu, self.density) * 100
        return convenience
