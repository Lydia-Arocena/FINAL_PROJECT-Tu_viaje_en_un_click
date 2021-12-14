import os
import pandas as pd
from dotenv import load_dotenv
from amadeus import Client, ResponseError
import src.geo_functions as gf

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
        #print(response)
        lista_points=[]
        for i in range(len(response.data)):
            point=response.data[i]["name"]
            lista_points.append(point)
        return pd.DataFrame(lista_points)
    except ResponseError:
        return "There are not any available point of interest"

