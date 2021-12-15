import os
import pandas as pd
from dotenv import load_dotenv
from amadeus import Client, ResponseError
import src.geo_functions as gf
import requests

load_dotenv()

def get_points_interest(ciudad):
    coord= gf.get_coordenadas(ciudad)
    load_dotenv()
    amadeus= Client(
    client_id= os.getenv("API_Key"),
    client_secret=os.getenv("API_Secret")
)
    try:
        '''
        Esta función devuelve un lista de puntos de interés de la ciudad que le pase.
        Args: ciudad (string).
        Return: una lista de los puntos de interés de la ciudad dada.
        '''
        response = amadeus.reference_data.locations.points_of_interest.get(latitude=coord[0],longitude= coord[1])
        
        dicc={"Name":[],"Latitud":[],"Longitud":[], "Category":[]}
        for i in range(len(response.data)):
            point=response.data[i]["name"]
            dicc["Name"].append(point)
            dicc["Latitud"].append(response.data[i]["geoCode"]["latitude"])
            dicc["Longitud"].append(response.data[i]["geoCode"]["longitude"])
            dicc["Category"].append(response.data[i]["tags"][0])
        return pd.DataFrame(dicc)
    except ResponseError:
        return "There are not any available point of interest"



def Google_museums(ciudad,radio):
    """
    Esta función me devuelve un json con todos los museos que estén en dicho radio de la ciudad seleccionada.
    Args: ciudad (string)
          radio(int)
    Return: json con todos los museos que estén en dicho radio de la ciudad seleccionada.
    """
    coord=gf.get_coordenadas(ciudad)
    url= "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    parameters={"key": os.getenv("API_Google"),
            "location": f'{coord[0]}, {coord[1]}',
            "radius": radio,
            "keyword":"Museum"
           }
    response=requests.get(url,params=parameters)
    res=response.json()
    return res



def cleaning_museums(ciudad,radio):
    """
    Esta función me transforma un json en df.
    Args: ciudad (string)
          radio(int)
    Return: df con las características principales de los museos.
    """
    mus=Google_museums(ciudad,radio)
    dicc={"Name":[], "Rating":[],"Dirección":[],"Latitud":[], "Longitud":[]}
    for i in range (len(mus['results'])):
        dicc['Name'].append(mus['results'][i]['name']) #name
        dicc['Rating'].append(mus['results'][i]['rating']) #rating
        dicc['Dirección'].append(mus['results'][i]['vicinity']) #dirección
        dicc['Latitud'].append(mus['results'][i]['geometry']['location']['lat']) #lat
        dicc['Longitud'].append(mus['results'][i]['geometry']['location']['lng']) #lng
    museos=pd.DataFrame(dicc)
    return museos