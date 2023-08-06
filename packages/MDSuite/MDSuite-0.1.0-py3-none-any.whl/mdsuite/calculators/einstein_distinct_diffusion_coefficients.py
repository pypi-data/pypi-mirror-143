"""
MDSuite: A Zincwarecode package.

License
-------
This program and the accompanying materials are made available under the terms
of the Eclipse Public License v2.0 which accompanies this distribution, and is
available at https://www.eclipse.org/legal/epl-v20.html

SPDX-License-Identifier: EPL-2.0

Copyright Contributors to the Zincwarecode Project.

Contact Information
-------------------
email: zincwarecode@gmail.com
github: https://github.com/zincware
web: https://zincwarecode.com/

Citation
--------
If you use this module please cite us with:

Summary
-------
Module for computing distinct diffusion coefficients using the Einstein method.
"""
import itertools
import warnings
from dataclasses import dataclass
from typing import Any, List, Union

import numpy as np
import tensorflow as tf
from tqdm import tqdm

from mdsuite.calculators.calculator import call
from mdsuite.calculators.trajectory_calculator import TrajectoryCalculator
from mdsuite.database.mdsuite_properties import mdsuite_properties
from mdsuite.utils.calculator_helper_methods import fit_einstein_curve


@dataclass
class Args:
    """
    Data class for the saved properties.
    """

    data_range: int
    correlation_time: int
    atom_selection: np.s_
    tau_values: np.s_
    molecules: bool
    species: list
    fit_range: int


tqdm.monitor_interval = 0
warnings.filterwarnings("ignore")


class EinsteinDistinctDiffusionCoefficients(TrajectoryCalculator):
    """
    Class for the Green-Kubo diffusion coefficient implementation

    Attributes
    ----------
    experiment :  object
            Experiment class to call from
    species : list
            Which species to perform the analysis on
    x_label : str
            X label of the tensor_values when plotted
    y_label : str
            Y label of the tensor_values when plotted
    analysis_name : str
            Name of the analysis
    loaded_property : str
            Property loaded from the database_path for the analysis

    See Also
    --------
    mdsuite.calculators.calculator.Calculator class

    Examples
    --------
    experiment.run_computation.EinsteinDistinctDiffusionCoefficients(data_range=500,
                                                                     plot=True,
                                                                     correlation_time=10)
    """

    def __init__(self, **kwargs):
        """
        Constructor for the Green Kubo diffusion coefficients class.

        Attributes
        ----------
        experiment :  object
                Experiment class to call from
        """
        super().__init__(**kwargs)

        self.scale_function = {"quadratic": {"inner_scale_factor": 10}}
        self.loaded_property = mdsuite_properties.unwrapped_positions

        self.database_group = "Diffusion_Coefficients"
        self.x_label = r"$$\text{Time} / s $$"
        self.y_label = r"$$\text{VACF} / m^{2}/s^{2}$$"
        self.analysis_name = "Einstein_Distinct_Diffusion_Coefficients"
        self.experimental = True
        self.result_keys = ["diffusion_coefficient", "uncertainty"]
        self.result_series_keys = ["time", "msd"]
        self.combinations = []

    @call
    def __call__(
        self,
        plot: bool = True,
        species: list = None,
        data_range: int = 500,
        save: bool = True,
        correlation_time: int = 1,
        tau_values: Union[int, List, Any] = np.s_[:],
        molecules: bool = False,
        export: bool = False,
        atom_selection: dict = np.s_[:],
        fit_range: int = -1,
    ):
        """
        Parameters
        ----------
        plot : bool
                if true, plot the output.
        species : list
                List of species on which to operate.
        data_range : int
                Data range to use in the analysis.
        save : bool
                if true, save the output.

        correlation_time : int
                Correlation time to use in the window sampling.
        atom_selection : np.s_
                Selection of atoms to use within the HDF5 database.
        export : bool
                If true, export the data directly into a csv file.

        Returns
        -------
        None

        """

        if species is None:
            species = list(self.experiment.species)
        self.combinations = list(itertools.combinations_with_replacement(species, 2))

        self.plot = plot

        if fit_range == -1:
            fit_range = int(data_range - 1)

        # set args that will affect the computation result
        self.args = Args(
            data_range=data_range,
            correlation_time=correlation_time,
            atom_selection=atom_selection,
            tau_values=tau_values,
            molecules=molecules,
            species=species,
            fit_range=fit_range,
        )
        self.time = self._handle_tau_values()

        self.msd_array = np.zeros(self.args.data_range)  # define empty msd array

    def msd_operation(self, ensemble: tf.Tensor, square: bool = True):
        """
        Perform a simple msd operation.

        Parameters
        ----------
        ensemble : tf.Tensor
            Trajectory over which to compute the msd.
        square : bool
            If true, square the result, else just return the difference.
        Returns
        -------
        msd : tf.Tensor shape=(n_atoms, data_range, 3)
                Mean square displacement.
        """
        if square:
            return tf.math.squared_difference(
                tf.gather(ensemble, self.args.tau_values, axis=1), ensemble[:, None, 0]
            )
        else:
            return tf.math.subtract(ensemble, ensemble[:, None, 0])

    def _compute_msd(self, data: dict, data_path: list, combination: tuple):
        """
        Compute the vacf on the given dictionary of data.

        Parameters
        ----------
        data : dict
                Dictionary of data returned by tensorflow.
        data_path : list
                Data paths for accessing the dictionary.
        combination : tuple
                Tuple being studied in the msd, i.e. ('Na', 'Cl) or ('Na', 'Na').
        Returns
        -------
        updates the class state
        """
        # shape = (n_atoms, data_range, 3)
        msd_a = self.msd_operation(data[data_path[0]], square=False)
        msd_b = self.msd_operation(data[data_path[0]], square=False)

        for i in range(len(data[data_path[0]])):
            for j in range(len(data[data_path[1]])):
                if combination[0] == combination[1] and i == j:
                    continue
                else:
                    self.msd_array += self.prefactor * np.array(
                        tf.reduce_sum(msd_a[i] * msd_b[j], axis=1)
                    )

    def _calculate_prefactor(self, species: Union[str, tuple] = None):
        """
        calculate the calculator pre-factor.

        Parameters
        ----------
        species : str
                Species property if required.
        Returns
        -------
        Updates the prefactor attribute of the class.
        """
        if species[0] == species[1]:
            atom_scale = self.experiment.species[species[0]].n_particles * (
                self.experiment.species[species[1]].n_particles - 1
            )
        else:
            atom_scale = (
                self.experiment.species[species[0]].n_particles
                * self.experiment.species[species[1]].n_particles
            )

        numerator = self.experiment.units["length"] ** 2
        denominator = self.experiment.units["time"] * atom_scale
        self.prefactor = numerator / denominator

    def _apply_averaging_factor(self):
        """
        Apply an averaging factor to the tensor_values.
        Returns
        -------
        averaged copy of the tensor_values
        """
        self.msd_array /= int(self.n_batches) * self.ensemble_loop

    def _post_operation_processes(self, species: Union[str, tuple] = None):
        """
        call the post-op processes
        Returns
        -------

        """
        try:
            fit_values, covariance, gradients, gradient_errors = fit_einstein_curve(
                x_data=self.time, y_data=self.msd_array, fit_max_index=self.args.fit_range
            )
            error = np.sqrt(np.diag(covariance))[0]

            data = {
                "diffusion_coefficient": fit_values[0],
                "uncertainty": error,
                "time": self.time.tolist(),
                "msd": self.msd_array.tolist(),
            }
        except ValueError:
            fit_values, covariance, gradients, gradient_errors = fit_einstein_curve(
                x_data=self.time,
                y_data=abs(self.msd_array),
                fit_max_index=self.args.fit_range,
            )
            error = np.sqrt(np.diag(covariance))[0]

            data = {
                self.result_keys[0]: -1 / 6 * fit_values[0],
                self.result_keys[1]: 1 / 6 * error,
                self.result_series_keys[0]: self.time.tolist(),
                self.result_series_keys[1]: self.msd_array.tolist(),
            }

        data.update({"time": self.time.tolist(), "msd": self.msd_array.tolist()})

        self.queue_data(data=data, subjects=list(species))

    def check_input(self):
        """
        Check the user input to ensure no conflicts are present.

        Returns
        -------

        """
        self._run_dependency_check()

    def run_calculator(self):
        """
        Perform the distinct coefficient analysis analysis
        """
        self.check_input()
        for combination in self.combinations:
            species_values = list(combination)
            dict_ref = [
                str.encode("/".join([species, self.loaded_property.name]))
                for species in species_values
            ]
            batch_ds = self.get_batch_dataset(species_values)
            self._calculate_prefactor(combination)

            for batch in tqdm(
                batch_ds,
                ncols=70,
                desc=f"{combination[0]}-{combination[1]}",
                total=self.n_batches,
                disable=self.memory_manager.minibatch,
            ):
                ensemble_ds = self.get_ensemble_dataset(batch, species_values)
                for ensemble in ensemble_ds:
                    self._compute_msd(ensemble, dict_ref, combination)

            self._post_operation_processes(combination)
