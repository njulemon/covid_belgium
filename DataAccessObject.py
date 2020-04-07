from typing import List, Dict, Optional
import pandas as pd
import requests
import io

from DataSource import FileInformation, DataSource
from Enums import Country, PatientCase, PatientCategory


class DataAccessObject:
    """
    This object allows to access the data through universal (Enums) categories and universal cases.
    """

    def __init__(self, country: Country):
        self.country = country

        # contains all the information to access data and mapping from field of the csv to enum fields (see Enums).
        self.list_data_source: List[FileInformation] = DataSource.get_info_for_country(country)

        # contains the data (in pandas DataFrame form).
        self.data_dic: Dict[PatientCase, List[pd.DataFrame]] = dict()

        # download data
        for item in self.list_data_source:

            # download content
            data_raw = requests.get(item.http_file).content

            # make a dic with pandas DataFrame
            try:
                # if this does not work you can try 'utf-8'
                temp_data: pd.DataFrame = pd.read_csv(io.StringIO(data_raw.decode('latin_1')))
            except UnicodeDecodeError:
                print('Format is not the right one.')
            else:
                temp_data = temp_data.loc[:, [header for header in item.dic_category.values()]]
                temp_data.columns = [univ_header.name for univ_header in item.dic_category.keys()]

                # set date as date format.
                temp_data[PatientCategory.date.name] = pd.to_datetime(temp_data[PatientCategory.date.name])

                # add the dataFrame to the list for the current case.
                if item.case not in self.data_dic.keys():
                    self.data_dic[item.case] = list()
                self.data_dic[item.case].append(temp_data)


    def get_cases_for(self, case: PatientCase, category: PatientCategory = None) -> Optional[Dict[str, pd.DataFrame]]:

        asked_for_country: bool = category is None or category == PatientCategory.country

        # find the table (index) in which we can find the category asked (country is an exception)
        if not asked_for_country:
            index = -1
            for ind, table in enumerate(self.data_dic[case]):
                if category.name in table.columns:
                    index = ind
                    continue

            if index == -1:
                return None
            current_table = self.data_dic[case][index]
        else:
            current_table = self.data_dic[case][0]

        if asked_for_country:
            return {'None': current_table.groupby(by=[PatientCategory.date.name]).sum()}
        else:
            return {current_category: current_table[current_table[category.name] == current_category].groupby(by=[PatientCategory.date.name]).sum()
                    for current_category in current_table[category.name].unique().tolist() if str(current_category) != 'nan'}


