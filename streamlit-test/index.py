import streamlit as st
import api as api
import datos_covid as covid

def index():
    st.title('Sobre este proyecto')

if __name__=='__main__':
    options = st.sidebar.selectbox(
        'Obtener Datos',
        ['Elija una opción','API Nasa','Datos Covid']
    )
    if options=='Elija una opción':
        index()
    elif options=='API Nasa':
        menu = st.sidebar.selectbox(
            "API's",
            ['Elija una opción','APOD','InSight']
        )
        if menu=='Elija una opción':
            api.index()
        elif menu=='APOD':
            api.obtener_imagen()
        else:
            st.write('API no encontrada')
    elif options=='Datos Covid':
        busqueda = st.sidebar.selectbox(
            'Parámetro a mostrar',
            ['Elija una opción','Pacientes UCI por rango etario']
        )
        if busqueda=='Elija una opción':
            covid.index()
        elif busqueda=='Pacientes UCI por rango etario':
            options = st.sidebar.selectbox(
                'Opción a mostrar',
                ['Tabla','Gráfico']
            )
            if options=='Tabla':
                covid.tabla_pacientes_uci()
            elif options=='Gráfico':
                covid.grafico_pacientes_uci()