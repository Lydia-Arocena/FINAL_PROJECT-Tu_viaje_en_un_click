from geopy.geocoders import Nominatim
from geopy.distance import geodesic 
from pymongo import MongoClient
import json
from bson.json_util import dumps
import pandas as pd


def get_coordenadas(city):
    """
    Esta función saca las coordenadas de la ciudad que le pases.
    Args: una ciudad (string).
    Return: Las coordeandas de la ciudad que le paso como argumento (latitud y longitud).
    """
    geolocator = Nominatim(user_agent="Lydia")
    location = geolocator.geocode(query=city, exactly_one=True,timeout=200)
    return location[1]



def get_coordenadas_tipo_point(city):
    """
    Esta función saca las coordenadas tipo point de la ciudad que le pases.
    Args: una ciudad (string).
    Return: Las coordeandas tipo point de la ciudad que le paso como argumento (latitud y longitud).
    """
    coord= get_coordenadas(city)
    return {"type": "Point", "coordinates": coord[::-1]}



def measure_distance(city1,city2):
    """
    Esta función mide la distancia en kms entre dos ciudades.
    Args: dos ciudades (string).
    Return: La distancia en kms entre ambas ciudades.
    """
    city1 = get_coordenadas_tipo_point(city1)['coordinates']
    city2 = get_coordenadas_tipo_point(city2)['coordinates']
    return (geodesic(city1, city2).kilometers)



def geonear(city, radio):
    """
    Esta función devuelve todas las ciudades contenidas dentro del radio que le paso desde el punto de origen especificado.
    Args:city (string).
         radio en kms (int).
    Return: lista de ciudades contenidas en el radio especificado.
    """
    coord=get_coordenadas(city)
    client = MongoClient("localhost:27017")
    db = client.get_database("Tu_viaje_ideal_en_un_click")
    coordenadas = db.get_collection("coordenadas")
    
    query_travel=[{
    "$geoNear": {'near': list(coord[::-1]),
             'distanceField': 'distance',
             'maxDistance': radio,
             'distanceMultiplier': 6371,
             'spherical'  : True}}]

    geoloc_=coordenadas.aggregate(query_travel)
    geoquery_travel=json.loads(dumps(geoloc_))
    return geoquery_travel


def df_geonear(city, radio):
    """
    Esta función sirve para obtener un df en base a la lista de diccionarios obtenida por la función "Geonear".
    Args: city (string).
          radio en kms (int)
    Return: df con todas las ciudades que están dentro de mi radio con sus respectivas distancias.
    """
    geo=geonear(city, radio)
    df= pd.DataFrame(geo)
    df2=df[df["distance"] < 800]
    df2.drop(columns=["_id","location"], inplace=True)
    df3=df2.drop(df2.index[[0]])
    return df3