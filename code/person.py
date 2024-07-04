#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 13:29:07 2022

@author: gesine steudle
"""

import numpy as np
from tools import Tools


class Person:
    count = 0
    final_attributes = 0
    variable_attributes = 2

    def __init__(self):
        self.id = self.create_id()
        self.final = {}
        self.variable: dict = {'mobilityType': None, 'utility': 2.0}
        self.cell = None
        self.friends: list[Person] = []
        self.friend_weights = []
        self.utility_weights = [1.]
        self.last_copied = None
        self.last_utility = self.variable['utility']
        self.new_mobility_type = self.variable['mobilityType']

    # ----- Init Functions-----
    def create_id(self):
        _id = Person.count
        Person.count += 1
        return _id

    def generate_friends(self, persons: list, n_friends: int, friends_locally: bool):
        if friends_locally:
            measures = [1 / (Tools.euclidean_distance(self.cell.coordinates,
                             person.cell.coordinates) + 0.1) for person in persons]
        else:
            measures = [1 for _ in persons]
        probabilities = Tools.normalize(measures)
        self.friends = np.random.choice(persons, size=n_friends,
                                        replace=False, p=probabilities)
        self.friend_weights = np.ones(n_friends)
    # ----- End Init -----

    def return_convenience(self) -> float:
        convenience = 0.
        if self.variable['mobilityType'] == 0:
            convenience = self.cell.variable['convenienceCar']
        elif self.variable['mobilityType'] == 1:
            convenience = self.cell.variable['conveniencePublic']
        return convenience

    def update_mobility_type(self):
        self.variable['mobilityType'] = self.new_mobility_type

    def update_utility(self):
        self.last_utility = self.variable['utility']
        self.variable['utility'] = self.return_convenience()

    def imitate(self):
        friend_utilities = [friend.variable['utility']
                            for friend in self.friends]
        probabilities_raw = [friend_utilities[i] * self.friend_weights[i]
                             for i in range(len(self.friends))]
        probabilities = Tools.normalize(probabilities_raw)
        self.last_copied = np.random.choice(self.friends, 1, p=probabilities)[0]

    def weight_connections(self, time: int = 0):
        if self.last_copied is not None:
            change = 1 + (self.variable['utility'] - self.last_utility) / self.last_utility
            friend_copied = self.last_copied
            self.friend_weights[np.where(self.friends == friend_copied)] *= change

    def choose_new_mobility_type(self):
        if self.last_copied.variable['utility'] <= self.variable['utility']:
            self.last_copied = None
        else:
            self.new_mobility_type = self.last_copied.variable['mobilityType']

    def step(self, time: int, weight_friends: bool):
        if weight_friends:
            self.weight_connections(time)
        self.imitate()
        self.choose_new_mobility_type()
