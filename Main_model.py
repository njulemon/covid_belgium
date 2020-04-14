from matplotlib.figure import Figure

from AxesPlotter import AxesPlotter
from DataAccessObject import DataAccessObject
from Enums import Country, PatientCase, PatientCategory
import matplotlib.pyplot as plt

from SEIR_model import SEIRModel

if __name__ == "__main__":
    """
    Only for debug purpose.
    """
    # dao = DataAccessObject(Country.belgium)

    model = SEIRModel(Country.belgium, 5, 5)
    sol_t, sol_y, sol_Re = model.run()

    plt.figure(1)
    plt.plot(sol_t, sol_y[0, :])
    plt.title('S')
    plt.figure(2)
    plt.plot(sol_t, sol_y[1, :])
    plt.title('E')
    plt.figure(3)
    plt.plot(sol_t, sol_y[2, :])
    plt.title('I')
    plt.figure(4)
    plt.plot(sol_t, sol_y[3, :])
    plt.title('R')

    plt.figure(5)
    plt.title('Re')
    plt.plot(sol_Re)

    plt.show()
    # figure
    # fig, ax = plt.subplots(figsize=(10, 7))

    # # plotter
    # ax_plotter = AxesPlotter(dao)
    #
    # # try to plot death
    # ax_plotter.plot(ax, (PatientCase.hospitalization_total, PatientCategory.country), cumsum=False, log=True)

    # make dates readable (rotation)
    # fig.autofmt_xdate()
    #
    # plt.show()