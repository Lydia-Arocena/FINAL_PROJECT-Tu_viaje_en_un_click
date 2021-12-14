from geopy.geocoders import Nominatim
from geopy.distance import geodesic 
from pymongo import MongoClient
import json
from bson.json_util import dumps
import pandas as pd
import re
import unicodedata
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from deep_translator import (MyMemoryTranslator)
import pandas as pd
from pymongo import MongoClient
from pymongo import GEOSPHERE
import json
from bson.json_util import dumps
import ast
                             


def get_coordenadas(city):
    """
    Esta función saca las coordenadas de la ciudad que le pases.
    Args: una ciudad (string).
    Return: Las coordeandas de la ciudad que le paso como argumento (latitud y longitud).
    """
    try:
        geolocator = Nominatim(user_agent="Lydia")
        location = geolocator.geocode(query=city, exactly_one=True,timeout=200)
        return location[1]
    except:
        return "Unkown"


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
    city1 = get_coordenadas(city1)
    city2 = get_coordenadas(city2)
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
    df.distance=df.distance.apply([lambda x: int(x)])
    df2=df[df["distance"] < radio]
    df2.drop(columns=["_id","location"], inplace=True)
    df3=df2.drop(df2.index[[0]])
    df3.columns=["City", "Distance(kms)"]
    return df3


def selenium_IATAS():
    """
    Esta función escrapea con selenium esta página web.
    Args: none.
    Return: diccionario del lugar (ciudad, país) y el código IATA.
    """
    driver = webdriver.Chrome("./chromedriver.exe")
    url= "https://www.flightconnections.com/es/c%C3%B3digos-de-aeropuertos"
    driver.get(url)
    driver.implicitly_wait(5)
    dicc={"IATA":[],"Lugar":[]}

    for x in range(4,55,2): 
        i=0
        while True:
            i+=1
            try:
                dicc["IATA"].append(driver.find_element_by_css_selector(f"body > div.site-content.airport-codes > div.site-section > ul:nth-child({x}) > li:nth-child({i}) > a > div > p.airport-city > span.airport-code").text)
                dicc["Lugar"].append(driver.find_element_by_css_selector(f"body > div.site-content.airport-codes > div.site-section > ul:nth-child({x}) > li:nth-child({i}) > a > div > p.airport-city > span.airport-city-country").text)
            except:
                break
    return dicc



def strip_accents(text):
    """
    Esta función quita los acentos y caracteres especiales de un string.
    Args: Un string.
    returns: String sin acentos.
   
    """
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)



def dicc_to_df():
    """
    Esta función convierte un diccionario en un df y lo limpia.
    Args: dicc.
    Return: df limpio.
    """
    dicc= selenium_IATAS()
    df=pd.DataFrame(dicc)
    df.Cities=df.Lugar.apply(lambda x: x.split(",")[0])
    df.Countries=df.Lugar.apply(lambda x: x.split(",")[1])
    df.drop('Lugar', inplace=True, axis=1)
    df["Countries"]=df.Countries.apply(lambda x: x.lstrip())
    df["Cities"]=df.Cities.apply(strip_accents)
    df["Countries"]=df.Countries.apply(strip_accents)
    
    return df



def translator(x):
    """
    Esta función traduce palabras en español al inglés.
    Args: palabra en español (string).
    Return: palabra en inglés (string).
    """

    try:
        translated = MyMemoryTranslator('es', 'en').translate_batch([x])
        return translated[0]
    except:
        return x
    

def string_dicc(x):
    try:
        return ast.literal_eval(x)
    except:
        return x



def insert_Mongo():
    """
    Esta función inserta los datos geográficos en Mongo DB.
    """
    client = MongoClient("localhost:27017")
    db = client.get_database("Tu_viaje_ideal_en_un_click")
    IATA=pd.read_csv("../Data/IATAcoord.csv")
    data = IATA.to_dict(orient='records') 
    print(data)
    coordenadas = db["coordenadas"]  
    coordenadas.insert_many(data)