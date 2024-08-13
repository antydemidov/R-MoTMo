#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 7 13:29:07 2022

@author: gesine steudle
"""

from parameters import Parameters, PlotSelection
import tools
from inputs import Inputs
from plotResults import load_results, plot_results
from world import World


# ========== USER AREA ==========
# ---------- simulation parameters ----------
parameters = Parameters(
    time_steps=50,
    save_plots=True
)

# ---------- choose plot types to show ----------
plot_selection = PlotSelection(
    population=True,
    conveniences_start=True,
    conveniences_end=True,
    usage_maps=True,
    utility_over_time=True,
    car_usage_over_time=True,
    similarity_over_time=True,
    usage_per_cell=[[1, 1], [1, 3]]
)
# ========== END OF USER AREA ==========


def main(params: Parameters, plots: PlotSelection):
    """Main function of the simulation."""
    # ---------- run simulation ----------
    world = World(params)
    world.run_simulation()

    # ---------- plot functions ----------
    results = load_results(params.simulation_name())
    plot_results(plots, params, **results)

    densities = Inputs.density.flatten()
    utilmax = [max(tools.gaussian((max(densities)-min(densities)) / 2,
                                min(densities), density) * 100 + 1,
                tools.gaussian((max(densities)-min(densities)) / 2,
                                max(densities), density) * 100 + 1) for density in densities]
    utilmean = sum(utilmax) / len(utilmax)
    print('Mean utility is ' + str(utilmean))


if __name__ == '__main__':
    main(parameters, plot_selection)
