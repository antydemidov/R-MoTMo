#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 2 10:01:57 2022

@author: gesine steudle
"""

from plotResults import load_results, plot_results
from parameters import PlotSelection, Parameters


# ========== USER AREA ==========
simulation_name = 'results/d1-f15-locTrue-bonTrue-malTrue-'  # directory name (if applicable) and simulation name
params = Parameters(
    save_plots=False
)

# ---------- choose plot types to show ----------
plot_selection = PlotSelection(
    population=True,
    conveniences_start=False,
    conveniences_end=False,
    usage_maps=False,
    usage_per_cell=[],
    utility_over_time=False,
    car_usage_over_time=False,
    similarity_over_time=False
)
# ========== END OF USER AREA ==========


if __name__ == '__main__':
    results = load_results(simulation_name)
    plot_results(plot_selection, params, **results)
