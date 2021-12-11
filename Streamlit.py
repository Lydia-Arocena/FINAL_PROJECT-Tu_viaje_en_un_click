import streamlit as st
from PIL import Image
import src.geo_functions as gf


st.write ("""
# Make your dream trip a reality just in one click!!
""")

st.text('''In this app you will be able to choose between some travel destinations 
that best meet your needs and requirements. ''')

imagen = Image.open("mapamundi.jpg")
st.image(imagen, use_column_width=True)


city = st.sidebar.text_input('Where will you travel from?', 'Madrid')

radio= st.sidebar.slider('How far would you like to travel?', 200, 19000, 200,step=100)

idomas=["English", "Spanish", "Chinese", "Others"]

date = st.sidebar.date_input("Pick a date")

Language = st.sidebar.radio("Pick a language", idomas)

st.table(gf.df_geonear(city, radio))

