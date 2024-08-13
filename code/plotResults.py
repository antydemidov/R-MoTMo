#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 7 13:29:07 2022

@author: gesine steudle
"""

import json
import os

import matplotlib.pyplot as plt
import numpy as np
from parameters import PlotSelection, Parameters
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


def plot_usage_per_cell(params: Parameters, time_steps, n_cells, cell_properties, cell_record,
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
        if params.save_plots:
            fig.savefig(os.path.join(
                params.plot_dir_name,
                f'plot_usage_per_cell_{coordinates[0]}_{coordinates[1]}.png'),
                        format='png')

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


def plot_population_density(params: Parameters, sim_params):
    """Builds a plot of population density."""

    fig = tools.density_plot(
        Inputs.density, title=f'Population map {sim_params["density"]}')
    if params.save_plots:
        fig.savefig(os.path.join(params.plot_dir_name,
                                 'plot_population_density.png'),
                    format='png')


def plot_convenience(params: Parameters, t, n_cells, cell_properties,
                     cell_record, mob_type):
    """Builds a plot of convenience."""

    convenience = np.zeros((x_map, y_map))
    for cell_id in range(n_cells):
        convenience[int(cell_properties[cell_id][0])][int(
            cell_properties[cell_id][1])] = cell_record[t][cell_id][mob_type]
        if mob_type == 0:
            title = 'Car conveniences'
            file_title = 'cars'
            colours = 'Blues'
        elif mob_type == 1:
            title = 'Public transport conveniences'
            file_title = 'public'
            colours = 'Greens'

    fig = tools.density_plot(convenience, title=title, cmap=colours)
    if params.save_plots:
        fig.savefig(os.path.join(params.plot_dir_name,
                                 f'plot_convenience_{file_title}.png'),
                    format='png')


def plot_usage(params: Parameters, t, n_cells, cell_properties, cell_record):
    """Builds a plot of usage."""

    car_usage = np.zeros((x_map, y_map))
    for cell_id in range(n_cells):
        car_usage[int(cell_properties[cell_id][0])][int(cell_properties[
            cell_id][1])] = cell_record[t][cell_id][2] / cell_properties[cell_id][2]

    fig = tools.density_plot(car_usage, title=f'Car usage, t={t}', cmap='Greys')
    if params.save_plots:
        fig.savefig(os.path.join(params.plot_dir_name,
                                 f'plot_usage_t={t}.png'),
                    format='png')


def plot_utility_over_time(params: Parameters, time_steps, utilities):
    """Builds a plot of utility over time."""

    time = list(range(time_steps))
    fig = plt.figure()
    plt.title('Utility over time')
    plt.plot(time, utilities)
    fig.show()
    if params.save_plots:
        fig.savefig(os.path.join(params.plot_dir_name,
                                 'plot_utility_over_time.png'),
                    format='png')


def plot_utilities_over_time(params: Parameters, time_steps, utilities,
                             utilities_car, utilities_public):
    """Builds a plot of utilities over time."""

    time = list(range(time_steps))
    fig = plt.figure()
    plt.title('Utilities over time')
    plt.plot(time, utilities)
    plt.plot(time, utilities_public)
    plt.plot(time, utilities_car)
    fig.show()
    if params.save_plots:
        fig.savefig(os.path.join(params.plot_dir_name,
                                 'plot_utilities_over_time.png'),
                    format='png')


def plot_similarity_over_time(params: Parameters, time_steps, similarity):
    """Builds a plot of similarity over time."""

    time = list(range(time_steps))
    fig = plt.figure()
    plt.title('Similarity over time')
    plt.plot(time, similarity)
    plt.show(block=True)
    if params.save_plots:
        fig.savefig(os.path.join(params.plot_dir_name,
                                 'plot_similarity_over_time.png'),
                    format='png')


# ========== plot results ==========

def plot_results(selection: PlotSelection, params: Parameters, **results):
    """Builds plots for the results."""

    if params.save_plots:
        if not os.path.exists(params.plot_dir_name):
            os.mkdir(params.plot_dir_name)
        for file in os.scandir(params.plot_dir_name):
            os.remove(file.path)

    if selection.population:
        plot_population_density(params, results['simParas'])

    if selection.conveniences_start:
        plot_convenience(params,
                         0,
                         results['nCells'],
                         results['cellProperties'],
                         results['cellRecord'],
                         mob_type=0)
        plot_convenience(params,
                         0,
                         results['nCells'],
                         results['cellProperties'],
                         results['cellRecord'],
                         mob_type=1)

    if selection.conveniences_end:
        plot_convenience(params,
                         results['endTime'],
                         results['nCells'],
                         results['cellProperties'],
                         results['cellRecord'],
                         mob_type=0)
        plot_convenience(params,
                         results['endTime'],
                         results['nCells'],
                         results['cellProperties'],
                         results['cellRecord'],
                         mob_type=1)

    for coordinates in selection.usage_per_cell:
        plot_usage_per_cell(params,
                            results['endTime']+1,
                            results['nCells'],
                            results['cellProperties'],
                            results['cellRecord'],
                            False,
                            coordinates)

    if selection.usage_maps:
        plot_usage(params,
                   0,
                   results['nCells'],
                   results['cellProperties'],
                   results['cellRecord'])
        # plot_usage(params,
        #            int(results['endTime'] / 2),
        #            results['nCells'],
        #            results['cellProperties'],
        #            results['cellRecord'])
        plot_usage(params,
                   results['endTime'],
                   results['nCells'],
                   results['cellProperties'],
                   results['cellRecord'])

    if selection.utility_over_time:
        plot_utilities_over_time(params,
                                 results['endTime'] + 1,
                                 results['globalRecord'][:, 1],
                                 results['globalRecord'][:, 2],
                                 results['globalRecord'][:, 3])

    if selection.car_usage_over_time:
        plot_utility_over_time(params,
                               results['endTime'] + 1,
                               results['globalRecord'][:, 0])

    if selection.similarity_over_time:
        plot_similarity_over_time(params,
                                  results['endTime'] + 1,
                                  results['globalRecord'][:, 4])
