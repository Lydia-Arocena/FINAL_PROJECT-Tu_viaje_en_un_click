import requests
from dotenv import load_dotenv
import os
import json, ast
from datetime import datetime
from datetime import timedelta
import geo_functions as gf
import pandas as pd


def datatime(date_str):
    dt_obj = datetime.strptime(date_str, '%m-%d-%Y').date()
    return dt_obj



def api_request(city,date_str):
    coord=gf.get_coordenadas(city)
    check_in=datatime(date_str)
    check_out=check_in + timedelta(days=1)
    in_string=check_in.strftime("%Y-%m-%d")
    out_string=check_out.strftime("%Y-%m-%d")
    url = "https://hotels-com-provider.p.rapidapi.com/v1/hotels/nearby"
    querystring = {f"latitude":{coord[0]},"currency":"EUR","longitude":{coord[1]},"checkout_date":{out_string} ,"sort_order":"GUEST_RATING","checkin_date":{in_string},"adults_number":"1","locale":"en_US","page_number":"1","price_min":"10","price_max":"150"}
    headers = {
        'x-rapidapi-host': "hotels-com-provider.p.rapidapi.com",
        'x-rapidapi-key': os.getenv("API_hotel")
    }
    response = requests.get(url, headers=headers, params=querystring)
    res=json.loads(response.text)
    return res


def cleaning_hotel(res,city,date_str):
    res=api_request(city,date_str)
    dicc={"Nombre":[],"Estrellas":[],"Valoración":[],"Precio(€)":[],"Latitud":[],"Longitud":[]}
    for i in range(len(res)):
        dicc["Nombre"].append(res['searchResults']['results'][i]['name'])
        dicc["Estrellas"].append(res['searchResults']['results'][i]['starRating'])
        dicc["Valoración"].append(res['searchResults']['results'][i]['guestReviews']['rating'])
        dicc["Precio(€)"].append(res['searchResults']['results'][i]['ratePlan']['price']['current'])
        dicc["Latitud"].append(res['searchResults']['results'][i][ 'coordinate']['lat'])
        dicc["Longitud"].append(res['searchResults']['results'][i][ 'coordinate']['lon'])

    hotels=pd.DataFrame(dicc)
    hotels["Precio(€)"]=hotels["Precio(€)"].apply(lambda x: x.split("€")[0])
    hotels["Precio(€)"] = hotels["Precio(€)"].astype(int)
    hotels["Estrellas"] = hotels["Estrellas"].astype(int)
    return hotels


  