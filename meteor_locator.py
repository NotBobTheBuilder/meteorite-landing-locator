#!/usr/bin/env python

import geopy            # For figuring out the locations
import geopy.distance   # For the distances
import arrow            # For figuring out the year
import webbrowser       # For displaying the location in google maps

geolocator = geopy.geocoders.Nominatim()

def year(date):
    """
    Return the year from a date
    """
    return arrow.get(date, 'MM/DD/YYYY HH:mm:ss A').year if date else None

def location(lat, lng):
    """
    Return a location from a latitude and longitude
    """
    return (float(lat), float(lng)) if lat and lng else None

def meteor(line):
    """
    Given a line, make a meteor object (some properties of the meteor)
    """
    (name, _, _, mass, fall, date, m_id, lat, lng) = line.strip().split(',')
    return {
        "name": name,
        "mass": mass,
        "fall": fall,
        "year": year(date),
        "location": location(lat, lng)
    }

def distance(location):
    def inner(meteor):
        """
        Distance between a location and a meteor
        """
        return geopy.distance.vincenty((location.latitude, location.longitude), meteor['location'])
    return inner

def get_location():
    """
    Find the user's location
    """
    city=raw_input('Which city are you in?: ')
    country=raw_input('Which country are you in?: ')
    return geolocator.geocode(city + ' ' + country)

with open('Meteorite_Landings.csv') as f:
    meteors = [meteor(line) for line in f.readlines()]

location = get_location()
meteor = min(meteors, key=distance(location))
print('the nearest meteor to you was {0} in {1}'.format(meteor['name'], meteor['year']))
webbrowser.open('https://www.google.co.uk/maps/place/{0[0]},{0[1]}'.format(meteor['location']))
