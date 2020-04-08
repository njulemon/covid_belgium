from DataAccessObject import DataAccessObject
from Enums import Country
import pandas as pd
from scipy.integrate import solve_ivp as sol


class SEIRModel:
    """
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

    def __init__(self, country: Country):

        # get population for current country
        self.N = self.get_population(country)

        # initial condition
        self.I_0 = 40
        self.S_0 = self.N
        self.E_0 = 20 * self.I_0
        self.R_O = 0

        self.sigma = 1/5.2
        self.gamma = 1/18

        # data access object
        self.dao = DataAccessObject(country)


    @staticmethod
    def get_population(country: Country) -> int:
        year = '2016'
        population_df: pd.DataFrame = pd.read_csv('data/population_by_country_world_bank.csv')
        return int(population_df[population_df['Country Name'] == country.name.capitalize()][year].iloc[0])

    def run(self, t0, tf):
        sol(self._dydt, [t0, tf], [])

    def _dydt(self, t, y, R0):

        S = y[0]
        E = y[1]
        I = y[2]

        beta = R0 * self.gamma

        dS = - beta * I * S / self.N
        dE = beta * I * S / self.N - self.sigma * E
        dI = self.sigma * E - self.gamma * I
        dR = self.gamma * I

        return [dS, dE, dI, dR]



