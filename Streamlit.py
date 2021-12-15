import streamlit as st
from PIL import Image
import time
import sys
sys.path.append('../')

import src.geo_functions as gf
import src.flights_functions as ff
import src.weather_functions as wf
import src.Restaurants_functions as rf
import src.hotels_functions as hf
import src.points_of_interests_functions as pf

import pandas as pd
import folium
from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import HeatMap, MarkerCluster
import streamlit as st
from streamlit_folium import folium_static
import streamlit.components.v1 as components
import streamlit as st
import pandas as pd
import plotly.express as px




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

radio= st.sidebar.slider('How far would you like to travel?', 200, 1000, 200,step=100)

budget= st.sidebar.slider('Which is your budget?', 70, 5000, 100,step=10)



date = st.sidebar.date_input("Pick a date")
date2=date.strftime("%Y-%m-%d")

idomas=["English", "Spanish", "Chinese", "Others"]
Language = st.sidebar.radio("Pick a language", idomas)



with st.spinner('Loading your dream destinations...'):
    time.sleep(60)
st.success('Here you have our recommendations for the cheapest flights and hotels!')




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

destinos["Flight Price(€)"]=precios #apendeo los precios

destinos_filtrados=destinos[destinos["Flight Price(€)"]!='There is not any flight for the selected date']
destinos_filtrados["Flight Price(€)"]=pd.to_numeric(destinos_filtrados["Flight Price(€)"], downcast="float")
destinos_filtrados=destinos_filtrados.sort_values(by=["Flight Price(€)"])
destinos_filtrados=destinos_filtrados.drop_duplicates(subset=['City'])
destinos_filtrados=destinos_filtrados.head(5)

ciudades_h=list(destinos_filtrados.City)


precio_hoteles=[]
for x in ciudades_h:
    barato=hf.cleaning_hotel(x,date2)
    precio_hoteles.append(barato)


destinos_filtrados["Hotel Price(€)"]= precio_hoteles
pt = destinos_filtrados["Flight Price(€)"] + destinos_filtrados["Hotel Price(€)"]
destinos_filtrados["Total Price(€)"] = pt
destinos_filtrados=destinos_filtrados[destinos_filtrados["Total Price(€)"]<budget]



st.dataframe(destinos_filtrados.style.format({"Flight Price(€)":'{:.2f}',"Hotel Price(€)":'{:.2f}',"Total Price(€)":'{:.2f}'}))

fig = px.histogram(destinos_filtrados, x="City", y="Total Price(€)")
fig.add_hline(destinos_filtrados["Total Price(€)"].mean(), line_width=3, line_color="red")
st.plotly_chart(fig)


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
        forecast=wf.cleaning(input_city,3)
        forecast=forecast.drop(columns=["Dates", "Rain", "Snow"])
        #iconos=wf.dibu3(forecast)
        forecast=forecast.drop(columns=["Icon"])
        st.dataframe(forecast.style.format({"Min_temp":'{:.1f}',"Max_temp":'{:.1f}'}))
        #st.image(iconos, use_column_width=True)
        
        
        
        st.write ("""
        ### Museums:
        """)
        museums=pf.cleaning_museums(input_city,10000)
        museums=museums.drop(columns=["Latitud", "Longitud"])
        museums2=st.dataframe(museums.style.format({"Rating":'{:.1f}'}))



        st.write ("""
        ### Restaurant recommendations:
        """)
        restaurants=rf.cleaning_rest(input_city,10000)
        restaurants=restaurants.drop(columns=["Latitud", "Longitud"])
        restaurants2=st.dataframe(restaurants.style.format({"Rating":'{:.1f}'}))
      


        st.write ("""
        ### Restaurants locations map:
        """)

        default_value = input_city
        folium_static(rf.map(input_city,10000))




       



    


