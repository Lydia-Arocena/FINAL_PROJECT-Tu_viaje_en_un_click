from pymongo import MongoClient
import pandas as pd



def get_country(city):
    """
    Esta función devuelve el país de una ciudad dada.
    Args: Ciudad (string).
    Return: País (string).
    """
    client = MongoClient("localhost:27017")
    db = client.get_database("Tu_viaje_ideal_en_un_click")
    c = db.get_collection("coordenadas")
    cond={"City": city}
    #pr={"IATA": 1,"Country":0, "_id":0, "City":1, "Location":0}
    div=list(c.find(cond))
    paises=div[0]['Country']
    
    return paises



def load_data():
    return pd.read_csv("Data/divisasdf.csv")