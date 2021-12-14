import streamlit as st
from PIL import Image
import time
import src.geo_functions as gf
import src.flights_functions as ff
import src.weather_functions as wf
import src.Restaurants_functions as rf
import src.points_of_interests_functions as pf
import pandas as pd
import folium
from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import HeatMap, MarkerCluster
import streamlit as st
from streamlit_folium import folium_static
import streamlit.components.v1 as components




st.write ("""
# Make your dream trip a reality just in one click!! 🌍
""")

st.text('''In this app you will be able to choose between some travel destinations 
that best meet your needs and requirements. ''')

imagen = Image.open("mapamundi.jpg")
st.image(imagen, use_column_width=True)



city = st.sidebar.text_input('Where will you travel from?', 'Madrid')

if not city:
    #st.warning('Please, introduce a city!!')
    st.stop()

radio= st.sidebar.slider('How far would you like to travel?', 200, 10000, 200,step=100)

budget= st.sidebar.slider('Which is your budget?', 70, 5000, 100,step=10)

idomas=["English", "Spanish", "Chinese", "Others"]

date = st.sidebar.date_input("Pick a date")
date2=date.strftime("%Y-%m-%d")


Language = st.sidebar.radio("Pick a language", idomas)



with st.spinner('Loading your dream destinations...'):
    time.sleep(5)
st.success('Here you have our recommendations!')




origen=ff.get_IATA(city)

destinos=gf.df_geonear(city, radio)
lista_destinos=list(destinos.City)

#itero sobre la lista_kms haciendo query de mongo para sacar los IATAS y los almaceno en una lista.
IATAS_=[]

for d in lista_destinos:
    iata = ff.get_IATA(d)
    IATAS_.append(iata)
    


precios=[]
for i in IATAS_:
    try:
        precio=ff.get_cheapest_price(city,i,date2)
        precios.append(precio)
    except:
        pass

destinos["Precio vuelo(€)"]=precios #apendeo los precios

destinos_filtrados=destinos[destinos["Precio vuelo(€)"]!='There is not any flight for the selected date']
destinos_filtrados["Precio vuelo(€)"]=pd.to_numeric(destinos_filtrados["Precio vuelo(€)"], downcast="float")
destinos_filtrados=destinos_filtrados[destinos_filtrados["Precio vuelo(€)"]<budget]
destinos_filtrados=destinos_filtrados.sort_values(by=["Precio vuelo(€)"])
destinos_filtrados=destinos_filtrados.head(5)
st.dataframe(destinos_filtrados.style.format({"Precio vuelo(€)":'{:.2f}'}))


if destinos_filtrados.shape[0]==0:
    pass
else:
    opciones_ciudades = list(destinos_filtrados.City)
    input_city= st.selectbox("Which is your favourite option?",["Choose an option"] + opciones_ciudades)
    if input_city=="Choose an option":
        pass
    else:
        st.write ("""
        ### Weather forecast:
        """)
        st.dataframe(wf.cleaning(input_city,3))
        st.write ("""
        ### Restaurant recommendations:
        """)
        restaurants=rf.cleaning_rest(input_city,10000)
        restaurants2=st.dataframe(restaurants.drop(columns=["Latitud", "Longitud"]))
        #points=pf.get_points_interest(input_city)
        #if points=="Raise error":
            #st.write("""There is not any interest points in this City""")
        #else:
            #st.table(points)
        #st.table(pf.get_points_interest(input_city))

        st.write ("""
        ### Restaurants:
        """)

        default_value = input_city
        user_input_dire = st.text_input("Introduce dirección", default_value)
        folium_static(rf.map(input_city,10000))




       



    


