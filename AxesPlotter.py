from enum import Enum, auto
from typing import Tuple

from matplotlib.axes import Axes
from matplotlib.ticker import ScalarFormatter

from DataAccessObject import DataAccessObject
from Enums import PatientCase, PatientCategory, DataForm


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
        data_ = self.dao.get_data(plot_pattern[0], plot_pattern[1])
        if data_ is None:
            return

        # check type of data (state or change of state).
        data_form = plot_pattern[0].get_data_form
        is_already_cum = data_form != DataForm.daily_incidence

        # make title
        title = plot_pattern[0].get_clean_str

        # loop to plot
        for label, data in sorted(data_.items(), key=lambda x: x[0], reverse=True):

            # label = key
            # data = data_[key]

            # when there is only one item (all the country, no category, we must just label the data as 'Country').
            label = self.dao.country.name.capitalize() if label == 'None' else label
            label = title + ' - ' + label

            if cumsum and not is_already_cum:
                data_to_plot = data[PatientCategory.total.name].cumsum().sort_index()
            else:
                data_to_plot = data[PatientCategory.total.name].sort_index()

            # daily needs points to
            line_style = '-o' if cumsum else '-o'

            if log:
                ax.semilogy(data.index, data_to_plot, line_style, label=label)
                for axis in [ax.yaxis]:
                    axis.set_major_formatter(ScalarFormatter())
            else:
                ax.plot(data.index, data_to_plot, line_style, label=label)

        # legend
        ax.legend()

        # grid
        ax.grid(which='both')
