import streamlit as st
import pandas as pd
import numpy as np


def get_csv():
    URL_DATOS = (
        'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/ReporteDiario/PCR.csv')

    return URL_DATOS


def pcr_1000(row):
    pcr_hab = ((row["PCR Totales"])/row["Poblacion"])*1000

    return pcr_hab


def get_datos():
    pcr = pd.read_csv(get_csv(), index_col='Codigo region')
    pcr = pcr.sort_index()
    return pcr


def get_graficable():
    # crea dataframe con todos los datos
    pcr_csv = pd.read_csv(get_csv(), index_col='Codigo region')
    # dataframe con sólo fechas
    fechas = pcr_csv.loc[:, '2020-04-09':]
    # series con la columa region de pcr_csv
    regiones = pcr_csv['Region']
    # series con la columna poblacion de pcr_csv
    Poblacion = pcr_csv['Poblacion']
    #
    reg_pcr = pcr_csv.drop(columns=['Poblacion'])
    regsum = reg_pcr.sort_index().sum(axis=1)

    pcr_final = pd.concat([regiones, Poblacion, regsum],
                          axis=1).rename(columns={0: 'PCR Totales'})
    pcr_final["PCR por 1000 hab"] = pcr_final.apply(pcr_1000, axis=1)

    pcr_graph = pcr_final[['Region', 'PCR por 1000 hab']]
    pcr_graph = pcr_graph.set_index('Region')

    return pcr_graph


def pcr_by_reg(reg):
    df = get_datos()
    df = df.query('Region.isin(@reg)')
    df.groupby(['Region']).sum()
    df
    return df 

def show_data():
    st.title("Cantidad de exámenes PCR por cada 1000 habitantes")

    st.bar_chart(get_graficable())
    datos_btn = st.checkbox("Mostrar datos")
    if datos_btn:
        graf = st.write(get_graficable())
        datos_full_btn = st.checkbox("Mostrar datos sin calcular")
        if datos_full_btn:
            graf = st.write(get_datos())



