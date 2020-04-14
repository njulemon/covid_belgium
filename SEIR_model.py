from typing import List

from DataAccessObject import DataAccessObject
from Enums import Country, PatientCase, PatientCategory
import pandas as pd
from scipy.integrate import solve_ivp as sol
from scipy.optimize import minimize_scalar
import numpy as np

class SEIRModel:
    """
    Model references :
    Wang, H., Wang, Z., Dong, Y. et al. Phase-adjusted estimation of the
    number of Coronavirus Disease 2019 cases in Wuhan, China. Cell Discov 6, 10 (2020).
    https://doi.org/10.1038/s41421-020-0148-0

    definition of the compartment of the population :
    - S : at risk of contracting the disease.
    - E : infected but not yet infectious.
    - I : infectious.
    - R : recovered of died from the disease.
    N = S + E + I + R: total population.

    Equations :
    dS/dt = - beta I / N * S
    dE/dt = beta I / N * S - sigma E
    dI/dt = sigma E - gamma I
    dR/dt = gamma I
    beta = R0 gamma

    beta = Rt * gamma : transmission rate
    sigma : infection rate (inverse of the mean latent period)
    gamma : recovery rate (inverse of the infectious period)

    own parameter
    pc_hospitalized : percentage of infectious person that must go to hospital = 4.6 (must be estimated more accurately).

    Initial condition (China) :
    - I_0 = 40 (zoonotic exposure)
    - S_0 = 11_000_000 (population of Wuhan)
    - E_0 = 20 * I0 (literature)
    - R_0 = 0

    Parameters (China) :
    - sigma = 1/5.2 [/day]
    - gamma = 1/18 [/day]
    - R0 = 2.6 (1.9 -> 3.1) [Rt variable to estimate] [No Unit]

    """

    def __init__(self, country: Country, R0_0 :float, n_iter):
        """

        :param country: the country
        :param R0_0: the initial R0 for the optimization procedure.
        """

        # get population for current country
        self.R0_0 = R0_0
        self.N = self.get_population(country)

        self.sigma = 1/5.2
        self.gamma = 1/18
        self.pc_hospitalized = 0.0046 # percentage of hospitalized patient in the I phase. TODO: 0.046

        # data access object
        self.dao = DataAccessObject(country)
        self.I_curve = self._get_reference_curve(self.dao).to_numpy()

        # initial condition
        self.E_0 = 7 * self.I_curve[0] # TODO : changed this.
        self.I_0 = self.I_curve[0]
        self.R_0 = 0
        self.S_0 = self.N - self.E_0 - self.I_0
        self.i_c = [self.S_0, self.E_0, self.I_0, self.R_0]

        # data len
        self.data_len = len(self.I_curve)

        # number of back and forth in the optimization procedure.
        self.back_and_forth = n_iter

        # this vector contains the Re(t). It will be updated by a backward forward procedure.
        self.Re_store = np.ones(self.data_len - 1) * R0_0

    @staticmethod
    def get_population(country: Country) -> int:
        year = '2016'
        population_df: pd.DataFrame = pd.read_csv('data/population_by_country_world_bank.csv')
        return int(population_df[population_df['Country Name'] == country.name.capitalize()][year].iloc[0])

    def run(self):

        for index_bf in range(self.back_and_forth):

            # loop for day to day
            for day_n in list(range(self.data_len-1)) + list(range(self.data_len-3, -1, -1)):

                # optimize R0 for day_n -> day_n + 1
                new_R0 = self._optimize([self.S_0, self.E_0, self.I_0, self.R_0], day_n)
                self.Re_store[day_n] = new_R0

        solution = self._solve()

        return solution.t, solution.y, self.Re_store

    def _optimize(self, i_c: List, index) -> float:
        print('---------------------------')
        print('index loop : ' + str(index))
        res = minimize_scalar(self._cost_function, bounds=[0, 5], args=(index, ), method='Bounded')
        print('Re current = ' + str(res.x))
        return res.x

    def _cost_function(self, R0, index) -> float:

        solution = sol(
                self._dydt,
                [0, self.data_len - 1],
                self.i_c,
                t_eval=list(range(0, self.data_len)),
                max_step=0.5,
                args=(R0, index)
        )
        cost = self._square_diff_reference(solution.y[2, :])
        # print('square diff = ' + str(cost))
        return cost

    def _square_diff_reference(self, signal_1: np.ndarray) -> float:
        return float(np.sum(np.square(self.I_curve - signal_1)))

    def _solve(self):

        solution = sol(
                self._dydt,
                [0, self.data_len - 2],
                self.i_c,
                max_step=0.1
        )
        return solution

    def _dydt(self, t, y, R0=0, index=-1):

        # find the index for the current time
        current_index = int(np.floor(t)) if t < self.data_len - 1 else self.data_len - 2

        # recompute all Re
        Re_temp = self.Re_store

        # change the value being optimized with the injected value (R0)
        if index > -1:
            Re_temp[index] = R0

        R_current = Re_temp[current_index]

        S, E, I, R = y

        beta = R_current * self.gamma

        dS = - beta * I * S / self.N
        dE = beta * I * S / self.N - self.sigma * E
        dI = self.sigma * E - self.gamma * I
        dR = self.gamma * I

        return [dS, dE, dI, dR]

    def _get_reference_curve(self, dao) -> pd.DataFrame:
        I_reference = self.dao.get_data(
                PatientCase.hospitalization_daily_prevalence,
                PatientCategory.country)['None']

        # only select over 10 hospitalization
        I_reference = I_reference[I_reference[PatientCategory.total.name] > 10]

        # we must divide by the proportion of people infectious which must go to hospitalization.
        I_reference[PatientCategory.total.name] = I_reference[PatientCategory.total.name] / self.pc_hospitalized

        # smoooth
        I_reference = I_reference.rolling(7, min_periods=1).mean()

        return I_reference[PatientCategory.total.name]


