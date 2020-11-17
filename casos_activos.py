import streamlit as st
import pandas as pd
from datetime import date
from datetime import datetime

now = datetime.now()
producto = 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto19/CasosActivosPorComuna.csv'

def obtener_regiones():
    datos = pd.read_csv(producto,header=0)
    reg = []
    regiones = datos['Region']
    for i in regiones:
        if i not in reg:
            reg.append(i)
    return reg

def obtener_comuna(region):
    data = pd.read_csv(producto,header=0)
    comunas = []
    df = data[['Region','Comuna']]
    for i in df.index:
        if df['Region'][i] == region:
            if df['Comuna'][i] != 'Total' and df['Comuna'][i] != 'Desconocido '+region:
                comunas.append(df['Comuna'][i])
    return comunas

def get_total_casos_activos_region_fecha(date, region):
    data = pd.read_csv(producto,header=0)
    total = 0
    if date in data.columns:
        df = data[['Region','Comuna',date]]
        for i in df.index:
            if df['Region'][i]==region and df['Comuna'][i] == 'Total':
                total = df[date][i]
        return total
    else:
        return 'La fecha ingresada no existe'

def get_fechas():
    data = pd.read_csv(producto)
    columnas = data.columns
    array = []
    for i in range(5,len(columnas)):
        array.append(columnas[i])
    return array

def get_totales_activos(fechas,region):
    total_activos = []
    for e in fechas:
        if get_total_casos_activos_region_fecha(e,region)!='La fecha ingresada no existe':
            total_activos.append(get_total_casos_activos_region_fecha(e,region))
    return total_activos

def main():
    graf = st.selectbox(
        'Seleccione un criterio a comparar',
        ['Total de casos activos por región','Total de casos activos por comuna']
    )
    st.sidebar.markdown('---')
    fechas = get_fechas()
    st.sidebar.markdown('Primera fecha registrada: '+fechas[0])
    st.sidebar.markdown('Última fecha registrada: '+fechas[-1])
    st.info('INFORMACIÓN: Considere que la frecuencia de actualización de los datos oficiales es cada 2 o 3 días')
    if graf=='Total de casos activos por región':
        st.title('Total de casos activos por Región')
        region = st.selectbox(
            'Seleccione la región de su preferencia',
            obtener_regiones()
        )
        #st.write(get_total_casos_activos_region_fecha(end_time.strftime('%Y-%m-%d'),region))
        #st.write(get_totales_activos(fechas,region))
        chart_data = st.line_chart(get_totales_activos(fechas,region))
    elif graf=='Total de casos activos por comuna':
        st.title('Total de casos activos por Comuna')
        region = st.selectbox(
            'Seleccione la región de su preferencia',
            obtener_regiones()
        )
        comuna = st.selectbox(
            'Seleccione la comuna de su preferencia',
            obtener_comuna(region)
        )

    st.markdown('Autor: [Eliaser Concha](https://github.com/eliasercs)')