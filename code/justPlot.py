#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 2 10:01:57 2022

@author: gesine steudle
"""

from plotResults import load_results, plot_results


simulation_name = 'results/d1-f15-locTrue-bonTrue-malTrue-'  # directory name (if applicable) and simulation name

# ========== choose plot types to show ==========
plot_selection = {
    'population': True,
    'conveniencesStart': True,
    'conveniencesEnd': True,
    'usageMaps': True,
    'usagePerCell': [],  # add a list of cells by coordinates, e.g. [[1, 1], [3, 4]],
    'utilityOverTime': True,
    'carUsageOverTime': False,
    'similarityOverTime': False
}


if __name__ == '__main__':
    results = load_results(simulation_name)
    plot_results(plot_selection, **results)
