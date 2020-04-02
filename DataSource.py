from collections import namedtuple
from enum import Enum, auto
from typing import List, Dict

from Enums import PatientCase, PatientCategory, Country


class FileInformation:
    """
    Each case (see PatientCase) will be described with one FileInformation.
    For One country, you will get a list of FileInformation.
    You can have several files with the same PatientCase !
    """

    def __init__(self, http_file: str, case: PatientCase, dic_category: Dict[PatientCategory, str]):

        # contains the http link to the file.
        self.http_file: str = http_file

        # contains the case (all of them should be defined as a list of FileInformation)
        self.case: PatientCase = case

        # contains the category contained in this file for this case (you can have several files with the same case,
        # but several different categories). This has been done to keep data anonymous.
        self.dic_category: Dict[PatientCategory, str] = dic_category


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
                Country.belgium: [
                        FileInformation(
                                'https://epistat.sciensano.be/Data/COVID19BE_CASES_AGESEX.csv',
                                PatientCase.positive_to_covid,
                                {
                                        PatientCategory.date: 'DATE',
                                        PatientCategory.geo_level_1: 'REGION',
                                        PatientCategory.geo_level_2: 'PROVINCE',
                                        PatientCategory.age: 'AGEGROUP',
                                        PatientCategory.sex: 'SEX'
                                }
                        ),
                        FileInformation(
                                'https://epistat.sciensano.be/Data/COVID19BE_CASES_MUNI.csv',
                                PatientCase.positive_to_covid,
                                {
                                        PatientCategory.date: 'DATE',
                                        PatientCategory.geo_level_1: 'TX_RGN_DESCR_FR',
                                        PatientCategory.geo_level_2: 'TX_PROV_DESCR_FR',
                                        PatientCategory.geo_level_3: 'TX_DESCR_FR',
                                        PatientCategory.geo_level_3_id: 'NIS5'
                                }
                        ),
                        FileInformation(
                                'https://epistat.sciensano.be/Data/COVID19BE_HOSP.csv',
                                PatientCase.hospitalization,
                                {
                                        PatientCategory.date: 'DATE',
                                        PatientCategory.geo_level_1: 'REGION',
                                        PatientCategory.geo_level_2: 'PROVINCE',
                                        PatientCategory.total: 'TOTAL_IN'
                                }
                        ),
                        FileInformation(
                                'https://epistat.sciensano.be/Data/COVID19BE_HOSP.csv',
                                PatientCase.hospitalization_respiratory,
                                {
                                        PatientCategory.date: 'DATE',
                                        PatientCategory.geo_level_1: 'REGION',
                                        PatientCategory.geo_level_2: 'PROVINCE',
                                        PatientCategory.total: 'TOTAL_IN_RESP'
                                }
                        ),
                        FileInformation(
                                'https://epistat.sciensano.be/Data/COVID19BE_HOSP.csv',
                                PatientCase.hospitalization_ecmo,
                                {
                                        PatientCategory.date: 'DATE',
                                        PatientCategory.geo_level_1: 'REGION',
                                        PatientCategory.geo_level_2: 'PROVINCE',
                                        PatientCategory.total: 'TOTAL_IN_ECMO'
                                }
                        ),
                        FileInformation(
                                'https://epistat.sciensano.be/Data/COVID19BE_MORT.csv',
                                PatientCase.death,
                                {
                                        PatientCategory.date: 'DATE',
                                        PatientCategory.geo_level_1: 'REGION',
                                        PatientCategory.sex: 'SEX',
                                        PatientCategory.age: 'AGEGROUP',
                                        PatientCategory.total: 'DEATHS'
                                }
                        )
                ]
        }

        return connection_object_dic[country]
