import pandas as pd
import os

path = "data"

dfCom = pd.read_excel(os.path.join(path, "Animal_feature_v2.xlsx"))
print(dfCom.shape) #(23080, 40)


dfWeather = pd.read_csv(os.path.join(path, "clean_data_weather.csv"))

dfCom = pd.concat([dfCom, dfWeather], axis=1)

dfCom = dfCom.loc[:,~dfCom.columns.isin(["shelter_id", "intake_date"])]


dfCom.to_excel(os.path.join("data", "Animal_feature_v3.xlsx"), index=False)


