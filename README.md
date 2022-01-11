# Tu_viaje_en_un_click
![portada](Images/mapamundi.jpg)

# Objetivo:
El objetivo de este proyecto es proporcionar al usuario una herramienta que le ayude a elegir un lugar de destino para sus vacaciones. 

Para ello, deberá indicar su presupuesto y distancia máximos como filtros y esta app le propondrá 10 ciudades de entre las que tendrá que seleccionar una. Para la misma, se mostrarán los restaurantes y museos mejor valorados así como un warning indicando la divisa de dicho país por si fuera necesario cambiar dinero antes de viajar.

# Desarrollo:
En primer lugar, creé una base de datos en Mongo DB Compass llamada "Tu_viaje_ideal_en_un_click" y, dentro de ella, creé una colección llamada "coordenadas" donde inserté desde Python los nombres de las ciudades más importantes del mundo junto con el país al que pertenecían, el código IATA de su aeropuerto y sus coordenadas (latitud, longitud).

La app está creada usando Streamlit y se estructura de la siguiente manera:
- Cuando el usuario entra, se le piden dos filtros para obtener las propuestas de destinos:
    1. **Distancia máxima que quiere viajar:** Mediante una Geoquery (geoNear), obtenemos las diez ciudades de la base de datos de Mongo DB Compass más cercanas respecto al punto de origen y radio pasados por el usuario. Se muestran en un dataframe indicando la distancia en kms a la que está cada una.
    2. **Presupuesto**: Es la suma de los precios del vuelo más el del hotel. Estos se obtienen mediante las llamadas a las APIs de Amadeus y Hotels.com, respectivamente.

- Mapa Kepler: se muestra un mapa de arcos desde el punto de origen hacia todas las diferentes propuestas de destino que representan los vuelos.

- A continuación, el usuario elige una de las diez ciudades propuestas en un desplegable. Una vez seleccionado el destino al que quiere viajar, se mostrará la siguiente información al respecto:
    - Aviso indicando la divisa que se utiliza en el país de la ciudad seleccionada para que el usuario sepa que debe cambiar dinero antes de viajar. Los datos relativos a las divisas fueron recolectados haciendo web scraping mediante Selenium.
    - Predicción metereológica: Llamada a la API de Weather API.
    - Restaurantes & Museos: Llamadas a la API de Google Places.
    - Mapa: Usando Folium se muestran en un mapa los restaurantes y museos anteriormente listados identificados por diferentes iconos de distinto color en función de la valoración que tengan.


# Estructura del repositorio:
Este respositorio está organizado de la siguiente manera:
- Config: En esta carpeta se guarda archivos de configuración para el mapa de kepler.
- Data: carpeta donde se almacenan los csvs.
- Images: carpeta que contiene las imágenes utilizadas y el video demo de la app.
- Notebooks: carpeta con diferentes jupyter notebooks utilizados para la realización del proyecto divididos por temáticas (vuelos, hoteles, divisas, coordenadas, restaurantes y predicción metereológica).
- src: carpeta con los archivos .py que recogen las diferentes funciones que he ido creando divididas por materia.
- Streamlit.py: archivo principal del proyecto.

# Tecnologías & Librerías:
- Llamadas a APIS: Amadeus, Hotels.com, Google Places, Weather Api.
- Web scraping.
- Streamlit.
- Base de datos: Mongo DB Compass.
- Librerías:
    - [pymongo](https://pymongo.readthedocs.io/en/stable/)
    - [pandas](https://pandas.pydata.org/docs/)
    - [os](https://docs.python.org/3/library/os.html)
    - [dotenv](https://pypi.org/project/python-dotenv/)
    - [re](https://docs.python.org/3/library/re.html)
    - [geopy](https://geopy.readthedocs.io/en/stable/)
    - [requests](https://docs.python-requests.org/en/latest/)
    - [sys](https://docs.python.org/3/library/sys.html)
    - [json](https://docs.python.org/3/library/json.html)
    - [folium](https://python-visualization.github.io/folium/) 
    - [datetime](https://docs.python.org/3/library/datetime.html)
    - [selenium](https://selenium-python.readthedocs.io/)
    - [unicodedata](https://docs.python.org/3/library/unicodedata.html)
    - [deep_translator](https://deep-translator.readthedocs.io/en/latest/)
    - [ast](https://docs.python.org/3/library/ast.html) 
    - [amadeus](https://amadeus.readthedocs.io/en/latest/) 




