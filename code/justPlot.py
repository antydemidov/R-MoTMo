#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 10:01:57 2022

@author: gesine
"""


from plotResults import load_results, plot_results

simulation_name = ''

plotSelection = {
    'population': True,
    'conveniencesStart': True,
    'conveniencesEnd': True,
    'usageMaps': True,
    'usagePerCell': [[0, 0], [2, 2]],
    'utilityOverTime': True
}


(endTime, nCells, cellProperties, cellRecord, nPersons, personProperties,
 personRecord, globalRecord, simParas) = load_results(simulation_name)

plot_results(plotSelection, endTime=endTime, nCells=nCells,
            cellProperties=cellProperties, cellRecord=cellRecord,
            nPersons=nPersons, personProperties=personProperties,
            personRecord=personRecord, globalRecord=globalRecord,
            simParas=simParas)
