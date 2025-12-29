"""
Gazetteer Module

Looks up geographic coordinates for place names using the OpenStreetMap Nomiatim API.

"""

import requests
import time

# Nominatim requires a User-Agent header (we gotta be polite to free APIs!)

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
HEADERS = {"User-Agent" : "MiniGeoParse (educational research project)"}

def lookup_location(place_name : str, limit : int = 5) -> list[dict]:
    """
    Query Nominatim for candidate locations matching the place name

    Args : 

    - The place name as a string which is the location to search for 
    - The limit which is an integer representing the maximum number of returned locations by Nominatim

    Output :

    List of candidate locations with name, lat, lon

    """

    params = {
        "q" : place_name,
        "format" : "json",
        "limit" : limit,
    }

    response = requests.get(NOMINATIM_URL, params=params, headers=HEADERS)
    response.raise_for_status() # Raise exception if the request ever fails

    results = response.json()

    candidates = []
    for r in results :
        candidates.append({
            "name" : r.get("display_name", ""),
            "lat" : float(r.get("lat", 0)),
            "lon" : float(r.get("lon", 0)),

        })

    #Be polite : Nominatim asks for 1 request per second 
    time.sleep(1)

    return candidates

if __name__ == "__main__":
    test_places = ["Paris", "Geneva", "Alps"]

    for place in test_places:
        print(f"Given place to the API : {place}")
        print(f"Returned candidates by the API : {lookup_location(place)}")