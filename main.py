"""
Mykola Kryvyi
Computer Science, 1 course, UCU
Lab 1.2
"""
import folium
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
from haversine import haversine

def read_raw_file(lati, longli, year):
    """
    (float, float, int) -> None

    Function takes user's coordinates and the year of film's production.
    Based on this information, it creates a .csv file, that contains next
    information of the film: year, location, coordinates of the location
    and the distance to user's location.
    """
    file = open('locations.list' , 'r')
    contents = file.readlines()
    geolocator = Nominatim(user_agent="Mykola's map")

    #Taking only first 400,000 elements from database
    small_contents = contents[:400000]
    films = []
    country_of_user = users_country(lati, longli)
    for _, elem in enumerate(small_contents):
        film = elem.split('\t')
        needed_list = []
        try:
            #looking for symbols that will help to distingusih needed characteristics
            first_quote_index = film[0].index('"')
            second_quote_index = film[0].rindex('"')
            first_bracket_index = film[0].index('(')

            movie_year = film[0][first_bracket_index+1:first_bracket_index+5]
            movie_location = film[-1][:-1]
            if (str(movie_year) == str(year)) and (',' in movie_location) \
            and (country_of_user in movie_location):
                place = film[-1][:-1]
                location = geolocator.geocode(place)
                coordinates = (location.latitude, location.longitude)

                distance = haversine(coordinates, (lati, longli))

                needed_list.append(film[0][first_quote_index+1:second_quote_index])
                needed_list.append(year)
                needed_list.append(movie_location)
                needed_list.append(coordinates)
                needed_list.append(distance)
                films.append(needed_list)
        #except errors that occur when messy data appears
        except AttributeError:
            continue
        except GeocoderUnavailable:
            continue
        except OSError:
            continue
    #creating a csv file with data
    movies_list = pd.DataFrame(films, \
    columns = ['Film', 'Year', 'Location','Coordinates', 'Distance'])
    movies_list.to_csv('films.csv')

def shortest_distance_movies():
    """
    (None) -> list
    Function reads .csv file with the data and returns coordinates of the
    maximum 10 films, that are the closest one to the user's location
    """
    #looking for the films with shortest distance to user's location
    movies_data_frame = pd.read_csv('films.csv')
    movies_data_frame.sort_values(by=['Distance'], inplace=True)
    movies_data_frame = movies_data_frame.head(10)
    movies_data_frame.to_csv('films.csv')
    list_of_films = movies_data_frame.values.tolist()
    film_and_location = []
    for elem in list_of_films:
        #creating a list that consists only of names of films and its coordinates
        line = elem[4].split(',')
        latitude = float(line[0][1:])
        longitude = float(line[1][:-1])
        film_and_location.append([elem[1],(latitude,longitude)])
    return film_and_location

def creating_map(latitude, longtitude):
    """
    (float, float) -> None
    Function takes coordinates of the user and information from functions above
    and creates .html map based on it.
    """
    my_map = folium.Map(location=[latitude,longtitude],zoom_start = 6)
    my_group = folium.FeatureGroup(name = 'Films map')
    films = shortest_distance_movies()
    my_group.add_child(folium.Marker(location=[latitude,longtitude], \
    popup = 'Your location', icon = folium.Icon(color = 'darkred', icon='home')))
    places = []
    places.append([latitude,longtitude])
    for elem in films:
        my_group.add_child(folium.Marker(location=[elem[1][0],elem[1][1]], \
        popup = elem[0], icon = folium.Icon(color = 'darkblue', icon='cloud')))
        places.append([elem[1][0], elem[1][1]])
    my_map.add_child(my_group)
    folium.PolyLine(places, color="red", weight=2.5, opacity=1).add_to(my_map)
    my_map.save('films.html')

def users_country(latitude, longitude):
    """
    (float, float) -> string
    Function defines user's country by coordinates of the user. It reduces
    time that is needed to build a map because program is looking only
    for films that were produced in the user's country.
    >>> users_country(49.651179,24.2450)
    'Ukraine'
    >>> users_country(51.488650, -2.168747)
    'UK'
    """
    geolocator = Nominatim(user_agent="user's map")
    coordinates = str(latitude)+ ', ' + str(longitude)
    location = str(geolocator.reverse(coordinates, language="en"))
    try:
        index_of_comma = location.rindex(',')
        country = location[index_of_comma+2:]
        if country == 'United States':
            return 'USA'
        if country == 'United Kingdom':
            return 'UK'
        return country
    except ValueError:
        return ''

if __name__ == "__main__":
    year_for_movie = int(input('Please enter a year you would like to have a map for: '))
    location_movie = input('Please enter your location (format: lat, long): ')
    print('Map is generating...')
    print('Please wait...')

    coordinates_of_user = location_movie.split(',')
    latitude_of_user = float(coordinates_of_user[0])
    longtitude_of_user = float(coordinates_of_user[1].strip())

    read_raw_file(latitude_of_user, longtitude_of_user, year_for_movie)
    creating_map(latitude_of_user, longtitude_of_user)
    print('Finished. Please have look at the map films.html')
