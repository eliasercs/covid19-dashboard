import streamlit as st
import pandas as pd
import numpy as np


URL_DATOS = ('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/ReporteDiario/PCR.csv')

st.title("Cantidad de exámenes PCR por cada 1000 habitantes")


pcr_csv = pd.read_csv(URL_DATOS, index_col='Codigo region')

fechas = pcr_csv.loc[:, '2020-04-09' :]

regiones = pcr_csv['Region']
Poblacion   = pcr_csv['Poblacion']
reg_pcr = pcr_csv.drop(columns=['Poblacion'])
regsum = reg_pcr.sort_index().sum(axis=1)
def pcr_1000(row):
    pcr_hab = ((row["PCR Totales"])/row["Poblacion"])*1000

    return pcr_hab


pcr_final = pd.concat([regiones,Poblacion, regsum], axis = 1).rename(columns={0: 'PCR Totales'})
pcr_final["PCR por 1000 hab"] = pcr_final.apply(pcr_1000, axis=1)
test = pcr_csv[['Region', 'Poblacion']]

#regsum["PCR por 1000 hab"] = regsum["0"]
#st.write(pcr_csv.sort_index())
st.write(pcr_final)






