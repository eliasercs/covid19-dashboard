import streamlit as st
import pandas as pd

product9 = 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto9/HospitalizadosUCIEtario_T.csv'
datos_product9 = pd.read_csv(product9,sep=',',header=0,names=['<=39','40-49','50-59','60-69','>=70'],index_col=False)

def index():
    st.title('Inicio Datos COVID')

def tabla_pacientes_uci():
    st.title('Tabla de Pacientes UCI por rango etario')
    st.table(datos_product9)

def grafico_pacientes_uci():
    st.title('Gráfico de Pacientes UCI por rango etario')
    st.line_chart(datos_product9)