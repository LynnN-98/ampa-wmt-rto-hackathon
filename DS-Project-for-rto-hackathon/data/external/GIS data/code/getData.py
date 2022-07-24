# coding=utf-8

import arcpy
from arcpy import env, da
from os import path
import pandas as pd
import time

if __name__ == '__main__':
    filePath = r'D:\self\202207\yannie'
    # 输入文件路径
    filename = path.join(filePath, 'Animal Data clean.xlsx')
    # 输出结果路径
    fLayer = path.join(filePath, 'traj.shp')

    t_start = time.time()

    env.workspace = filePath
    env.overwriteOutput = True

    data = pd.read_excel(filename)
    print data

    fromLons = data['found_lng']
    fromLats = data['found_lat']
    toLons = data['outcome_lng']
    toLats = data['outcome_lat']
    citys = data['shelter_id']
    times = data['intake_date']

    arcpy.CreateFeatureclass_management(filePath, 'traj.shp', 'polyline',
                                        spatial_reference=arcpy.SpatialReference(4326))
    try:
        arcpy.AddField_management(fLayer, "city", "TEXT", field_length=50)
    except:
        pass

    try:
        arcpy.AddField_management(fLayer, "time", "TEXT", field_length=50)
    except:
        pass

    with da.InsertCursor(fLayer, ["SHAPE@JSON", "city", "time"]) as cursor:
        for item in zip(fromLons, fromLats, toLons, toLats, citys, times):
            cursor.insertRow(
                ['{"paths":[' + str(
                    [[item[0], item[1]],
                     [item[2], item[3]]]) + '],"spatialReference":{"wkid":4326,"latestWkid":4326}}', item[4], item[5]])

    print "Processing cost {} seconds".format(time.time() - t_start)
