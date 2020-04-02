from enum import Enum, auto

class Country(Enum):
    belgium = auto()


class PatientCase(Enum):
    positive_to_covid = auto()
    death = auto()
    hospitalization = auto()
    intensive_care = auto() # ICU
    hospitalization_respiratory = auto() # life support -> respiratory
    hospitalization_ecmo = auto() # life support -> oxygenation through the skin.
    hospitalization_out_24 = auto() # patient which have left hospital in the last 24h.
    test_number = auto()


class PatientCategory(Enum):
    date = auto()
    age = auto()
    sex = auto()
    geo_level_1 = auto() # for example, the region
    geo_level_2 = auto() # for example, the province
    geo_level_3 = auto() # for example, the district
    geo_level_3_id = auto()
    no_data = auto()
    total = auto() # if not some individual cases, but already summed.


