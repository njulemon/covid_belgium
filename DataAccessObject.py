from typing import List, Dict, Optional
import pandas as pd
import requests
import io

from DataSource import FileInformation, DataSource
from Enums import Country, PatientCase, PatientCategory, DataForm, UnifiedStatistic


class DataAccessObject:
    """
    This object allows to access the data through universal (Enums) categories and universal cases.
    """

    def __init__(self, country: Country):
        self.country = country

        # contains all the information to access data and mapping from field of the csv to enum fields (see Enums).
        self.list_file_info: List[FileInformation] = DataSource.get_info_for_country(country)

        # contains the data (in pandas DataFrame form).
        self.data_dic: Dict[PatientCase, List[pd.DataFrame]] = dict()

        # download data
        for item in self.list_file_info:

            # download content
            data_raw = requests.get(item.http_file).content

            # make a dic with pandas DataFrame
            try:
                # if this does not work you can try 'utf-8'
                temp_data: pd.DataFrame = pd.read_csv(io.StringIO(data_raw.decode('latin_1')),
                                                      sep=country.sep)
            except UnicodeDecodeError:
                print('Format is not the right one.')
            else:
                temp_data = temp_data[[header for header in item.dic_category.values()]]
                temp_data.columns = [univ_header.name for univ_header in item.dic_category.keys()]

                # set date as date format.
                temp_data[PatientCategory.date.name] = pd.to_datetime(temp_data[PatientCategory.date.name])

                # add the dataFrame to the list for the current case.
                if item.case not in self.data_dic.keys():
                    self.data_dic[item.case] = list()
                self.data_dic[item.case].append(temp_data)

    def get_data(self, case: UnifiedStatistic, category: PatientCategory = None) -> Optional[Dict[str, pd.DataFrame]]:
        """
        Return the data available for the (case, category).
        :param case:
        :param category:
        :return: None (data not available) or the data (pd.DataFrame).
        """

        asked_for_country: bool = category is None or category == PatientCategory.country

        # find the table (index) in which we can find the category asked (country is an exception)
        if not asked_for_country:
            index = -1
            for ind, table in enumerate(self.data_dic[case]):
                if category.name in table.columns:
                    index = ind
                    break

            if index == -1:
                return None
            current_table = self.data_dic[case][index]
        else:
            current_table = self.data_dic[case][0]

        if asked_for_country:
            return {'None': current_table.groupby(by=[PatientCategory.date.name]).sum()}
        else:
            return {current_category: current_table[current_table[category.name] == current_category].groupby(
                by=[PatientCategory.date.name]).sum()
                    for current_category in current_table[category.name].unique().tolist() if
                    str(current_category) != 'nan'}

    def get_cases_available(self) -> List[PatientCase]:
        """
        get the list of all the available cases for current object.
        :return: the list of the cases available for the current country.
        """
        list_cases = [file_info.get_case() for file_info in self.list_file_info]
        return list_cases

    def get_categories_available_for_case(self, case: PatientCase) -> List[PatientCategory]:
        """

        :param case: the available cases for the current country you want to get.
        :return: a list of available categories.
        """
        list_list_categories = [file_info.get_real_category() for file_info in self.list_file_info
                                if file_info.get_case() == case]
        list_categories = [category for categories in list_list_categories for category in categories]
        return list_categories






