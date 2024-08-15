# Reduced Mobility Transition Model (R-MoTMo)

| | |
|---|---|
| **Author** | Gesine Steudle |
| **Updated by** | Anton Demidov |
| **Keywords** | socio-technical systems, mobility demand, social learning, expected utility|
| **License** | [CC-BY-4.0](http://creativecommons.org/licenses/by/4.0/) |
| **Read more** | [Reduced Mobility Transition Model (R-MoTMo) (comses.net/)](https://www.comses.net/codebases/eef9e270-909b-4832-8228-c2f3a839f171/releases/1.0.0/) |
| **Documentation** | [Reduced_MoTMo_ODD](./docs/Reduced_MoTMo_ODD.pdf) |

The Mobility Transition Model (MoTMo) is a large scale agent-based model to simulate the private mobility demand in Germany until 2035. Here, we publish a very much reduced version of this model (R-MoTMo) which is designed to demonstrate the basic modelling ideas; the aim is by abstracting from the (empirical, technological, geographical, etc.) details to examine the feed-backs of individual decisions on the socio-technical system.

## Version 1.0.0 Release Notes

In the file `run.py`, the simulation parameters can be set in `parameters` dictionary. The simulation name (part of the name of the saved result files) is created from the input parameters in `simulationName` field of `parameters`.

Run the file `run.py` to start a simulation. If `plotResults` is set `True`, the plots specified in `plot_selection` are done after the simulation is finished. (To plot results from saved files without a new simulation use the file `justPlot.py`.)

## Updated

- The code was formatted;
- The names was transformed to snake_case;
- Encoding was added to parameters dictionary;
- Tools module was updated with new methods `save_to_file` and `save_json_to_file`;
- Some code improvements;
- Added some docstrings;
- Tools were transformed from class into a set of functions;
- Added Parameters and PlotSelection classes to avoid dictionary usage;
- Added functionality to save the chart to files, use `save_plots` to save the charts;
- Experiment class was added, you can use it to run simulations more than once.

## Requirements

- [matplotlib](https://matplotlib.org/);
- [numpy](https://numpy.org/).

Use this to install requirements automatically or just install them manually:

```sh
pip install -r requirements.txt
```
