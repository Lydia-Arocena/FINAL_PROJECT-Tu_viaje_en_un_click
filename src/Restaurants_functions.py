import requests
import pandas as pd
import os
from dotenv import load_dotenv
import os
import sys
sys.path.append('../')

import src.geo_functions as gf

load_dotenv()

def Google_Api_request(ciudad,radio):
    """
    Esta función me devuelve un json con todos los restaurantes que estén en dicho radio de la ciudad seleccionada.
    Args: ciudad (string)
          radio(int)
    Return: json con todos los restaurantes que estén en dicho radio de la ciudad seleccionada.
    """
    coord=gf.get_coordenadas(ciudad)
    url= "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    parameters={"key": os.getenv("API_Google"),
            "location": f'{coord[0]}, {coord[1]}',
            "radius": radio,
            "keyword":"restaurant"
           }
    response=requests.get(url,params=parameters)
    res=response.json()
    return res


def cleaning_rest(ciudad,radio):
    """
    Esta función me transforma un json en df.
    Args: ciudad (string)
          radio(int)
    Return: df con las características principales de los restaurantes.
    """
    res=Google_Api_request(ciudad,radio)
    dicc={"Name":[], "Rating":[],"Dirección":[],"Latitud":[], "Longitud":[]}
    for i in range (len(res['results'])):
        dicc['Name'].append(res['results'][i]['name']) #name
        dicc['Rating'].append(res['results'][i]['rating']) #rating
        dicc['Dirección'].append(res['results'][i]['vicinity']) #dirección
        dicc['Latitud'].append(res['results'][i]['geometry']['location']['lat']) #lat
        dicc['Longitud'].append(res['results'][i]['geometry']['location']['lng']) #lng
    restaurants=pd.DataFrame(dicc)
    return restaurants