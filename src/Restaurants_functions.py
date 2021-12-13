import requests
import pandas as pd
import os
from dotenv import load_dotenv
import folium
from folium import Choropleth, Circle, Marker, Icon, Map
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
            "keyword":"Restaurant"
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


def map(ciudad,radio):
    restaurants=cleaning_rest(ciudad, radio)
    coord=list(gf.get_coordenadas(ciudad))
    map_rest = Map(location = coord, zoom_start = 15)
    for i,row in restaurants.iterrows():
        dicc = {"location": [row["Latitud"], row["Longitud"]], "tooltip": row["Name"]}
        
        if row["Rating"] >= 4.5:
            icono = Icon(color = "green",
                        prefix="fa",
                        icon="thumbs-o-up",
                        icon_color="black"
            )
        elif row["Rating"] < 4.5 and row["Rating"]>= 2.5:
            icono = Icon(color = "orange",
                        prefix="fa",
                        icon="hand-o-right",
                        icon_color="black")
            
        elif row["Rating"] < 2.5:
            icono = Icon(color = "red",
                        prefix="fa",
                        icon="thumbs-o-down",
                        icon_color="black")
            
        mark = Marker(**dicc, icon=icono)
        mark.add_to(map_rest)
    return map_rest