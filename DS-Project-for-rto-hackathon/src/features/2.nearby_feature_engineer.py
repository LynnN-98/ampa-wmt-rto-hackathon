import pandas as pd
import os
from tqdm import tqdm
import requests
import geopy.distance
from multiprocessing import Process

near1List = []
near2List = []
near3List = []
near4List = []
near5List = []

def getNerbyResponse(found_coordinate):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={}%2C{}&radius=1500&key=AIzaSyAMKUgQqgEaqXFTToC6Pqcaa30tQkMV0fA".format(
        found_coordinate[0], found_coordinate[1])
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    responseJson = response.json()
    return responseJson



def getNthNearbyDistance(found_coordinate, responseObj, i):
    try:
        coordinate = responseObj["results"][i]["geometry"]["location"]
        coordinate_nearby = (coordinate["lat"], coordinate["lng"])
        distance = geopy.distance.geodesic(found_coordinate, coordinate_nearby).miles
    except Exception as e:
        print("get nearby failed,", e)
        distance = None
    return distance

def parseAndAddList(responseJson, found_coordinate):

    if responseJson["status"] == "OK":
        distance = getNthNearbyDistance(found_coordinate, responseJson, 0)
        near1List.append(distance)

        distance = getNthNearbyDistance(found_coordinate, responseJson, 1)
        near2List.append(distance)

        distance = getNthNearbyDistance(found_coordinate, responseJson, 2)
        near3List.append(distance)

        distance = getNthNearbyDistance(found_coordinate, responseJson, 3)
        near4List.append(distance)

        distance = getNthNearbyDistance(found_coordinate, responseJson, 4)
        near5List.append(distance)
    else:
        near1List.append(None)
        near2List.append(None)
        near3List.append(None)
        near4List.append(None)
        near5List.append(None)


def genGeoFeatures(name, animalDF):
    error_count = 0
    for row in tqdm(range(animalDF.shape[0]), desc=f'{name}_err_count({error_count}):'):
        found_coordinate = (animalDF.loc[row, 'found_lat'], animalDF.loc[row, 'found_lng'])
        responseJson = getNerbyResponse(found_coordinate)
        parseAndAddList(responseJson, found_coordinate)

    ##add nearby features##
    animalDF["nearby1"] = near1List
    animalDF["nearby2"] = near2List
    animalDF["nearby3"] = near3List
    animalDF["nearby4"] = near4List
    animalDF["nearby5"] = near5List

    animalDF.to_csv(f'{name}.csv', index=False)

def concact_data(save_name, process_num, prefix='process_'):
    df = pd.read_csv(prefix+'0.csv')
    for i in range(1, process_num):
        next_df = pd.read_csv(prefix+str(i)+'.csv')
        df = pd.concat((df, next_df), axis=0, join='inner')
        print(df.shape)
    if save_name.endswith('xlsx'):
        df.to_excel(save_name, index=False)
    else:
        df.to_csv(save_name, index=False)

if __name__ == '__main__':

    animalDF = pd.read_excel(os.path.join("data", "Animal Data clean.xlsx"))

    print(f'Main Process（{os.getpid()}）begins...')
    process_list = []
    prefix = os.path.join("nearbyFeature", 'process_')
    process_num = 16
    for i in range(process_num):
        part_info = animalDF.loc[i::process_num, :]
        part_info = part_info.reset_index(drop=True)
        # print(part_info.shape)
        p = Process(target=genGeoFeatures, args=(prefix + f'{i}', part_info,))
        process_list.append(p)

    for i in range(process_num):
        process_list[i].start()

    for i in range(process_num):
        process_list[i].join()

    concact_data(os.path.join("data", 'Animal_feature_v1.xlsx'), process_num, prefix=prefix)
