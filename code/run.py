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
    time_steps=50
)

# ---------- choose plot types to show ----------
plot_selection = PlotSelection(
    usage_maps=True,
    usage_per_cell=[[1, 1]]
)
# ========== END OF USER AREA ==========


def main(params: Parameters, plots: PlotSelection):
    """Main function of the simulation."""
    # ---------- run simulation ----------
    world = World(params)
    world.run_simulation()

    # ---------- plot functions ----------
    results = load_results(params.simulation_name())
    plot_results(plots, **results)

    densities = Inputs.density.flatten()
    utilmax = [max(tools.gaussian((max(densities)-min(densities)) / 2,
                                min(densities), density) * 100 + 1,
                tools.gaussian((max(densities)-min(densities)) / 2,
                                max(densities), density) * 100 + 1) for density in densities]
    utilmean = sum(utilmax) / len(utilmax)
    print('Mean utility is ' + str(utilmean))


if __name__ == '__main__':
    main(parameters, plot_selection)
