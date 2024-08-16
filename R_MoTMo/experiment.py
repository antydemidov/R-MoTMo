import numpy as np
from R_MoTMo import tools

from R_MoTMo.parameters import ExperimentParameters, Parameters, PlotSelection
from R_MoTMo.plotResults import load_results, plot_results
from R_MoTMo.world import World


class Experiment:
    """The main manipulation component."""

    def __init__(self, sim_params: Parameters, plot_selection: PlotSelection,
                 exp_params: ExperimentParameters = None):
        self.sim_params = sim_params
        self.plot_selection = plot_selection
        if not exp_params:
            exp_params = ExperimentParameters()
        self.exp_params = exp_params

    def run(self):
        """Main function of the simulation."""

        if self.exp_params.n_runs == 1:
            self.run_one()
        else:
            self.run_many()

    def run_one(self):
        """Runs simulation ones."""

        world = World(self.sim_params)
        world.run_simulation()

        results = load_results(self.sim_params.simulation_name())
        plot_results(self.plot_selection, self.sim_params, **results)

        tools.export_to_csv(results,
                            self.sim_params)

    def run_many(self):
        """Runs simulation more than once."""

        global_record = []
        cell_record = []
        person_record = []

        for _ in range(self.exp_params.n_runs):

            world = World(self.sim_params)
            world.run_simulation()

            global_record.append(world.global_record)
            cell_record.append(world.cell_record)
            person_record.append(world.person_record)

        results = {
            'globalRecord': global_record,
            'cellRecord': cell_record,
            'personRecord': person_record
        }

        tools.export_to_csv_by_runs(results,
                                    self.sim_params)

        global_record = np.array(global_record).mean(0)
        cell_record = np.array(cell_record).mean(0)
        person_record = np.array(person_record).mean(0)

        results = {
            'endTime': self.sim_params.time_steps-1,
            'nCells': len(world.cells),
            'cellProperties': world.cell_properties,
            'cellRecord': cell_record,
            'nPersons': world.n_persons,
            'personProperties': world.person_properties,
            'personRecord': person_record,
            'globalRecord': global_record,
            'simParams': self.sim_params.__dict__
        }

        plot_results(self.plot_selection, self.sim_params, **results)

        tools.export_to_csv(results,
                            self.sim_params)
