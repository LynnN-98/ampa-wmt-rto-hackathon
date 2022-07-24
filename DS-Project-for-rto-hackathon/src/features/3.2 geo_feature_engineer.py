import pandas as pd
import os

path = "data"

dfCom = pd.read_excel(os.path.join(path, "Animal_feature_v3.xlsx"))
print(dfCom.shape) #(23080, 40)

dfGeo = pd.read_excel(os.path.join(path, "GIS data.xlsx"))
dfBasic = pd.read_excel(os.path.join(path, "shelter_intake_date_id.xlsx"))

dfGeoFeature = pd.merge(dfBasic, dfGeo,left_on="shelter_id", right_on="city", how="left")

dfGeoFeature[['NVDI', 'impervious']] = dfGeoFeature[['NVDI', 'impervious']].fillna(value=dfGeoFeature[['NVDI', 'impervious']].mean())

dfCom[['NVDI', 'impervious']] = dfGeoFeature[['NVDI', 'impervious']]

dfCom.to_excel(os.path.join("data", "Animal_feature_v4.xlsx"), index=False)
