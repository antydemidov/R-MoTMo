#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 7 13:29:07 2022

@author: gesine steudle
"""


from inputs import Inputs
from plotResults import load_results, plot_results
from tools import Tools
from world import World


# ========== simulation parameters ==========
parameters = {
    'timeSteps': 50,
    'density': 1,  # choose between population mpas 1,2,3,4
    'initialChoice': 1,  # choose between initial choice sets 1,2,3,4
    'nFriends': 15,
    'friendsLocally': True,
    'weightFriends': True,
    'convenienceBonus': True, 
    'convenienceMalus': True,
    'printDetails': False,
    'encoding': 'utf-8'  # use encodings from codecs library
}

parameters['simulationName'] = (
    'd'+ str(parameters['density']) +
    '-f' + str(parameters['nFriends']) +
    '-loc' + str(parameters['friendsLocally']) +
    '-bon' + str(parameters['convenienceBonus']) +
    '-mal' + str(parameters['convenienceMalus']) +
    '-'
)


# ========== choose plot types to show ==========
plot_selection = {
    'population': False,
    'conveniencesStart': False,
    'conveniencesEnd': False,
    'usageMaps': True,
    'usagePerCell': [],  # add a list of cells by coordinates, e.g. [[1, 1], [3, 4]],
    'utilityOverTime': False,
    'carUsageOverTime': False,
    'similarityOverTime': False
}


if __name__ == '__main__':
    # ========== run simulation  ==========
    world = World(parameters)
    world.run_simulation()

    # ========== plot functions ==========
    (endTime, nCells, cellProperties, cellRecord, nPersons, personProperties,
     personRecord, globalRecord, simParas) = load_results(parameters['simulationName'])

    plot_results(plot_selection,
                 endTime=endTime,
                 nCells=nCells,
                 cellProperties=cellProperties,
                 cellRecord=cellRecord,
                 nPersons=nPersons,
                 personProperties=personProperties,
                 personRecord=personRecord,
                 globalRecord=globalRecord,
                 simParas=simParas)

    densities = Inputs.density.flatten()
    utilmax = [max(Tools.gaussian((max(densities)-min(densities)) / 2,
                                  min(densities), d) * 100 + 1,
                   Tools.gaussian((max(densities)-min(densities)) / 2,
                                  max(densities), d) * 100 + 1) for d in densities]
    utilmean = sum(utilmax) / len(utilmax)
    print('Mean utility is ' + str(utilmean))
