from collections import namedtuple
from enum import Enum, auto
from typing import List, Dict

from Enums import PatientCase, PatientCategory, Country, UnifiedStatistic
import pandas as pd


class FileInformation:
    """
    Each case (see PatientCase) will be described with one FileInformation.
    For One country, you will get a list of FileInformation.
    You can have several files with the same PatientCase !
    """

    exclusion_list_real_category = [PatientCategory.date, PatientCategory.total]

    def __init__(self, http_file: str, case: PatientCase, dic_category: Dict[PatientCategory, str]):
        # contains the http link to the file.
        self.http_file: str = http_file

        # contains the case (all of them should be defined as a list of FileInformation)
        self.case: PatientCase = case

        # contains the category contained in this file for this case (you can have several files with the same case,
        # but several different categories). This has been done to keep data anonymous.
        self.dic_category: Dict[PatientCategory, str] = dic_category

    def get_case(self):
        return self.case

    def get_real_category(self):
        return [category for category in self.dic_category.keys()
                if category not in FileInformation.exclusion_list_real_category]


class DataSource:
    """
    This class contains all the information for each country to access data and to map the fields of the raw data
    to universal categories.
    """

    @staticmethod
    def get_info_for_country(country: Country) -> List[FileInformation]:
        """
        This method allows to get all the informations needed to access the data and map data to the fields
        defined in "Enums".
        :return: a list of FileInformation
        """

        connection_object_dic: Dict[Country, List[FileInformation]] = {

                # BELGIUM
                Country.belgium: [
                        FileInformation(
                                'https://epistat.sciensano.be/Data/COVID19BE_CASES_AGESEX.csv',
                                PatientCase.positive_to_covid_daily,
                                {
                                        PatientCategory.date: 'DATE',
                                        PatientCategory.geo_level_1: 'REGION',
                                        PatientCategory.geo_level_2: 'PROVINCE',
                                        PatientCategory.age: 'AGEGROUP',
                                        PatientCategory.sex: 'SEX',
                                        PatientCategory.total: 'CASES'
                                }
                        ),
                        FileInformation(
                                'https://epistat.sciensano.be/Data/COVID19BE_CASES_MUNI.csv',
                                PatientCase.positive_to_covid_daily,
                                {
                                        PatientCategory.date: 'DATE',
                                        PatientCategory.geo_level_1: 'TX_RGN_DESCR_FR',
                                        PatientCategory.geo_level_2: 'TX_PROV_DESCR_FR',
                                        PatientCategory.geo_level_3: 'TX_DESCR_FR',
                                        PatientCategory.total: 'CASES'
                                }
                        ),
                        FileInformation(
                                'https://epistat.sciensano.be/Data/COVID19BE_HOSP.csv',
                                PatientCase.hospitalization_daily_prevalence,
                                {
                                        PatientCategory.date: 'DATE',
                                        PatientCategory.geo_level_1: 'REGION',
                                        PatientCategory.geo_level_2: 'PROVINCE',
                                        PatientCategory.total: 'TOTAL_IN'
                                }
                        ),
                        FileInformation(
                                'https://epistat.sciensano.be/Data/COVID19BE_HOSP.csv',
                                PatientCase.hospitalization_respiratory_daily_prevalence,
                                {
                                        PatientCategory.date: 'DATE',
                                        PatientCategory.geo_level_1: 'REGION',
                                        PatientCategory.geo_level_2: 'PROVINCE',
                                        PatientCategory.total: 'TOTAL_IN_RESP'
                                }
                        ),
                        FileInformation(
                                'https://epistat.sciensano.be/Data/COVID19BE_HOSP.csv',
                                PatientCase.hospitalization_ecmo_daily_prevalence,
                                {
                                        PatientCategory.date: 'DATE',
                                        PatientCategory.geo_level_1: 'REGION',
                                        PatientCategory.geo_level_2: 'PROVINCE',
                                        PatientCategory.total: 'TOTAL_IN_ECMO'
                                }
                        ),
                        FileInformation(
                                'https://epistat.sciensano.be/Data/COVID19BE_MORT.csv',
                                PatientCase.death_daily,
                                {
                                        PatientCategory.date: 'DATE',
                                        PatientCategory.geo_level_1: 'REGION',
                                        PatientCategory.sex: 'SEX',
                                        PatientCategory.age: 'AGEGROUP',
                                        PatientCategory.total: 'DEATHS'
                                }
                        )
                ],

                # FRANCE
                Country.france: [
                        FileInformation(
                                'https://www.data.gouv.fr/fr/datasets/r/b4ea7b4b-b7d1-4885-a099-71852291ff20',
                                PatientCase.positive_to_covid_daily,
                                {
                                        PatientCategory.date: 'jour',
                                        PatientCategory.geo_level_1: 'dep',
                                        PatientCategory.age: 'clage_covid',
                                        PatientCategory.total: 'nb_pos'
                                }
                        ),
                        FileInformation(
                                'https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7',
                                PatientCase.hospitalization_cumsum,
                                {
                                        PatientCategory.date: 'jour',
                                        PatientCategory.geo_level_1: 'dep',
                                        PatientCategory.sex: 'sexe',
                                        PatientCategory.total: 'hosp'
                                }
                        ),
                        FileInformation(
                                'https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7',
                                PatientCase.death_cumsum,
                                {
                                        PatientCategory.date: 'jour',
                                        PatientCategory.geo_level_1: 'dep',
                                        PatientCategory.sex: 'sexe',
                                        PatientCategory.total: 'dc'
                                }
                        )
                ]
        }

        return connection_object_dic[country]

    def get_stat_for_country(self, stat_name: UnifiedStatistic):

        dic: Dict[PatientCategory, pd.DataFrame] = {
                
        }