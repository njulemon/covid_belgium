import sys

from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

from matplotlib.figure import Figure

from AxesPlotter import AxesPlotter
from DataAccessObject import DataAccessObject
from Enums import Country, PatientCase, PatientCategory


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

        # widget size
        width = 200
        self.list_select_country.setMaximumWidth(width)
        self.list_select_case.setMaximumWidth(width)
        self.list_select_category.setMaximumWidth(width)

        # buttons
        self.plot_button = QtWidgets.QPushButton('Plot')
        self.plot_button.setMaximumWidth(width)

        # fill the lists.
        for country in Country:
            self.list_select_country.addItem(QtWidgets.QListWidgetItem(country.name))

        for case in PatientCase:
            self.list_select_case.addItem(QtWidgets.QListWidgetItem(case.name))

        for category in PatientCategory:
            self.list_select_category.addItem(QtWidgets.QListWidgetItem(category.name))

        # add widgets to the layouts.
        self.layout_button.addWidget(self.list_select_country)
        self.layout_button.addWidget(self.list_select_case)
        self.layout_button.addWidget(self.list_select_category)

        self.layout_button.addWidget(self.plot_button)

        self.layout_button_fig.addLayout(self.layout_button)
        self.layout_button_fig.addLayout(self.layout_fig)

        # map(action -> method)
        self.list_select_country.itemClicked.connect(self.select_country)
        self.plot_button.clicked.connect(self.plot)

        # country data.
        self.dataAO = None
        self.plotter = None

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

            self.fig_ax.clear()
            self.plotter = AxesPlotter(self.dataAO)
            self.plotter.plot(self.fig_ax, (current_case, current_category))

            # make dates readable (rotation)
            self.fig_ax.figure.autofmt_xdate()

            self.fig_ax.figure.canvas.draw()
            self.repaint()


if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()
