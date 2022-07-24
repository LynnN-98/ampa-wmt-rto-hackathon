# Find the Home for Lost Pets/Data is All We Need

Highlights: 

1. My data is accurate. I used Google Maps API to correct all the longitudes and latitudes
2. My visualizations are fabulous. You can interactively analyze the interaction of animal movement routes with urban facilities!
3. My goal is practical and ambitious. It is possible for us to predict the direction and distance of the pet's home at the moment we find it.
(datafolio)

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

### Data visualizations:
1. Using the heat map of coordinates and distance (the redder the place represents the farther the distance), we found not only that the locations where pets were found were generally distributed next to buildings or by roads in the city, rather than near green areas or water sources, but also that pets near the edge of the city generally traveled a long distance. However, the specific characteristics of different cities vary, for example, downtown McAllen, TX also has a lot of pets found traveling long distances
2. I drew the Origin-Destination Map [13] with the help of external professional software: ArcGIS and QGIS. Although these routes are very haphazard, it is still evident that in most cities the animals radiate from the center to the edge of the city. Moreover, most of the animals have very short movement distances, that is, they are found close to home and traveling thousands of miles to get them to the shelter is a very inefficient method.

### EDA:
After getting all of this information, we want to build a model to predict the direction and distance of the animal's home. We need to explore the correlation between the response variables and…:
1. Nearby Facilities: the distance of the found spot to nearby facility
2. Weather Features: Temperature, humidity, wind direction and visibility
3. Geography Features: NDVI and percent imperviousness
4. Species: Dog or Cat

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

 * OSM - Map Data Extraction and Visual Generation
 * 
