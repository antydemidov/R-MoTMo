#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 7 13:29:07 2022

@author: gesine steudle
"""

from R_MoTMo.experiment import Experiment
from R_MoTMo.parameters import ExperimentParameters, Parameters, PlotSelection


# ========== USER AREA ==========
# ---------- simulation parameters ----------
params = Parameters(
    time_steps=50,
    n_friends=2,
    save_plots=False,
    save_to_csv=True
)

# ---------- choose plot types to show ----------
plot_selection = PlotSelection(
    # population=True,
    # conveniences_start=True,
    # conveniences_end=True,
    # usage_maps=True,
    # utility_over_time=True,
    # similarity_over_time=True,
    # usage_per_cell=[[5, 5]]
)

# ---------- experiment parameters ----------
exp_params = ExperimentParameters(
    n_runs=2
)

# ========== END OF USER AREA ==========


if __name__ == '__main__':
    experiment = Experiment(params, plot_selection, exp_params)
    experiment.run()
