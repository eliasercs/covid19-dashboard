import streamlit as st
import pandas as pd
import numpy as np
import datetime

@st.cache
def csv_lab_nac():
    URL_DATOS = ('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto72/lab24.nacional.csv')
    return URL_DATOS

@st.cache
def csv_lab_reg():
    URL_DATOS = ('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto72/lab24.regional.csv')
    return URL_DATOS

@st.cache
def df_lab_nac():
    
    lab_nac = pd.read_csv(csv_lab_nac())
    return lab_nac

@st.cache
def df_lab_reg():
    lab_reg = pd.read_csv(csv_lab_reg())
  

    return lab_reg


@st.cache
def nac_fechas(f1,f2):
    nac_f = df_lab_nac()
    nac_f = nac_f.groupby(['fecha_notificacion']).sum()
    nac_f = nac_f.loc[str(f1): str(f2)]
    return nac_f

def reg_fecha(fecha):
    reg_f = df_lab_reg()
    reg_f = reg_f.drop(columns=['Codigo region'])
    reg_f = reg_f[reg_f['fecha_notificacion'] == fecha]
    reg_f = reg_f.groupby(['Region']).sum()
    reg_f = reg_f.sort_index()
    if reg_f.empty:
        return 'No se han encontrado registros'
    else:
        return reg_f

def show_data():
    current = datetime.datetime.now()
    yr = current.year
    month = current.month
    day = current.day

    st.title('Tiempo de examen y laboratorio de casos sintomáticos')
    
    sel = st.selectbox('Seleccione opción', [
        'Gráfico a nivel nacional', 'Gráfico por regiones'
    ])

    if sel == 'Gráfico a nivel nacional':
        #acu = st.checkbox()
        date_inicio = st.date_input(
            'Fecha inicio', datetime.date(yr,month,day))
        date_final = st.date_input(
            'Fecha término', datetime.date(yr,month,day))
        result_nac = nac_fechas(date_inicio, date_final)
        st.line_chart(result_nac)
    if sel == 'Gráfico por regiones':
        date = st.date_input(
            'Seleccione fecha', datetime.date(yr,month,day))
        result_reg = reg_fecha(str(date))
        
        if isinstance(result_reg, pd.DataFrame):
            st.title('Tiempo de examen y laboratorio por regiones')
            st.subheader('Fecha: ' + str(date))
            st.bar_chart(result_reg)
            data_btn = st.checkbox('Mostrar tabla de datos')
            if data_btn:
                grf2 = st.write(result_reg)
        else:
            st.error(result_reg)
        

