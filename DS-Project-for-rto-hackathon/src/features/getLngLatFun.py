
import googlemaps

gmaps = googlemaps.Client(key='AIzaSyBj47Ce7_0rkOTPHZllLAfonfYqu6oW1x0')

def getLngLat(address):
    try:
        geocode_result = gmaps.geocode(address)

        latLngDict = geocode_result[0]["geometry"]["location"]

        return latLngDict["lng"], latLngDict["lat"]
    except Exception as e:
        print("address extract error|","Address：",address,"|", e)

        return None, None

result = getLngLat('1600 Amphitheatre Parkway, Mountain View, CA')
print(result)