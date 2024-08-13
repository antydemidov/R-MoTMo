#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 7 13:29:07 2022

@author: gesine steudle
"""

import json

import matplotlib.pyplot as plt
import numpy as np
from parameters import PlotSelection
import tools
from inputs import Inputs


# ========== load results ==========
def load_results(name):
    """Loads results from files."""

    with open(name+'worldParameters.json', encoding='utf-8') as file:
        sim_params = json.load(file)
    cell_properties = np.load(name+'cellProperties.npy')
    person_properties = np.load(name+'personProperties.npy')
    n_cells = len(cell_properties)
    n_persons = len(person_properties)
    cell_record = np.load(name+'cellRecord.npy')
    person_record = np.load(name+'personRecord.npy')
    global_record = np.load(name+'globalRecord.npy')
    time_steps = len(cell_record)
    end_time = time_steps - 1
    return {
        'endTime': end_time,
        'nCells': n_cells,
        'cellProperties': cell_properties,
        'cellRecord': cell_record,
        'nPersons': n_persons,
        'personProperties': person_properties,
        'personRecord': person_record,
        'globalRecord': global_record,
        'simParas': sim_params
    }

# ========== plot functions ==========
x_map = Inputs.density.shape[0]
y_map = Inputs.density.shape[1]


def plot_usage_per_cell(time_steps, n_cells, cell_properties, cell_record,
                        all_cells=True, coordinates=None):
    """Builds plot of usage per cell."""

    if not coordinates:
        coordinates = [0, 0]
    time = list(range(time_steps))

    def plot_cell(time, users_brown, users_public):
        fig = plt.figure()
        plt.title(f'Usage in cell: [{coordinates[0]}, {coordinates[1]}]')
        plt.plot(time, users_brown)
        plt.plot(time, users_public)
        fig.show()

    for cell_id in range(n_cells):
        if all_cells:
            users_brown = [cell_record[t][cell_id][2] for t in range(time_steps)]
            users_public = [cell_record[t][cell_id][3] for t in range(time_steps)]
            plot_cell(time, users_brown, users_public)
        else:
            if (cell_properties[cell_id][0] == coordinates[0] and
                cell_properties[cell_id][1] == coordinates[1]):
                users_brown = [cell_record[t][cell_id][2]
                               for t in range(time_steps)]
                users_public = [cell_record[t][cell_id][3]
                                for t in range(time_steps)]
                plot_cell(time, users_brown, users_public)
                break


def plot_population_density(sim_params):
    """Builds a plot of population density."""

    tools.density_plot(
        Inputs.density, title=f'Population map {sim_params["density"]}')


def plot_convenience(t, n_cells, cell_properties, cell_record, mob_type):
    """Builds a plot of convenience."""

    convenience = np.zeros((x_map, y_map))
    for cell_id in range(n_cells):
        convenience[int(cell_properties[cell_id][0])][int(
            cell_properties[cell_id][1])] = cell_record[t][cell_id][mob_type]
        if mob_type == 0:
            title = 'Car conveniences'
            colours = 'Blues'
        elif mob_type == 1:
            title = 'Public transport conveniences'
            colours = 'Greens'

    tools.density_plot(convenience, title=title, cmap=colours)


def plot_usage(t, n_cells, cell_properties, cell_record):
    """Builds a plot of usage."""

    car_usage = np.zeros((x_map, y_map))
    for cell_id in range(n_cells):
        car_usage[int(cell_properties[cell_id][0])][int(cell_properties[
            cell_id][1])] = cell_record[t][cell_id][2] / cell_properties[cell_id][2]

    tools.density_plot(car_usage, title=f'Car usage, t={t}', cmap='Greys')


def plot_utility_over_time(time_steps, utilities):
    """Builds a plot of utility over time."""

    time = list(range(time_steps))
    fig = plt.figure()
    plt.title('Utility over time')
    plt.plot(time, utilities)
    fig.show()


def plot_utilities_over_time(time_steps, utilities, utilities_car, utilities_public):
    """Builds a plot of utilities over time."""

    time = list(range(time_steps))
    fig = plt.figure()
    plt.title('Utilities over time')
    plt.plot(time, utilities)
    plt.plot(time, utilities_public)
    plt.plot(time, utilities_car)
    fig.show()


def plot_similarity_over_time(time_steps, similarity):
    """Builds a plot of similarity over time."""

    time = list(range(time_steps))
    fig = plt.figure()
    plt.title('Similarity over time')
    plt.plot(time, similarity)
    fig.show()


# ========== plot results ==========

def plot_results(selection: PlotSelection, **results):
    """Builds plots for the results."""

    if selection.population:
        plot_population_density(results['simParas'])

    if selection.conveniences_start:
        plot_convenience(0,
                         results['nCells'],
                         results['cellProperties'],
                         results['cellRecord'],
                         mob_type=0)
        plot_convenience(0,
                         results['nCells'],
                         results['cellProperties'],
                         results['cellRecord'],
                         mob_type=1)

    if selection.conveniences_end:
        plot_convenience(results['endTime'],
                         results['nCells'],
                         results['cellProperties'],
                         results['cellRecord'],
                         mob_type=0)
        plot_convenience(results['endTime'],
                         results['nCells'],
                         results['cellProperties'],
                         results['cellRecord'],
                         mob_type=1)

    for coordinates in selection.usage_per_cell:
        plot_usage_per_cell(results['endTime']+1,
                            results['nCells'],
                            results['cellProperties'],
                            results['cellRecord'],
                            False,
                            coordinates)

    if selection.usage_maps:
        plot_usage(0,
                   results['nCells'],
                   results['cellProperties'],
                   results['cellRecord'])
        # plotUsage(int(results['endTime'] / 2),
        #           results['nCells'],
        #           results['cellProperties'],
        #           results['cellRecord'])
        plot_usage(results['endTime'],
                   results['nCells'],
                   results['cellProperties'],
                   results['cellRecord'])

    if selection.utility_over_time:
        plot_utilities_over_time(results['endTime'] + 1,
                                 results['globalRecord'][:, 1],
                                 results['globalRecord'][:, 2],
                                 results['globalRecord'][:, 3])

    if selection.car_usage_over_time:
        plot_utility_over_time(results['endTime'] + 1,
                               results['globalRecord'][:, 0])

    if selection.similarity_over_time:
        plot_similarity_over_time(results['endTime'] + 1,
                                  results['globalRecord'][:, 4])
