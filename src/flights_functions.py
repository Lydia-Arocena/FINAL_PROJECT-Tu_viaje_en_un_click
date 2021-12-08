import os
from dotenv import load_dotenv
from amadeus import Client, ResponseError
import re


def get_cheapest_price(origen,destino,fecha):
    """
    Esta función me devuelve el precio más bajo para un origen, destino y fecha dadas por el usuario.
    Args:origen = un str de 3 letras (el código IATA del aeropuerto de origen).
         destino = un str de 3 letras (el código IATA del aeropuerto de destino).
         fecha = un str en formato yyyy-mm-dd con la fecha de vuelo.
    Return: El precio más bajo para el vuelo seleccionado.
    
    """
    load_dotenv()
    amadeus = Client(
        client_id= os.getenv("API_Key"),
        client_secret= os.getenv("API_Secret")
)
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origen,
            destinationLocationCode=destino,
            departureDate=fecha,
            adults=1)
        list_prices=[]
        for i in range(len(response.data)):
            price=response.data[i]['price']['total']
            list_prices.append(price)
        return f"The minimun price among all available flights is {min(list_prices)} euros"
    except ResponseError as error:
        return "There is not any fight for the selected date"




def get_min_duration(origen,destino,fecha):
    """
    Esta función me devuelve la duración mínima de los vuelos disponibles para un origen, destino y fecha dadas por el usuario.
    Args:origen = un str de 3 letras (el código IATA del aeropuerto de origen).
         destino = un str de 3 letras (el código IATA del aeropuerto de destino).
         fecha = un str en formato yyyy-mm-dd con la fecha de vuelo.
    Return: La duración mínima de los vuelos disponibles según los argumentos dados.
    
    """
    load_dotenv()
    amadeus = Client(
        client_id= os.getenv("API_Key"),
        client_secret= os.getenv("API_Secret")
)
    try:
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origen,
            destinationLocationCode=destino,
            departureDate=fecha,
            adults=1)
        list_duration=[]
        for i in range(len(response.data)):
            duration=response.data[i]['itineraries'][0]['duration']
            dur=re.findall('[0-9]+', duration)
            lista_dur=[int(x) for x in dur]
            list_duration.append(total_hours(lista_dur))
        return f"The fastest flight lasts {min(list_duration)} hours."
    except ResponseError as error:
        return "Duration not found"
        

    


def total_hours(total):
    """
    Esta función devuelve las horas totales con decimales.
    Args: una lista con dos elementos: el primero horas y el segundo minutos.
    Return: La suma de las horas y minutos en forma de hora (número decimal).
    """
    try:
        return round(total[0]+total[1]/60,1)
    except: 
        return total[0]

   