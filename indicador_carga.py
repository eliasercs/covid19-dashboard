import streamlit as st
import pandas as pd
import datetime


def csv_carga_nac():
    URL_DATOS = (
        'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/UC/carga.nacional.csv')
    return URL_DATOS


def csv_carga_nac_ajustada():
    URL_DATOS = (
        'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/UC/carga.nacional.ajustada.csv')
    return URL_DATOS


def csv_carga_reg():
    URL_DATOS = (
        'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/UC/carga.regional.csv')
    return URL_DATOS


def csv_carga_reg_ajustada():
    URL_DATOS = (
        'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/input/UC/carga.regional.ajustada.csv')
    return URL_DATOS


def get_carga_nac():
    carga_nac = pd.read_csv(csv_carga_nac(), sep=';')
    #carga_nac = carga_nac.groupby(['fecha']).sum()
    return carga_nac


def get_carga_nac_a():
    carga_nac_a = pd.read_csv(csv_carga_nac_ajustada(), sep=';')
    return carga_nac_a


def diccionario_regiones():
    dc = {
        1: 'Tarapacá', 2: 'Antofagasta', 3: 'Atacama', 4: 'Coquimbo',
        5: 'Valparaíso', 6: 'Del Libertador General Bernardo O’Higgins',
        7: 'Maule', 8: 'Biobio', 9: 'La Araucanía', 10: 'Los Lagos',
        11: 'Aysén', 12: 'Magallanes y la Antártica', 13: 'Metropolitana',
        14: 'Los Ríos', 15: 'Arica y Parinacota', 16: 'Ñuble'
    }
    return dc


def get_carga_reg():
    carga_reg = pd.read_csv(csv_carga_reg(), sep=';')

    carga_reg['region'] = carga_reg['region'].map(diccionario_regiones())
    return carga_reg


def get_carga_reg_a():
    carga_reg_a = pd.read_csv(csv_carga_reg_ajustada(), sep=';')
    carga_reg_a['region'] = carga_reg_a['region'].map(diccionario_regiones())
    return carga_reg_a


def get_nac_fechas(f1, f2):
    c_nac = pd.read_csv(csv_carga_nac(), sep=';')
    c_nac = c_nac.groupby(['fecha']).sum()
    c_nac = c_nac.loc[str(f1): str(f2)]

    return c_nac


def get_nac_a_fechas(f1, f2):
    c_nac_a = pd.read_csv(csv_carga_nac_ajustada(), sep=';')

    c_nac_a = c_nac_a.groupby(['fecha']).sum()
    c_nac_a = c_nac_a.loc[str(f1): str(f2)]

    return c_nac_a


def get_by_region():

    dfxd
    return dfxd


def get_reg_fecha(fecha):
    r_reg = get_carga_reg()
    r_reg = r_reg.drop(columns=['carga.liminf', 'carga.lisup'])

    r_reg = r_reg[r_reg['fecha'] == fecha]
    r_reg = r_reg.groupby(['region']).sum()
    r_reg = r_reg.sort_index()

    if r_reg.empty:
        return 'No se han encontrado registros'
    else:
        return r_reg

def show_data():
    current = datetime.datetime.now()
    yr = current.year
    month = current.month
    day = current.day

    st.title('Indicadores de carga a nivel nacional y regional')

    sel = st.selectbox('Seleccione opción', [
        'Gráfico a nivel nacional', 'Comparación por regiones'])
    if sel == 'Gráfico a nivel nacional':
        acu = st.checkbox('Mostrar carga acumulada')

        if acu:
            date_inicio = st.date_input(
                'Fecha inicio', datetime.date(yr, month, day))
            date_final = st.date_input(
                'Fecha término', datetime.date(yr, month, day))
            result_nac = get_nac_a_fechas(date_inicio, date_final)
            st.line_chart(result_nac)
        else:
            date_inicio = st.date_input(
                'Fecha inicio', datetime.date(yr, month, day))
            date_final = st.date_input(
                'Fecha término', datetime.date(yr, month, day))
            result_nac = get_nac_fechas(date_inicio, date_final)
            st.line_chart(result_nac)
    else:
        date = st.date_input('Seleccione fecha', datetime.date(yr, month, day))
        result_reg = get_reg_fecha(str(date))
        if isinstance(result_reg, pd.DataFrame):
            st.title('Comparación de indicadores de carga regionales')
            st.subheader('Fecha: ' + str(date))
            st.bar_chart(result_reg)
        else:
            st.error(result_reg)


