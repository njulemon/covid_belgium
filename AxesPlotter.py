from enum import Enum, auto
from matplotlib.axes import Axes

from DataAccessObject import DataAccessObject
from Enums import PatientCase, PatientCategory


class PlotPattern(Enum):
    death_by_day_country = auto()
    death_by_day_age = auto()

    def get_pattern(self):
        dic = {
                self.death_by_day_country: [PatientCase.death, None],
                self.death_by_day_age: [PatientCase.death, PatientCategory.age]
        }

        return dic[self]


class AxesPlotter:

    def __init__(self, dao: DataAccessObject):
        self.dao = dao

    def plot(self, ax: Axes, plot_pattern: PlotPattern, cumsum: bool = False):

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
