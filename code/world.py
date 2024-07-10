#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 7 13:29:07 2022

@author: gesine steudle
"""

import copy as cp
import random as rd

import numpy as np
import tools
from cell import Cell
from inputs import Inputs
# from mobilityTypes import CombustionCar
from person import Person

if __name__ == '__main__':
    print('Please, use run.py to run the simulation.')


class World:
    """Representates a simulation world, which contains cells, persons, etc."""

    # ----- Initialize -----
    def __init__(self, parameters: dict):
        self.cell_record: np.ndarray = None
        self.person_record: np.ndarray = None
        self.global_record: np.ndarray = None
        self.parameters = parameters
        self.mob_type_dict = {
            'car': 0,
            'public': 1
        }
        self.variables = {
            'carUsage': 0.5,
            'meanUtility': 0,
            'meanUtilityCar': 0,
            'meanUtilityPublic': 0,
            'meanSimilarity': parameters['nFriends'] / 2
        }

        # ----- setup simulation -----
        Cell.count = 0
        Person.count = 0
        self.population = self.init_population(parameters['density'])
        self.cells: list[Cell] = self.init_cells(self.parameters['convenienceBonus'],
                                                 self.parameters['convenienceMalus'])
        self.persons: list[Person] = self.init_persons()
        self.n_persons = len(self.persons)
        self.init_mobility_choices(parameters['initialChoice'])
        self.generate_social_network(parameters['nFriends'])
        self.finalize_init()
        self.time = 0

    def init_population(self, density_type: int):
        """Returns the chosen density."""

        density = Inputs.init_density(density_type)
        return density

    def init_cells(self, bonus: bool, malus: bool):
        """Initialize and return a list of `Cell` objects based on the population grid."""

        population = self.population
        rows, cols = len(population), len(population[0])

        cells = [
            Cell([x, y], population[x][y], bonus, malus)
            for x in range(rows)
            for y in range(cols)
        ]

        return cells

    def init_persons(self):
        """Initialize persons and distribute them across cells based on cell density."""

        persons = Inputs.create_persons()
        persons_distributed = 0

        for cell in self.cells:
            density = cell.final['density']
            cell.persons = persons[persons_distributed : persons_distributed + density]

            for person in cell.persons:
                person.cell = cell

            persons_distributed += density

        return persons

    def generate_social_network(self, n_friends: int):
        """Generates friends network for all persons."""

        for person in self.persons:
            persons = cp.copy(self.persons)
            persons.remove(person)
            person.generate_friends(persons,
                                    n_friends,
                                    self.parameters['friendsLocally'])

    def init_mobility_choices(self, init_choice: int):
        """Creates mobility choices."""

        if init_choice == 1:
            mob_types = Inputs.init_choice_1
        elif init_choice == 2:
            mob_types = Inputs.init_choice_2
        elif init_choice == 3:
            mob_types = Inputs.init_choice_3
        else:
            mob_types = []
            for _ in range(len(self.persons)):
                mob_types.append(rd.randint(0, 1))
        for p, person in enumerate(self.persons):
            person.variable['mobilityType'] = mob_types[p]
            person.new_mobility_type = mob_types[p]
            person.update_utility()

    def finalize_init(self):
        """
        Creates data structures for the variables and constants of all object
        and saves them.
        """

        name = self.parameters['simulationName']
        cell_properties = np.zeros((len(self.cells), Cell.final_attributes))
        person_properties = np.zeros((len(self.persons), Person.final_attributes))
        mobility_types = {}
        for key, value in self.mob_type_dict.items():
            mobility_types[value] = key

        tools.save_json_to_file(name+'mobilityTypes.json',
                                mobility_types, self.parameters['encoding'])

        for person in self.persons:
            for k, key in enumerate(person.final.keys()):
                person_properties[person.id][k] = person.final[key]
        persons_in_cell = {}
        for cell in self.cells:
            persons_in_cell[cell.id] = [person.id for person in cell.persons]
            for k, key in enumerate(cell.final.keys()):
                cell_properties[cell.id][k] = cell.final[key]

        tools.save_json_to_file(name+'personsInCell.json',
                                persons_in_cell, self.parameters['encoding'])

        np.save(name+'cellProperties', cell_properties)
        np.save(name+'personProperties', person_properties)

        tools.save_json_to_file(name+'worldParameters.json',
                                self.parameters, self.parameters['encoding'])
    # -- End Init -----


    # ----- Run and Save -----
    def run_simulation(self):
        """Runs the simulation."""

        time_steps = self.parameters['timeSteps']
        name = self.parameters['simulationName']

        self.cell_record = np.zeros((time_steps,
                                     len(self.cells),
                                     Cell.variable_attributes), dtype=float)
        self.person_record = np.zeros((time_steps,
                                       len(self.persons),
                                       Person.variable_attributes), dtype=float)
        self.global_record = np.zeros((time_steps,
                                       len(self.variables),
                                       2), dtype=float)

        for time in range(0, time_steps):
            self.time = time
            self.step(time)

        np.save(name+'cellRecord', self.cell_record)
        np.save(name+'personRecord', self.person_record)
        np.save(name+'globalRecord', self.global_record)
    # -- End Run and Save -----


    # ----- World Time Step -----
    def step(self, time: int):
        """Moves the model to the next step."""

        utilities = []
        utilities_car = []
        utilities_public = []
        similar_list = []

        if time > 0:
            for person in self.persons:
                person.update_mobility_type()

        for cell in self.cells:
            cell.step()
            for k, key in enumerate(cell.variable.keys()):
                self.cell_record[self.time][cell.id][k] = cell.variable[key]

                if self.parameters['printDetails']:
                    print("In cell #" + str(cell.id) + " is car convenience " +
                          str(cell.variable['convenienceCar']) +
                          " and public transport convenience " +
                          str(cell.variable['conveniencePublic']))

        for person in self.persons:
            person.update_utility()

        for person in self.persons:
            person.step(self.parameters['weightFriends'])

            # --- calculate global record ---
            for k, key in enumerate(person.variable.keys()):
                self.person_record[self.time][person.id][k] = person.variable[key]
            utilities.append(person.variable['utility'])
            if person.variable['mobilityType']:
                utilities_public.append(person.variable['utility'])
            else:
                utilities_car.append(person.variable['utility'])
            friends_mob_types = [friend.variable['mobilityType']
                                 for friend in person.friends]
            similar = friends_mob_types.count(person.variable['mobilityType'])
            similar_list.append(similar)

        # --- save global record ---
        self.variables['meanUtility'] = np.mean(utilities)
        self.variables['meanUtilityCar'] = np.mean(utilities_car)
        self.variables['meanUtilityPublic'] = np.mean(utilities_public)
        self.variables['carUsage'] = len(utilities_car)/self.n_persons
        self.variables['meanSimilarity'] = np.mean(similar_list)
        for k, key in enumerate(self.variables.keys()):
            self.global_record[self.time][k] = self.variables[key]
    # ----- End Time Step -----
