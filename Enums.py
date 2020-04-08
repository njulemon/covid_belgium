from enum import Enum, auto


class Country(bytes, Enum):

    def __new__(cls, value, sep):
        obj = bytes.__new__(cls, [value])
        obj._value_ = value
        obj.sep = sep
        return obj

    belgium = (1, ',')
    france = (2, ';')


class DataForm(Enum):
    cumsum = auto()
    daily_incidence = auto()
    daily_prevalence = auto()


class PatientCase(Enum):

    positive_to_covid_daily = (1, DataForm.daily_incidence)
    positive_to_covid_cumsum = (2, DataForm.cumsum)
    death_daily = (3, DataForm.daily_incidence)
    death_cumsum = (4, DataForm.cumsum)
    hospitalization_daily_prevalence = (5, DataForm.daily_prevalence)
    hospitalization_daily_incidence = (6, DataForm.daily_incidence)
    hospitalization_respiratory_daily_prevalence = (7, DataForm.daily_prevalence)   # hosp life support -> respiratory
    hospitalization_respiratory_daily_incidence = (8, DataForm.daily_incidence)     # hosp life support -> respiratory
    hospitalization_ecmo_daily_prevalence = (9, DataForm.daily_prevalence)          # life support ->  external oxygenation.
    hospitalization_out_daily_incidence = (10, DataForm.daily_incidence)             # patient which have left hospital.
    test_number_daily = (12, DataForm.daily_incidence)
    test_number_cumsum = (13, DataForm.cumsum)

    def __init__(self, id, data_form):
        self.id = id
        self.data_form = data_form

    @property
    def get_data_form(self):
        return self.data_form

    @property
    def get_clean_str(self):
        """
        Capitalize the name of the enum.
        :return:
        """
        return ' '.join([item.capitalize() for item in self.name.split('_')])


class PatientCategory(Enum):
    country = auto()
    date = auto()
    age = auto()
    sex = auto()
    geo_level_1 = auto()  # for example, the region
    geo_level_2 = auto()  # for example, the province
    geo_level_3 = auto()  # for example, the district
    geo_level_3_id = auto()
    total = auto()  # the total this category or this country.
