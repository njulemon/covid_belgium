import sys
from typing import List

from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure

from AxesPlotter import AxesPlotter
from DataAccessObject import DataAccessObject
from Enums import Country, PatientCase, PatientCategory, DataForm


def unique_list(l: List):
    list_unique = []
    for item in l:
        if item not in list_unique:
            list_unique.append(item)

    return list_unique




class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)

        # layouts
        # ---  layout_button_fig ---
        # |    button   |    fig    |
        # --------------------------
        self.layout_button_fig = QtWidgets.QHBoxLayout(self._main)
        self.layout_button = QtWidgets.QVBoxLayout()
        self.layout_fig = QtWidgets.QHBoxLayout()

        # fig layout.
        self.figure_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.fig_ax = self.figure_canvas.figure.subplots()
        self.layout_fig.addWidget(self.figure_canvas)
        self.addToolBar(NavigationToolbar(self.figure_canvas, self))

        # buttons & list layout.
        self.list_select_country = QtWidgets.QListWidget()
        self.list_select_case = QtWidgets.QListWidget()
        self.list_select_category = QtWidgets.QListWidget()

        # buttons
        self.plot_button = QtWidgets.QPushButton('Plot')
        self.clear_button = QtWidgets.QPushButton('Clear Figure')
        self.clear_and_plot_button = QtWidgets.QPushButton('Clear and Plot')

        # check box
        self.check_cumsum = QtWidgets.QCheckBox('Cumulative sum')
        self.check_log = QtWidgets.QCheckBox('Log plot')

        # widget size
        width = 200
        self.list_select_country.setMaximumWidth(width)
        self.list_select_case.setMaximumWidth(width)
        self.list_select_category.setMaximumWidth(width)
        self.plot_button.setMaximumWidth(width)
        self.clear_button.setMaximumWidth(width)
        self.clear_and_plot_button.setMaximumWidth(width)
        self.check_cumsum.setMaximumWidth(width)
        self.check_log.setMaximumWidth(width)

        # fill the lists.
        for country in Country:
            self.list_select_country.addItem(QtWidgets.QListWidgetItem(country.name))

        # add widgets to the layouts.
        self.layout_button.addWidget(self.list_select_country)
        self.layout_button.addWidget(self.list_select_case)
        self.layout_button.addWidget(self.list_select_category)

        self.layout_button.addWidget(self.plot_button)
        self.layout_button.addWidget(self.clear_button)
        self.layout_button.addWidget(self.clear_and_plot_button)

        self.layout_button.addWidget(self.check_cumsum)
        self.layout_button.addWidget(self.check_log)

        self.layout_button_fig.addLayout(self.layout_button)
        self.layout_button_fig.addLayout(self.layout_fig)

        # map(action -> method)
        self.list_select_country.itemClicked.connect(self.select_country)
        self.list_select_case.itemClicked.connect(self.select_case)
        self.plot_button.clicked.connect(self.plot)
        self.clear_button.clicked.connect(self.clear_fig)
        self.clear_and_plot_button.clicked.connect(self.clear_and_plot)

        # country data.
        self.dataAO = None
        self.plotter = None

    # ------------------
    #  Events Management
    # ------------------

    def select_country(self, item):
        """
        When clicked on a country,
        we change the data access object.
        (will download last data).
        :param item:
        :return:
        """
        country_selected = None
        for country in Country:
            if country.name == item.text():
                country_selected = country
                continue

        # change the data access object
        self.dataAO = DataAccessObject(country_selected)

        # update list of cases available for the country
        list_cases = unique_list(self.dataAO.get_cases_available())

        # clear list of cases and category
        self.list_select_case.clear()
        self.list_select_category.clear()

        # populate the cases list with available case for this country
        for case in list_cases:
            self.list_select_case.addItem(QtWidgets.QListWidgetItem(case.name))

    def select_case(self, item):

        # clear old list
        self.list_select_category.clear()

        # look for the choice of the case
        case_selected = None
        for case in PatientCase:
            if case.name == self.list_select_case.currentItem().text():
                case_selected = case

        # get the list of categories for current case and country.
        list_category = self.dataAO.get_categories_available_for_case(case_selected)

        # add country to the list
        self.list_select_category.addItem(QtWidgets.QListWidgetItem(PatientCategory.country.name))

        # populate list with available category
        for category in list_category:
            self.list_select_category.addItem(QtWidgets.QListWidgetItem(category.name))

    def plot(self):
        """
        When clicked on the plot button.
        :return:
        """

        if self.dataAO is not None \
                and self.list_select_case.currentItem() is not None \
                and self.list_select_category.currentItem() is not None:

            # find current case
            current_case = None
            for case in PatientCase:
                if case.name == self.list_select_case.currentItem().text():
                    current_case = case
                    continue

            # find current category
            current_category = None
            for category in PatientCategory:
                if category.name == self.list_select_category.currentItem().text():
                    current_category = category
                    continue

            # plot figure.
            self.plotter = AxesPlotter(self.dataAO)
            self.plotter.plot(self.fig_ax,
                              (current_case, current_category),
                              cumsum=self.check_cumsum.isChecked(),
                              log=self.check_log.isChecked())

            # make dates readable (rotation)
            self.fig_ax.figure.autofmt_xdate()

            # if already cumsum (original data) -> check the box
            if current_case.get_data_form != DataForm.daily_incidence:
                self.check_cumsum.setChecked(True)

            # repaint the figure and update the window
            self.fig_ax.figure.canvas.draw()
            self.repaint()

    def clear_fig(self):
        """
        to clear the figure.
        :return:
        """
        # clear the axes.
        self.fig_ax.clear()

        # repaint the figure and update the window
        self.fig_ax.figure.canvas.draw()
        self.repaint()

    def clear_and_plot(self):
        self.clear_fig()
        self.plot()


if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()
