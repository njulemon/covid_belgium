from collections import namedtuple
from enum import Enum, auto
from typing import List, Dict

from Enums import PatientCase, PatientCategory, Country

FileInformation = namedtuple('DataInformation', ['http_file', 'case', 'dic_category'])


class DataSource:


    @classmethod
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
                                        PatientCategory.age: 'AGEGROUP'
                                }
                        )
                ]
        }

        return connection_object_dic[country]
