

class model:
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

    beta : transmission rate = Rt * gamma
    sigma : infection rate (inverse of the mean latent period)
    gamma : recovery rate (inverse of the infectious period)

    Initial condition (China) :
    - I_0 = 40 (zoonotic exposure)
    - S_0 = 11_000_000 (population of Wuhan)
    - E_0 = 20 * I0 (literature)
    - R_0 = 0

    Parameters (China) :
    - sigma = 1/5.2
    - gamma = 1/18
    - R0 = 2.6 (1.9 -> 3.1) [Rt variable to estimate]

    """
