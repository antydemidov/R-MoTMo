#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 7 09:03:57 2021

@author: gesine steudle
"""

from mobilityTypes import CombustionCar, PublicTransport
from person import Person


if __name__ == '__main__':
    print('Please, use run.py to run the simulation.')


class Cell():
    """Representation of cells of the World."""

    count = 0
    final_attributes = 3
    variable_attributes = 4

    def __init__(self, coordinates, density, bonus: bool, malus: bool):
        self.id = self.create_id()
        self.public_transport = PublicTransport(density)
        self.combustion_car = CombustionCar(density)
        self.bonus = bonus
        self.malus = malus
        self.infra_car = 0
        self.infra_public = 0
        self.final = {'x': coordinates[0],
                      'y': coordinates[1],
                      'density': density}
        self.variable = {'convenienceCar': self.combustion_car.convenience,
                         'conveniencePublic': self.public_transport.convenience,
                         'usageCar': 0,
                         'usagePublic': 0}
        self.persons: list[Person] = []
        self.coordinates = coordinates

    def create_id(self):
        """Creates an ID for the Person."""

        _id = Cell.count
        Cell.count += 1
        return _id

    def update_malus(self, proportion) -> int | float:
        """Updates malus."""

        if self.malus:
            factor = 1 - proportion / 3
        else:
            factor = 1
        return factor

    def update_conveniences(self):
        """Updates conveniences."""

        car_proportion = self.variable['usageCar'] / self.final['density']
        public_proportion = self.variable['usagePublic'] / self.final['density']
        if self.bonus:
            self.infra_car = (self.infra_car * 2 + car_proportion) / 3
            self.infra_public = (self.infra_public * 2 + public_proportion) / 3
        self.variable['convenienceCar'] = self.update_malus(
            car_proportion) * self.combustion_car.convenience + self.infra_car
        self.variable['conveniencePublic'] = self.update_malus(
            public_proportion) * self.public_transport.convenience + self.infra_public

    def step(self):
        """Moves the model to the next step."""

        usage_car, usage_public = 0, 0
        for person in self.persons:
            if person.variable['mobilityType']:
                usage_public += 1
            else:
                usage_car += 1
        self.variable['usageCar'] = usage_car
        self.variable['usagePublic'] = usage_public
        self.update_conveniences()
