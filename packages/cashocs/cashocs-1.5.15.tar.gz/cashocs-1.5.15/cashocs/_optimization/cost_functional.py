# Copyright (C) 2020-2022 Sebastian Blauth
#
# This file is part of cashocs.
#
# cashocs is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# cashocs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with cashocs.  If not, see <https://www.gnu.org/licenses/>.

"""Module for general reduced cost functionals."""

from __future__ import annotations

from typing import TYPE_CHECKING

import fenics
import numpy as np

if TYPE_CHECKING:
    from cashocs import _pde_problems
    from cashocs import types


class ReducedCostFunctional:
    """Reduced cost functional for PDE constrained optimization."""

    def __init__(
        self,
        form_handler: types.FormHandler,
        state_problem: _pde_problems.StateProblem,
    ) -> None:
        """Initializes self.

        Args:
            form_handler: The FormHandler object for the optimization problem.
            state_problem: The StateProblem object corresponding to the state system.

        """
        self.form_handler = form_handler
        self.state_problem = state_problem

    def evaluate(self) -> float:
        """Evaluates the reduced cost functional.

        First solves the state system, so that the state variables are up-to-date,
        and then evaluates the reduced cost functional by assembling the corresponding
        UFL form.

        Returns:
            The value of the reduced cost functional

        """
        self.state_problem.solve()

        val: float = fenics.assemble(self.form_handler.cost_functional_form)
        if self.form_handler.use_scalar_tracking:
            for j in range(self.form_handler.no_scalar_tracking_terms):
                scalar_integral_value = fenics.assemble(
                    self.form_handler.scalar_cost_functional_integrands[j]
                )
                self.form_handler.scalar_cost_functional_integrand_values[
                    j
                ].vector().vec().set(scalar_integral_value)

                val += (
                    self.form_handler.scalar_weights[j].vector().vec()[0]
                    / 2
                    * pow(
                        scalar_integral_value
                        - self.form_handler.scalar_tracking_goals[j],
                        2,
                    )
                )

        if self.form_handler.use_min_max_terms:
            for j in range(self.form_handler.no_min_max_terms):
                min_max_integral_value = fenics.assemble(
                    self.form_handler.min_max_integrands[j]
                )
                self.form_handler.min_max_integrand_values[j].vector().vec().set(
                    min_max_integral_value
                )

                if self.form_handler.min_max_lower_bounds[j] is not None:
                    val += (
                        1
                        / (2 * self.form_handler.min_max_mu[j])
                        * pow(
                            np.minimum(
                                0,
                                self.form_handler.min_max_lambda[j]
                                + self.form_handler.min_max_mu[j]
                                * (
                                    min_max_integral_value
                                    - self.form_handler.min_max_lower_bounds[j]
                                ),
                            ),
                            2,
                        )
                    )

                if self.form_handler.min_max_upper_bounds[j] is not None:
                    val += (
                        1
                        / (2 * self.form_handler.min_max_mu[j])
                        * pow(
                            np.maximum(
                                0,
                                self.form_handler.min_max_lambda[j]
                                + self.form_handler.min_max_mu[j]
                                * (
                                    min_max_integral_value
                                    - self.form_handler.min_max_upper_bounds[j]
                                ),
                            ),
                            2,
                        )
                    )

        val += self.form_handler.cost_functional_shift

        if self.form_handler.is_shape_problem:
            val += self.form_handler.shape_regularization.compute_objective()

        return val
