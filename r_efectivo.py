import streamlit as st
import pandas as pd
import datetime

@st.cache
def csv_r_nacional():
    URL_DATOS = (
        'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/UC/r.nacional.csv')
    return URL_DATOS

@st.cache
def csv_r_regional():
    URL_DATOS = (
        'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/UC/r.regional.csv')
    return URL_DATOS

@st.cache
def get_nac_fechas(f1, f2):
    r_nac = pd.read_csv(csv_r_nacional(), sep=';')
    r_nac = r_nac.groupby(['fecha']).sum()
    r_nac = r_nac.loc[str(f1) : str(f2)]
  
    
    return r_nac

def diccionario_regiones():
    dc = {
        1: 'Tarapacá', 2: 'Antofagasta', 3: 'Atacama', 4: 'Coquimbo',
        5: 'Valparaíso', 6: 'Del Libertador General Bernardo O’Higgins',
        7: 'Maule', 8: 'Biobio', 9: 'La Araucanía', 10: 'Los Lagos',
        11: 'Aysén', 12: 'Magallanes y la Antártica', 13: 'Metropolitana',
        14: 'Los Ríos', 15: 'Arica y Parinacota', 16: 'Ñuble'
    }
    return dc


@st.cache
def get_reg():
    reg = pd.read_csv(csv_r_regional(), sep=';')

    return reg
def get_reg_fecha(fecha):
    reg_f = get_reg()
    reg_f = reg_f.drop(columns=['r.liminf', 'r.lisup'])
    reg_f = reg_f[reg_f['fecha'] == fecha]
    reg_f['region'] = reg_f['region'].map(diccionario_regiones())
    reg_f = reg_f.groupby(['region']).sum()
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
    st.title('Comparación de R efectivo')
    grf = st.selectbox(
        'Seleccione', ['Gráfico a nivel nacional', 'Comparación por regiones']
    )
    if grf == 'Comparación por regiones':
        date = st.date_input('Seleccione fecha', datetime.date(yr, month, day))
        result_reg = get_reg_fecha(str(date))
        if isinstance(result_reg, pd.DataFrame):
            st.title('Comparación de indice R por regiones')
            st.subheader('Fecha:' + str(date))
            st.bar_chart(result_reg)
            data_btn  = st.checkbox("Mostrar tabla de datos")
            fulldata_btn = st.checkbox("Mostrar tabla de datos completa")

            if data_btn:
                grf2 = st.write(result_reg)
            if fulldata_btn:
                grf2= st.write(get_reg())

        else:
            st.error(result_reg)
    else:
        date_inicio = st.date_input('Fecha inicio', datetime.date(yr,month,day))
        date_final = st.date_input('Fecha término', datetime.date(yr,month,day))
        result_nac = get_nac_fechas(date_inicio,date_final)
        st.line_chart(result_nac)

        #st.write(result_nac)
    
    
show_data()
