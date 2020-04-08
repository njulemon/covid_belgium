from matplotlib.figure import Figure

from AxesPlotter import AxesPlotter
from DataAccessObject import DataAccessObject
from Enums import Country, PatientCase, PatientCategory
import matplotlib.pyplot as plt

if __name__ == "__main__":
    """
    Only for debug purpose.
    """
    dao = DataAccessObject(Country.belgium)

    # figure
    fig, ax = plt.subplots(figsize=(10, 7))

    # plotter
    ax_plotter = AxesPlotter(dao)

    # try to plot death
    ax_plotter.plot(ax, (PatientCase.hospitalization_total, PatientCategory.country), cumsum=False, log=True)

    # make dates readable (rotation)
    fig.autofmt_xdate()

    plt.show()