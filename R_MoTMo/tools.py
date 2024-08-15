#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 7 13:29:07 2022

@author: gesine steudle
"""

import csv
import json
import math
import os

import matplotlib.pyplot as plt


def create_dir(filename):
    """Checks if a directory exists and creates it if it doesn't exist."""

    dir_name = os.path.dirname(filename)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def gaussian(sigma, mu, rho):
    """Calculates gaussian distribution."""

    return math.exp(((rho - mu) / sigma) ** 2 / (-2)) / math.sqrt(2 * math.pi * sigma**2)


def density_plot(density, title="Density Plot", cmap="Oranges"):
    """Creates a density plot."""

    fig = plt.figure()
    plt.imshow(density, cmap)
    plt.title(title)
    plt.colorbar()
    plt.show()
    return fig


def euclidean_distance(coordinates_a, coordinates_b):
    """Calculates the euclidian distance between two points."""

    return math.sqrt((coordinates_a[0] - coordinates_b[0]) ** 2 +
                        (coordinates_a[1] - coordinates_b[1]) ** 2)


def normalize(array):
    """Normalizes the array."""

    sum_array = sum(array)
    return [element / sum_array for element in array]


def save_to_file(filename: str, content: str, encoding: str = 'utf-8'):
    """Saves the contents to the specified file."""

    create_dir(filename)
    with open(filename, 'w', encoding=encoding) as f:
        f.write(content)


def save_json_to_file(filename: str, content, encoding: str = 'utf-8'):
    """Saves the contents to the specified file."""

    assert filename.endswith('.json')
    create_dir(filename)
    with open(filename, 'w', encoding=encoding) as f:
        json.dump(content, f)

def export_to_csv_by_runs(data: dict, name: str, encoding: str = 'utf-8'):

    global_record = data['globalRecord']
    cell_record = data['cellRecord']
    person_record = data['personRecord']

    global_variables = [
        'carUsage',
        'meanUtility',
        'meanUtilityCar',
        'meanUtilityPublic',
        'meanSimilarity'
    ]

    cell_variables = [
        'convenienceCar',
        'conveniencePublic',
        'usageCar',
        'usagePublic'
    ]

    person_variables = [
        'mobilityType',
        'utility'
    ]

    with open(name+'globalRecordByRuns.csv', 'w', encoding=encoding) as file:
        csv_writer = csv.writer(file, lineterminator='\n')
        csv_writer.writerow(['run', 'step', 'variable', 'value'])
        for run, run_values in enumerate(global_record):
            for step, values in enumerate(run_values):
                for i, key in enumerate(global_variables):
                    csv_writer.writerow([run, step, key, values[i]])

    with open(name+'cellRecordByRuns.csv', 'w', encoding=encoding) as file:
        csv_writer = csv.writer(file, lineterminator='\n')
        csv_writer.writerow(['run', 'step', 'cell', 'variable', 'value'])
        for run, run_values in enumerate(cell_record):
            for step, row in enumerate(run_values):
                for cell, values in enumerate(row):
                    for i, key in enumerate(cell_variables):
                        csv_writer.writerow([run, step, cell, key, values[i]])

    with open(name+'personRecordByRuns.csv', 'w', encoding=encoding) as file:
        csv_writer = csv.writer(file, lineterminator='\n')
        csv_writer.writerow(['run', 'step', 'person', 'variable', 'value'])
        for run, run_values in enumerate(person_record):
            for step, row in enumerate(run_values):
                for person, values in enumerate(row):
                    for i, key in enumerate(person_variables):
                        csv_writer.writerow([run, step, person, key, values[i]])

def export_to_csv(data: dict, name: str, encoding: str = 'utf-8'):

    global_record = data['globalRecord']
    cell_record = data['cellRecord']
    person_record = data['personRecord']

    global_variables = [
        'carUsage',
        'meanUtility',
        'meanUtilityCar',
        'meanUtilityPublic',
        'meanSimilarity'
    ]

    cell_variables = [
        'convenienceCar',
        'conveniencePublic',
        'usageCar',
        'usagePublic'
    ]

    person_variables = [
        'mobilityType',
        'utility'
    ]

    with open(name+'globalRecord.csv', 'w', encoding=encoding) as file:
        csv_writer = csv.writer(file, lineterminator='\n')
        csv_writer.writerow(['step', 'variable', 'value'])
        for step, values in enumerate(global_record):
            for i, key in enumerate(global_variables):
                csv_writer.writerow([step, key, values[i]])

    with open(name+'cellRecord.csv', 'w', encoding=encoding) as file:
        csv_writer = csv.writer(file, lineterminator='\n')
        csv_writer.writerow(['step', 'cell', 'variable', 'value'])
        for step, row in enumerate(cell_record):
            for cell, values in enumerate(row):
                for i, key in enumerate(cell_variables):
                    csv_writer.writerow([step, cell, key, values[i]])

    with open(name+'personRecord.csv', 'w', encoding=encoding) as file:
        csv_writer = csv.writer(file, lineterminator='\n')
        csv_writer.writerow(['step', 'person', 'variable', 'value'])
        for step, row in enumerate(person_record):
            for person, values in enumerate(row):
                for i, key in enumerate(person_variables):
                    csv_writer.writerow([step, person, key, values[i]])

    # 'endTime'
    # 'nCells'
    # 'cellProperties'
    # 'cellRecord'
    # 'nPersons'
    # 'personProperties'
    # 'personRecord'
    # 'globalRecord'
    # 'simParams'
