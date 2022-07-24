import pandas as pd
import os
from funUtils import direction_lookup
import numpy as np
path = "data"

dfShelter = pd.read_excel(os.path.join(path, "animal_shelter_raw_data.xlsx"), sheet_name="shelter_data")

animalDF = pd.read_excel(os.path.join(path, "Animal_feature_v1.xlsx"))

animalDF = pd.merge(animalDF, dfShelter)

##add direaction label##
direactionList = []
for row in range(animalDF.shape[0]):
    outcome_lat = animalDF.loc[row, "outcome_lat"]
    outcome_lng = animalDF.loc[row, "outcome_lng"]
    found_lat = animalDF.loc[row, "found_lat"]
    found_lng = animalDF.loc[row, "found_lng"]
    directResult = direction_lookup(found_lat, outcome_lat, found_lng, outcome_lng)
    direactionList.append(directResult)

animalDF["direction"] = direactionList


label_col = ["distance","direction"]
numeric_col = ['nearby1', 'nearby2', 'nearby3', 'nearby4', 'nearby5',
                'annual_intake_2019','annual_intake_2020', 'annual_intake_2021',
               'jurisdiction_size_sq_km','jurisdiction_pop_size',
                'jurisdiction_pop_density_person_per_sq_km']

factor_col = ['Species', 'justidiction_state', 'jurisdiction_region']

####################
##covert feature to all numeric##
dfNum = animalDF[numeric_col].fillna(value=animalDF[numeric_col].mean())

dfFactor = animalDF[factor_col]
dfFactor = pd.get_dummies(dfFactor)

dfY = animalDF[label_col]

dfCom = pd.concat([dfNum, dfFactor, dfY], axis=1)

dfCom.shape #(23080, 40)

dfCom.to_excel(os.path.join("data", "Animal_feature_v2.xlsx"), index=False)