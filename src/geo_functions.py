from geopy.geocoders import Nominatim
from geopy.distance import geodesic 

def get_coordenadas(city):
    """
    Esta función saca las coordenadas de la ciudad que le pases.
    Args: una ciudad (string).
    Return: Las coordeandas de la ciudad que le paso como argumento (latitud y longitud).
    """
    geolocator = Nominatim(user_agent="Lydia")
    location = geolocator.geocode(query=city, exactly_one=True,timeout=200)
    return {"type": "Point", "coordinates": [location[1][0], location[1][1]]}


def measure_distance(city1,city2):
    """
    Esta función mide la distancia en kms entre dos ciudades.
    Args: dos ciudades (string).
    Return: La distancia en kms entre ambas ciudades.
    """
    city1 = get_coordenadas(city1)['coordinates']
    city2 = get_coordenadas(city2)['coordinates']
    return (geodesic(city1, city2).kilometers)