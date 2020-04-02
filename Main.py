from DataAccessObject import DataAccessObject
from Enums import Country, PatientCase, PatientCategory

if __name__ == "__main__":
    dao = DataAccessObject(Country.belgium)
    