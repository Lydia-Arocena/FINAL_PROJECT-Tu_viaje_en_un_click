import streamlit as st
from PIL import Image
import time
import src.geo_functions as gf
import src.flights_functions as ff
import src.weather_functions as wf
import pandas as pd



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
destinos_filtrados["Precio vuelo(€)"]=destinos_filtrados["Precio vuelo(€)"].apply(lambda x: round(x,2))
destinos_filtrados=destinos_filtrados[destinos_filtrados["Precio vuelo(€)"]<budget]

st.dataframe(destinos_filtrados)






    


