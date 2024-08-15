#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 2 10:01:57 2022

@author: gesine steudle
"""

from R_MoTMo.plotResults import load_results, plot_results
from R_MoTMo.parameters import PlotSelection, Parameters


# ========== USER AREA ==========
SIMULATION_NAME = 'results/d1-f15-locTrue-bonTrue-malTrue/'  # directory name (if applicable) and simulation name
params = Parameters(
    save_plots=False,
    plot_dir_name='plots'
    # Don't use any other parameters, they don't matter for plots
)

# ---------- choose plot types to show ----------
plot_selection = PlotSelection(
    population=True,
    conveniences_start=False,
    conveniences_end=False,
    usage_maps=False,
    usage_per_cell=[[1, 1]],
    utility_over_time=False,
    similarity_over_time=False
)
# ========== END OF USER AREA ==========


if __name__ == '__main__':
    results = load_results(SIMULATION_NAME)
    plot_results(plot_selection, params, **results)
