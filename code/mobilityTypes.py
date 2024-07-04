#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 13:29:07 2022

@author: gesine steudle
"""
from abc import ABC, abstractmethod

from inputs import Inputs
from tools import Tools


class MobilityType(ABC):

    @abstractmethod
    def get_convenience(self):
        pass


class CombustionCar(MobilityType):
    name = 'car'

    def __init__(self, density):
        self.density = density
        self.convenience = self.get_convenience()

    def get_convenience(self):
        mu = Inputs.pop_min
        sigma = (Inputs.pop_max - mu) / 2
        convenience = Tools.gaussian(sigma, mu, self.density) * 100
        return convenience


class PublicTransport(MobilityType):
    name = 'public'

    def __init__(self, density):
        self.density = density
        self.convenience = self.get_convenience()

    def get_convenience(self):
        mu = Inputs.pop_max
        sigma = (mu - Inputs.pop_min) / 2
        convenience = Tools.gaussian(sigma, mu, self.density) * 100
        return convenience
