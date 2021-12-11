import streamlit as st
from PIL import Image
import time
import src.geo_functions as gf
import src.flights_functions as ff
import src.weather_functions as wf



st.write ("""
# Make your dream trip a reality just in one click!! :star:
""")

st.text('''In this app you will be able to choose between some travel destinations 
that best meet your needs and requirements. ''')

imagen = Image.open("mapamundi.jpg")
st.image(imagen, use_column_width=True)



city = st.sidebar.text_input('Where will you travel from?', 'Madrid')

if not city:
    #st.warning('Please, introduce a city!!')
    st.stop()

radio= st.sidebar.slider('How far would you like to travel?', 200, 19000, 200,step=100)

budget= st.sidebar.slider('Which is your budget?', 70, 5000, 100,step=10)

idomas=["English", "Spanish", "Chinese", "Others"]

date = st.sidebar.date_input("Pick a date")

Language = st.sidebar.radio("Pick a language", idomas)


df=st.table(gf.df_geonear(city, radio))



with st.spinner('Loading your dream destinations...'):
    time.sleep(5)
st.success('Here you have our recommendations!')


#st.table(df.iloc[0:5])

#if not destino:
    #st.warning('Please, introduce a city!!')
    #st.stop()




    


