import streamlit as st
import requests

def index():
    st.title('Página de inicio')

def obtener_imagen():
    image = 'https://api.nasa.gov/planetary/apod?api_key=6PmnxwBjbCASNtXg6uEPmzbHvnX1EsoxUvH0VqHo'
    res = requests.get(image)
    if res.status_code==200: 
        imagenJson = res.json()
        st.title('APOD: Astronomy Picture of the day')
        st.image(imagenJson['url'],caption=imagenJson['title'],width=None,use_column_width=True,channels='RGB',output_format='auto')
        st.write(imagenJson['date'])
        st.write(imagenJson['explanation'])
    else:
        st.title('Error al conectar con la API')