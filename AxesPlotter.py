from enum import Enum, auto
from typing import Tuple

from matplotlib.axes import Axes
from matplotlib.ticker import ScalarFormatter

from DataAccessObject import DataAccessObject
from Enums import PatientCase, PatientCategory


class AxesPlotter:
    """
    This class allows to plot on an axes the data following the pattern of PlotPattern.
    It needs a data access object (which depends on the country) to access the data AND a plotPattern.
    """

    def __init__(self, dao: DataAccessObject):
        self.dao = dao

    def plot(self, ax: Axes, plot_pattern: Tuple[PatientCase, PatientCategory], cumsum: bool = False, log: bool = False):
        """
        Plot the data on the provided axis.
        :param ax: The axis you want to plot on.
        :param plot_pattern: A tuple with first arg as PatientCase and second PatientCategory (=None if no category)
        :param cumsum: Day by day or cumulative sum [default = False].
        :param log: If you want logy presentation [default = False].
        :return:
        """

        # get data
        data_ = self.dao.get_cases_for(plot_pattern[0], plot_pattern[1])
        if data_ is None:
            return

        # loop to plot
        for label, data in data_.items():

            # when there is only one item (all the country, no category, we must just label the data as "Cases").
            label = 'Cases' if label == 'None' else label

            if cumsum:
                data_to_plot = data[PatientCategory.total.name].cumsum()
            else:
                data_to_plot = data[PatientCategory.total.name]

            if log:
                ax.semilogy(data.index, data_to_plot, label=label)
                for axis in [ax.yaxis]:
                    axis.set_major_formatter(ScalarFormatter())
            else:
                ax.plot(data.index, data_to_plot, label=label)

            # grid
            ax.grid(which='both')

        # make title
        cumsum_title = ' [Total Cases]' if cumsum else ' [Daily Cases]'
        title = plot_pattern[0].name + cumsum_title

        # legend & title
        ax.legend()
        ax.set_title(title)
