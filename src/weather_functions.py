import requests
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

def Api_request(ciudad,dias):
    """
    Esta función me devuelve un json con la predicción meterológica de, como máximo, de los tres siguientes días en la ciudad que le pase.
    Args: ciudad (string) o coordenadas (tupla numérica)
          dias(int del 1 al 3)
    Return: json con la predicción del timpo para ese día y los dos siguientes de la ciudad dada.
    """
    url= "http://api.weatherapi.com/v1/forecast.json"
    parameters={'key':os.getenv("API_weather"),'q':ciudad,'days':dias}
    response=requests.get(url,params=parameters)
    res=response.json()
    return res


def get_date(x):
    """
    Esta función limpia la columna de fechas.
    Args: fecha hora (string)
    Return: fecha (string) 
    """
    return x.split(" ")[0]


def cleaning(ciudad,dias):
    """
    Esta función me transforma un json en df.
    Args: ciudad (string) o coordenadas (tupla numérica)
          dias(int del 1 al 3)
    Return: df con las principales características metereológicas de los tres próximos días (contando hoy).
    """
    res = Api_request(ciudad,dias)
    dicc={"Date_hours":[],"Temperature":[],"Sky":[],"Icon":[],"Will it rain?":[],"Will it snow?":[]}
    for day in range(len(res)):
        for hour in range(0,24):
            dicc["Date_hours"].append(res['forecast']['forecastday'][day]['hour'][hour]['time'])
            dicc["Temperature"].append(res['forecast']['forecastday'][day]['hour'][hour]['temp_c'])
            dicc["Sky"].append(res['forecast']['forecastday'][day]['hour'][hour]['condition']['text'])
            dicc["Icon"].append(res['forecast']['forecastday'][day]['hour'][hour]['condition']['icon'])
            dicc["Will it rain?"].append(res['forecast']['forecastday'][day]['hour'][hour]['will_it_rain'])
            dicc["Will it snow?"].append(res['forecast']['forecastday'][day]['hour'][hour]['will_it_snow'])

    forecast=pd.DataFrame(dicc)
    forecast["Dates"] = forecast["Date_hours"].apply(get_date)
    forecast.drop(columns="Date_hours",inplace=True)
    result= pd.DataFrame({'Min_temp': forecast.groupby("Dates")["Temperature"].min(), 
                          'Max_temp': forecast.groupby("Dates")["Temperature"].max(),
                          'Rain': forecast.groupby("Dates")["Will it rain?"].agg(pd.Series.mode), 
                          'Snow': forecast.groupby("Dates")["Will it snow?"].agg(pd.Series.mode), 
                          'Sky': forecast.groupby("Dates")["Sky"].agg(pd.Series.mode), 
                          'Icon': forecast.groupby("Dates")["Icon"].agg(pd.Series.mode)}).reset_index()
    return result