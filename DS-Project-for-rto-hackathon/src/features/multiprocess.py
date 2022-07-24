import os, time
import random
from multiprocessing import Process
from tqdm import tqdm
import pandas as pd
import googlemaps
import geopy
import geopy.distance
import requests

gmaps = googlemaps.Client(key='AIzaSyBj47Ce7_0rkOTPHZllLAfonfYqu6oW1x0')
weather_keys = 'Y7M7PVJ9KRZAU3MASXRVKB7S4'

def getLngLat(address):
    try:
        geocode_result = gmaps.geocode(address)

        latLngDict = geocode_result[0]["geometry"]["location"]
        # print("success extract:, ", latLngDict)
        return float(latLngDict["lng"]), float(latLngDict["lat"])
    except Exception as e:
        print("address extract error|","Address：",address,"|", e)

        return None, None



def process_lnglat(name, df):
    df.index = range(df.shape[0])

    error_count = 0
    ##1.1 crorect coordinates##
    for row in tqdm(range(df.shape[0]), desc=f'{name}_err_count({error_count}):'):
        foundAddress = df.loc[row, "found_address"]

        found_lng, found_lat = getLngLat(foundAddress)

        if found_lng != None and found_lat != None:
            df.loc[row, "found_lng"] = found_lng
            df.loc[row, "found_lat"] = found_lat

        outcomeAddress = df.loc[row, "outcome_address"]

        outcome_lng, outcome_lat = getLngLat(outcomeAddress)

        if outcome_lng != None and outcome_lat != None:
            df.loc[row, "outcome_lng"] = outcome_lng
            df.loc[row, "outcome_lat"] = outcome_lat

    ##1.2 get distance##
    distanceList = []
    for row in range(df.shape[0]):
        coords_1 = (df.loc[row, "found_lat"], df.loc[row, "found_lng"])
        coords_2 = (df.loc[row, "outcome_lat"], df.loc[row, "outcome_lng"])
        try:
            distance = geopy.distance.geodesic(coords_1, coords_2).miles
        except Exception as e:
            print(f'distance cal error, because:{e}')
            distance = 99999
        df.loc[row, "distance"] = distance

    maxColsDict = {
        'distance': 10000
    }

    ###if col's value greater than setted max value, then replace by mean value###
    for col, max_val in maxColsDict.items():
        index = df[col] > max_val
        df.loc[index, col] = round(df.loc[~index, col].mean())

    # for row in range(df.shape[0]):
    #     loc = df.loc[row, 'found_address']
    #     url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{loc}/2020-12-15T13:00:00?key={weather_keys} '
    #     headers = {
    #         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
    #
    #     res = requests.get(url, headers=headers)
    #     if res.status_code == 200:
    #         res = res.json()['days'][0]
    #         df.loc[row, ['temp', 'humidity', 'pressure', 'visibility']] = round((res['tempmax'] + res['tempmin']) / 2, 1), \
    #                                                                        res['humidity'], \
    #                                                                        res['pressure'], \
    #                                                                        res['visibility']
    #     else:
    #         print("error for: http ", res.status_code)
    #         df.loc[row, ['temp', 'humidity', 'pressure', 'visibility']] = 20, \
    #                                                                        64, \
    #                                                                        1027, \
    #                                                                        8.4
    #     time.sleep(random.random())

    df.to_csv(f'{name}.csv', index=False)


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
    infos = pd.read_excel('Animal Data.xlsx')
    # infos = infos.dropna() # drop nan

    # reformat address delete space
    for col in ['found_address', 'outcome_address']:
        infos[col] = infos[col].apply(lambda x:" ".join(item.strip() for item in x.split(' ')) if type(x) == str else x)

    # get valid lng lat
    infos = infos[(infos.found_lng < 180) & (infos.found_lng > -180) &
                  (infos.found_lat < 90) & (infos.found_lat > -90)]

    # infos = infos.iloc[:200, :]
    # infos.reindex()
    print(f'主进程（{os.getpid()}）开始...')
    process_list = []
    prefix = 'process_'
    process_num = 16
    for i in range(process_num):
        part_info = infos.loc[i::process_num, :]
        # print(part_info.shape)
        p = Process(target=process_lnglat, args=(prefix+f'{i}', part_info, ))
        process_list.append(p)

    for i in range(process_num):
        process_list[i].start()

    for i in range(process_num):
        process_list[i].join()

    concact_data('cleand_data.xlsx', process_num, prefix=prefix)


