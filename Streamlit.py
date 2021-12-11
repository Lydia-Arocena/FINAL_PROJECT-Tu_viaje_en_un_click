import streamlit as st
from PIL import Image

st.write ("""
# Make your dream trip a reality just in one click!!
""")

st.text('''In this app you will be able to choose between some travel destinations 
that best meet your needs and requirements. ''')

imagen = Image.open("mapamundi.jpg")
st.image(imagen, use_column_width=True)

radio= st.sidebar.slider('How far would you like to travel?', 500, 10000, 800)



