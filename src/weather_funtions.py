import requests
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

def Api_request(ciudad,dias):
    url= "http://api.weatherapi.com/v1/forecast.json"
    parameters={'key':os.getenv("API_weather"),'q':ciudad,'days':dias}
    response=requests.get(url,params=parameters).json
    return response