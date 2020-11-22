import streamlit as st
import casos_activos
import pandas as pd

description = 'Esta sección de la aplicación busca permitir la comparación de nuevos casos y los casos totales entre las comunas de una misma región, un aspecto que consideramos relevante para monitorear de mejor manera la nueva enfermedad.'

def obtener_fechas():
    url = 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto1/Covid-19.csv'
    data = pd.read_csv(url,header=0)
    columnas = data.columns
    array = []
    for i in range(5,len(columnas)):
        if columnas[i] != 'Tasa':
            array.append(columnas[i])
    return array

def obtener_semanas():
    url = 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto15/SemanasEpidemiologicas.csv'
    data = pd.read_csv(url,header=0)

    url2 = 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto15/FechaInicioSintomas.csv'
    data2 = pd.read_csv(url2,header=0)

    columnas = data.columns
    semanas = []
    for j in range(1,len(columnas)):
        if columnas[j] in data2.columns:
            semanas.append(columnas[j])
    return semanas

def info_semanas_epid():
    url = 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto15/SemanasEpidemiologicas.csv'
    data = pd.read_csv(url,header=0)

    fecha_inicio = []
    fecha_final = []
    for s in obtener_semanas():
        fecha_inicio.append(data[s][0])
        fecha_final.append(data[s][1])
    info = {
        'Semana': obtener_semanas(),
        'Fecha Inicio': fecha_inicio,
        'Fecha Final': fecha_final}

    return info

@st.cache
def obtener_casos_totales(comuna, fecha):
    url = 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto1/Covid-19.csv'
    df = pd.read_csv(url,header=0)
    total = 0
    if fecha in df.columns:
        data = df[['Comuna',fecha]]
        for i in data.index:
            if data['Comuna'][i]==comuna:
                total = data[fecha][i]
        return total
    else:
        return 'error'

@st.cache
def obtener_casos_totales_comuna(fechas,comuna):
    array = []
    for f in fechas:
        if obtener_casos_totales(comuna,f)!='error':
            array.append(obtener_casos_totales(comuna,f))
    return array

@st.cache
def obtener_casos_nuevos(comuna, semana):
    url = 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto15/FechaInicioSintomas.csv'
    data = pd.read_csv(url,header=0)
    cantidad_nuevos_casos = 0
    if semana in data.columns:
        df = data[['Comuna',semana]]
        for i in df.index:
            if df['Comuna'][i]==comuna:
                cantidad_nuevos_casos = df[semana][i]
        return cantidad_nuevos_casos
    else:
        return 'error'

@st.cache
def obtener_casos_nuevos_comuna(comuna,semanas):
    array = []
    for s in semanas:
        if obtener_casos_nuevos(comuna,s)!='error':
            array.append(obtener_casos_nuevos(comuna,s))
    return array

def main():
    st.info('INFORMACIÓN: Considere que la frecuencia de actualización de los datos oficiales es cada 2 o 3 días.')
    criterio = st.selectbox('Elegir criterio de comparación',
        ['Total de casos confirmados','Nuevos casos confirmados']
    )
    region = st.sidebar.selectbox('Elegir una región',
        casos_activos.obtener_regiones()
    )
    comunas = st.sidebar.multiselect('Seleccione la comuna de su preferencia',
        casos_activos.obtener_comuna(region),
        default = None
    )
    st.title(criterio+' por comuna')
    st.markdown('> '+description)
    if criterio=="Total de casos confirmados":
        st.sidebar.markdown('Fecha de inicio: '+obtener_fechas()[0])
        st.sidebar.markdown('Fecha de término: '+obtener_fechas()[-1])
        if len(comunas)>0:
            lista = []
            for c in comunas:
                lista.append(obtener_casos_totales_comuna(obtener_fechas(),c))
            diccionario = {
                'Fecha':obtener_fechas()}
            for r in range(len(comunas)):
                diccionario[comunas[r]] = lista[r]
            mostrar_datos = st.checkbox('Mostrar datos',value=False,key=None)
            if mostrar_datos:
                st.dataframe(diccionario)
            del diccionario['Fecha']
            st.line_chart(diccionario)
    elif criterio=="Nuevos casos confirmados":
        st.markdown("## Información sobre las semanas epidemiológicas")
        mostrar_semanas = st.checkbox('Mostrar semanas:',value=False,key=None)
        if mostrar_semanas:
            st.table(info_semanas_epid())
        if len(comunas)>0:
            st.markdown('## Información sobre nuevos casos confirmados por comuna')
            casos = []
            for c in comunas:
                casos.append(obtener_casos_nuevos_comuna(c,obtener_semanas()))
            #st.write(casos)
            semanas = []
            for s in range(len(obtener_semanas())):
                semanas.append(obtener_semanas()[s])
            casos_nuevos = {'Semana':semanas}
            for r in range(len(comunas)):
                casos_nuevos[comunas[r]] = casos[r]
            mostrar_datos = st.checkbox('Mostrar datos',value=False,key=None)
            if mostrar_datos:
                st.dataframe(casos_nuevos)
            del casos_nuevos['Semana']
            st.line_chart(casos_nuevos)
    st.markdown('Autor: [Eliaser Concha](https://github.com/eliasercs)')