#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 13:29:07 2022

@author: gesine steudle
"""

import json

import matplotlib.pyplot as plt
import numpy as np
from inputs import Inputs
from tools import Tools


# ========== load results ==========
def load_results(name):
    with open(name+'worldParameters.json', encoding='utf-8') as file:
        sim_paras = json.load(file)
    cell_properties = np.load(name+'cellProperties.npy')
    person_properties = np.load(name+'personProperties.npy')
    n_cells = len(cell_properties)
    n_persons = len(person_properties)
    cell_record = np.load(name+'cellRecord.npy')
    person_record = np.load(name+'personRecord.npy')
    global_record = np.load(name+'globalRecord.npy')
    time_steps = len(cell_record)
    end_time = time_steps - 1
    return (end_time, n_cells, cell_properties, cell_record, n_persons,
            person_properties, person_record, global_record, sim_paras)

# ========== plot functions ==========
x_map = Inputs.density.shape[0]
y_map = Inputs.density.shape[1]


def plot_usage_per_cell(time_steps, n_cells, cell_properties, cell_record,
                        all_cells=True, coordinates=[0, 0]):
    time = list(range(time_steps))

    def plot_cell(time, users_brown, users_public):
        fig = plt.figure()
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


def plot_population_density(simParas):
    Tools.density_plot(
        Inputs.density, title='population map ' + str(simParas['density']))


def plot_convenience(t, n_cells, cell_properties, cell_record, mob_type):
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
    Tools.density_plot(convenience, title=title, cmap=colours)


def plot_usage(t, n_cells, cell_properties, cell_record):
    car_usage = np.zeros((x_map, y_map))
    for cell_id in range(n_cells):
        car_usage[int(cell_properties[cell_id][0])][int(
            cell_properties[cell_id][1])] = cell_record[t][cell_id][2] / cell_properties[cell_id][2]
    Tools.density_plot(car_usage, title="Car usage, t=" + str(t), cmap="Greys")


def plot_utility_over_time(time_steps, utilities):
    time = [t for t in range(time_steps)]
    fig = plt.figure()
    plt.plot(time, utilities)
    fig.show()


def plot_utilities_over_time(time_steps, utilities, utilities_car, utilities_public):
    time = list(range(time_steps))
    fig = plt.figure()
    plt.plot(time, utilities)
    plt.plot(time, utilities_public)
    plt.plot(time, utilities_car)
    fig.show()


def plot_similarity_over_time(time_steps, similarity):
    time = list(range(time_steps))
    fig = plt.figure()
    plt.plot(time, similarity)
    fig.show()


# ========== plot results ==========

def plot_results(selection, **results):

    if selection['population']:
        plot_population_density(results['simParas'])

    if selection['conveniencesStart']:
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

    if selection['conveniencesEnd']:
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

    for coordinates in selection['usagePerCell']:
        plot_usage_per_cell(results['endTime']+1,
                            results['nCells'],
                            results['cellProperties'],
                            results['cellRecord'],
                            False,
                            coordinates)

    if selection['usageMaps']:
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

    if selection['utilityOverTime']:
        plot_utilities_over_time(results['endTime'] + 1,
                                 results['globalRecord'][:, 1],
                                 results['globalRecord'][:, 2],
                                 results['globalRecord'][:, 3])

    if selection['carUsageOverTime']:
        plot_utility_over_time(results['endTime'] + 1,
                               results['globalRecord'][:, 0])

    if selection['similarityOverTime']:
        plot_similarity_over_time(results['endTime'] + 1,
                                  results['globalRecord'][:, 4])
