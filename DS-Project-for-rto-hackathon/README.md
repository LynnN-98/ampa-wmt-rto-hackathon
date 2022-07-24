# Find the Home for Lost Pets/Data is All We Need

Highlights: 

1. My data is accurate. I used Google Maps API to correct all the longitudes and latitudes
2. My visualizations are fabulous. You can interactively analyze the interaction of animal movement routes with urban facilities!
3. My goal is practical and ambitious. It is possible for us to predict the direction and distance of the pet's home at the moment we find it.

![datafolio](https://user-images.githubusercontent.com/63036112/180656563-e2df2074-8114-4295-a677-dffef8856c7f.png)

## Challenge Category: Data Science

## Team Members

 * Lingyu Niu - Data Science

## Problem Statement

In this project, I tried to answer the following questions:

1. **What affects a pet's lost behavior?** Weather, urban facilities, or geography? Some studies have shown that pets are super sensitive to the weather! [1] [2] But does this affect their route?

2. **When we find a lost pet in a corner of the city, can we approximate the location and distance to its home?** I built models to try to provide insight into which features are more important and whether the predictions are realistic.

3. **How can we decide whether we should try to return it directly or contact the shelter in our region?** Imagine if we could predict the distance and direction of home, and if the shelter is right on the way, we could contact the staffs to help the pets get home efficiently. Hoo-Ray!

My final goal is to predict the distance (miles) & ordinal direction (N, S, E, W) [3] of the animal's home based on the location where the animal was found (weather, nearby, and geography)+ the attributes of the animal + the attributes of the shelter.

## Solution Description

### Data Cleaning:
1. I was noted in the data dictionary that the longitude and latitude are inaccurate. So, I applied the Google Maps API [4] to output the accurate coordinates based on the addresses.
2. The distance_miles are also inaccurate, so I re-calculated the distance using Geopy based on the corrected found & outcome coordinates. [5]
3. For other alternate format/errors/missing values, I conducted detailed checking and chose to drop/impute them.

### Feature Engineering:
I used existing data to derive the following new features:

1. **Weather!!** Temperature, humidity, wind direction and visibility of the location where the animal was found. I used Visual Crossing API [6] to output these features based on intake_date and found location.
2. **Urban Amenities!!** I calculated the distance between the found spot and the nearest commercial facility to try to measure this factor. I used Google Maps Nearby API [7] to extract the distance of the found location from the nearest 5 city facilities (might be Restaurants/Coffee/Petrol/Parking/Hotels....all the categories you can see on a Google Map), thus showing its proximity to public or commercial facilities in the city
3. **Geography!!** Normalized Difference Vegetation Index [8] and percent imperviousness [9] of the location where the animal was found. I know these 2 features sounds a bit obscure, but according to geographic exploration scholars, these indicators can measure the land cover and land use to some extent. I used a geographic information system application called ArcGIS to find the raster data and extract the numerical variables. [10] [11] [12] If you have downloaded and configured your environment, you can see my results in the *GIS* folder.

Also did one-hot encoding for categorical variables.

### Data visualizations:

![geo1](https://user-images.githubusercontent.com/63036112/180654627-c8ac1b4e-704a-4cc9-8c8a-aacaa7241f50.png)

1. Using the heat map of coordinates and distance (the redder the place represents the farther the distance), I found not only that the locations where pets were found were generally distributed next to buildings or by roads in the city, rather than near green areas or water sources, but also that pets near the edge of the city generally traveled a long distance. However, the specific characteristics of different cities vary, for example, downtown McAllen, TX also has a lot of pets found traveling long distances

![geo](https://user-images.githubusercontent.com/63036112/180654647-c46f1122-9fd9-4df5-a934-3c4d1bff40bc.png)

2. I drew the Origin-Destination Map [13] with the help of external professional software: ArcGIS and QGIS. Although these routes are very haphazard, it is still evident that in most cities the animals radiate from the center to the edge of the city. Moreover, most of the animals have very short movement distances, that is, they are found close to home and traveling thousands of miles to get them to the shelter is a very inefficient method.

### EDA (interactive!):
After getting all of this information, we want to build a model to predict the direction and distance of the animal's home. We need to explore the correlation between the response variables and…:
1. Nearby Facilities: the distance of the found spot to nearby facility

![eda1](https://user-images.githubusercontent.com/63036112/180654664-a7803b9f-182f-48ad-984a-7e93696bf5d0.png)
![eda2](https://user-images.githubusercontent.com/63036112/180654711-56078bd3-e523-4fa7-9d5e-2a89baff2828.png)

2. Weather Features: Temperature, humidity, wind direction and visibility

![eda3](https://user-images.githubusercontent.com/63036112/180654715-4e681f1d-792f-44e4-ac96-a4b120cc25bf.png)
![EDA5](https://user-images.githubusercontent.com/63036112/180654872-cde35144-4813-4ff6-88b4-3ef2a6615ec6.png)

3. Geography Features: NDVI and percent imperviousness

![EDA6](https://user-images.githubusercontent.com/63036112/180654887-61c20b57-7c66-4d9c-93a4-627489ed2bc0.png)
![eda7](https://user-images.githubusercontent.com/63036112/180654895-e85ca202-b0c6-4502-8653-d24e444b9fb7.png)
![eda8](https://user-images.githubusercontent.com/63036112/180654905-5fedde6e-e717-4272-ac9c-b03bbb721981.png)

4. Species: Dog or Cat

![eda9](https://user-images.githubusercontent.com/63036112/180654914-752fb027-a425-46a8-a2cc-3b11ca03684b.png)
![eda10](https://user-images.githubusercontent.com/63036112/180654918-688436d2-8950-454a-9a8b-f4351fa43b96.png)

### Modeling:
Based on the relative positions of the outcome and found coordinates, we calculated the ordinal directions[3], which have four categories. The calculation method is detailed in Ref.

**Please be patient and review our features again:**
Input:
* Species
* found_lng	found_lat
* nearby1	- nearby5	
* temp	
* humidity	
* winddir	
* visibility	
* NDVI	
* impervious
* annual_intake_2019
* annual_intake_2020
* annual_intake_2021
* jurisdiction_size_sq_km
* justidiction_state
* jurisdiction_region
* jurisdiction_pop_size
* jurisdiction_pop_density_person_per_sq_km


**Output:**
* the distance (miles): This is a regression model
* ordinal direction (NE/SE/SW/NW): This is a classification model

**Models:**
I choosed the XGBoost Regression and Classifier in this problem for following reasons:
1. It is a large number of observations in training data. (~18400+)
2. Number features < number of observations in training data.
3. Data has mixture numerical and categorical features.
4. Its execution speed and model performance.

**Performance:**
* Mean Squared Error for the Regression model: 0.000116
* Accuracy for the Classifier: 36.71%

I adjusted the parameters of the model, but the difference is very small, all after the thousandth place. The regression algorithm uses least squares to find the solution directly, and adjusting the parameters is not very meaningful for this case.

## Demo and Deep-Dive Visuals

A working demo of the interactive Origin-Destination Map:
https://www.youtube.com/watch?v=Xt-LaZSC8Wc


## Tools Used

 * googlemaps - Use Google Maps API
 * geopy - Calculate distance
 * multiprocessing - Batch processing of large amounts of data
 * funUtils - look up direction by latitude & longitude of 2 points
 * sklearn - modeling
 * pickle - save models
 * Timeline Weather API - get historical weather data with dates and cities
 * Geocoding API - Get coordinates by address
 * Places API - Get nearby facilities information
 * ArgGIS - Get geographic features based on jurisdiction region
 * QGIS - Draw interactive OD Map
 * matplotlib, seaborn, plotly - visualizations
 * folium - heat map

## Reference
[1] https://www.missinganimalresponse.com/lost-dog-behavior/

[2] https://www.missinganimalresponse.com/lost-cat-behavior/

[3] https://www.analytics-link.com/post/2018/08/21/calculating-the-compass-direction-between-two-points-in-python

[4] https://developers.google.com/maps/documentation/geocoding/best-practices

[5] https://geopy.readthedocs.io/en/stable/#module-geopy.distance

[6] https://www.visualcrossing.com/resources/documentation/weather-api/timeline-weather-api/

[7] https://developers.google.com/maps/documentation/places/web-service/search-nearby 

[8] https://gisgeography.com/ndvi-normalized-difference-vegetation-index/

[9] https://dec.vermont.gov/sites/dec/files/wsm/lakes/docs/Shoreland/lp_AppendixFImpervious.pdf

[10] Ndvi data source: nasa website 
https://neo.gsfc.nasa.gov/view.php?datasetId=MOD_NDVI_M

[11] Impervious surface data source: 
https://zenodo.org/record/3505079#.Yt0SwnZBxx2
Inversion results from multi-source satellite remote sensing data

[12] U.S. Administrative Border Data: https://gadm.org/download_country.html

[13] https://medium.com/@CompassIoT/what-is-origin-destination-mapping-what-can-it-teach-us-about-mobility-f6088e10bfb1
