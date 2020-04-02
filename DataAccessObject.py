from typing import List, Dict
import pandas as pd
import requests
import io

from DataSource import FileInformation, DataSource
from Enums import Country, PatientCase


class DataAccessObject:
    """
    This object allows to access the data through universal (Enums) categories and universal cases.
    """

    def __init__(self, country: Country):
        self.country = country

        # contains all the information to access data and mapping from field of the csv to enum fields (see Enums).
        self.list_data_source: List[FileInformation] = DataSource.get_info_for_country(country)

        # contains the data (in pandas DataFrame form).
        self.data_dic: Dict[PatientCase, pd.DataFrame] = dict()

        # download data
        for item in self.list_data_source:

            # download content
            data_raw = requests.get(item.http_file).content

            # make a dic with pandas DataFrame
            try:
                # if this does not work you can try 'utf-8'
                temp_data: pd.DataFrame =  pd.read_csv(io.StringIO(data_raw.decode('latin_1')))
            except UnicodeDecodeError:
                print('Format is not the right one.')
            else:
                temp_data = temp_data.loc[:, [header for header in item.dic_category.values()]]
                temp_data.columns = [univ_header.name for univ_header in item.dic_category.keys()]
                self.data_dic[item.case] = temp_data