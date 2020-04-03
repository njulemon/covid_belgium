from enum import Enum, auto
from matplotlib.axes import Axes

from DataAccessObject import DataAccessObject
from Enums import PatientCase, PatientCategory


class PlotPattern(Enum):
    """
    This class should be thought as all available plots.
    It defines the variable you want to plot (dead, positive tested, ...) and optionally a category if you want to
    split the data in this category.
    """
    death_country = auto()
    death_age = auto()

    def get_pattern(self):
        """
        Allows to get the information needed to plot the item you selected (item of the enum).
        :return:
        """
        dic = {
                self.death_country: [PatientCase.death, None],
                self.death_age: [PatientCase.death, PatientCategory.age],
                self.death_sex: [PatientCase.death, PatientCategory.sex]
        }

        return dic[self]


class AxesPlotter:
    """
    This class allows to plot on an axes the data following the pattern of PlotPattern.
    It needs a data access object (which depends on the country) to access the data AND a plotPattern.
    """

    def __init__(self, dao: DataAccessObject):
        self.dao = dao

    def plot(self, ax: Axes, plot_pattern: PlotPattern, cumsum: bool = False):
        """
        Plot the data on the provided axis.
        :param ax: The axis you want to plot on.
        :param plot_pattern: the type of data you want to plot.
        :param cumsum: Day by day or cumulative sum [default = False]
        :return:
        """

        # get data
        data_ = self.dao.get_cases_for(plot_pattern.get_pattern()[0], plot_pattern.get_pattern()[1])

        # loop to plot
        for label, data in data_.items():

            label = 'Cases' if label == 'None' else label

            if cumsum:
                ax.plot(data.index, data[PatientCategory.total.name].cumsum(), label=label)
            else:
                ax.plot(data.index, data[PatientCategory.total.name], label=label)

        # make title
        cumsum_title = ' [Total Cases]' if cumsum else ' [Daily Cases]'
        title = plot_pattern.get_pattern()[0].name + cumsum_title

        # legend & title
        ax.legend()
        ax.set_title(title)
