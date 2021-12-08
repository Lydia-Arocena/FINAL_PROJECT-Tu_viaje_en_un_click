import os
from dotenv import load_dotenv
from amadeus import Client, ResponseError
import src.geo_functions as gf

load_dotenv()

def get_points_interest(ciudad):
    load_dotenv()
    amadeus= Client(
    client_id= os.getenv("API_Key"),
    client_secret=os.getenv("API_Secret")
)
    try:
        '''
        What are the popular places in Barcelona (based on a geo location and a radius)
        '''
        response = amadeus.reference_data.locations.points_of_interest.get(latitude=gf.get_coordenadas(ciudad)["coordinates"][0],longitude= gf.get_coordenadas(ciudad)["coordinates"][1])
        lista_points=[]
        for i in range(len(response.data)):
            point=response.data[i]["name"]
            lista_points.append(point)
        return f"Points of interest in {ciudad} are :{lista_points}"
    except ResponseError as error:
        return "There are not any available point of interest"

