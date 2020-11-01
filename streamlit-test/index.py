import streamlit as st
import funciones as fun

if __name__=='__main__':
    menu = st.sidebar.selectbox(
        "API's",
        ['Elija una opción','APOD','InSight']
    )
    if menu=='Elija una opción':
        fun.index()
    elif menu=='APOD':
        fun.obtener_imagen()
    else:
        st.write('API no encontrada')