#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 7 13:29:07 2022

@author: gesine steudle
"""

from dataclasses import dataclass, field


@dataclass
class Parameters:
    """Parameters for the simulation."""

    time_steps: int = 50
    """Number of time steps."""
    density: int = 1
    """Choose between population maps 1, 2, 3, 4."""
    initial_choice: int = 1
    """Choose between initial choice sets 1, 2, 3, 4."""
    n_friends: int = 15
    """Number of person's friends."""
    friends_locally: bool = True
    weight_friends: bool = True
    convenience_bonus: bool = True
    convenience_malus: bool = True
    print_details: bool = False
    encoding: str = 'utf-8'
    """Use encodings from codecs library."""
    dir_name: str = 'results/'
    """Directory name for results files."""

    def simulation_name(self):
        """Returns the name of the simulation."""
        assert self.dir_name.endswith('/')
        return (
            self.dir_name
            + 'd'+ str(self.density)
            + '-f' + str(self.n_friends)
            + '-loc' + str(self.friends_locally)
            + '-bon' + str(self.convenience_bonus)
            + '-mal' + str(self.convenience_malus)
            + '-'
        )


@dataclass
class PlotSelection:
    """Selection of plots to show."""

    population: bool = False
    conveniences_start: bool = False
    conveniences_end: bool = False
    usage_maps: bool = False
    utility_over_time: bool = False
    car_usage_over_time: bool = False
    similarity_over_time: bool = False
    usage_per_cell: list[int] = field(default_factory=list)
    """Add a list of cells by coordinates, e.g. [[1, 1], [3, 4]]"""
