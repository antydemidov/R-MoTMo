#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 13:29:07 2022

@author: gsteudle
"""

import json
import math

import matplotlib.pyplot as plt


class Tools:
    def gaussian(sigma, mu, rho):
        return math.exp(((rho - mu) / sigma) ** 2 / (-2)) / math.sqrt(2 * math.pi * sigma**2)

    def density_plot(density, title="Density Plot", cmap="Oranges"):
        plt.figure()
        plt.imshow(density, cmap)
        plt.title(title)
        plt.colorbar()
        plt.show()

    def euclidean_distance(coordinates_a, coordinates_b):
        return math.sqrt((coordinates_a[0] - coordinates_b[0]) ** 2 +
                         (coordinates_a[1] - coordinates_b[1]) ** 2)

    def normalize(array):
        sum_array = sum(array)
        return [element / sum_array for element in array]

    def save_to_file(filename: str, content: str, encoding: str = 'utf-8'):
        """Saves the contents to the specified file."""
        with open(filename, 'w', encoding=encoding) as f:
            f.write(content)

    def save_json_to_file(filename: str, content, encoding: str = 'utf-8'):
        """Saves the contents to the specified file."""
        assert filename.endswith('.json')
        with open(filename, 'w', encoding=encoding) as f:
            json.dump(content, f)
