import streamlit as st
import pandas as pd
import datetime

now = datetime.datetime.now()

def obtener_datos():
    url = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto19/CasosActivosPorComuna_std.csv"
    return pd.read_csv(url,header=0)

@st.cache
def obtener_fecha_inicio():
    df = obtener_datos()
    fechas = []
    for i in df['Fecha']:
        if i not in fechas:
            fechas.append(i)
    return fechas[0]

@st.cache
def obtener_regiones():
    df = obtener_datos()
    regiones = []
    for i in df['Region']:
        if i not in regiones:
            regiones.append(i)
    return regiones

@st.cache
def obtener_comunas(region):
    df = obtener_datos()
    comunas = []
    for i in range(len(df)):
        if df['Region'][i]==region and (df['Comuna'][i]!='Desconocido '+region and df['Comuna'][i]!='Total'):
            if df['Comuna'][i] not in comunas:
                comunas.append(df['Comuna'][i])
    return comunas

@st.cache(allow_output_mutation=True)
def filtrar_datos_region_fecha(region,fecha_inicio,fecha_termino):
    df = obtener_datos()
    df = pd.DataFrame(data=df)
    data = pd.DataFrame()
    for i in range(len(df)):
        if df.loc[i,'Region']==region and df.loc[i,'Comuna']=='Total':
            data[i] = df.loc[i]
    data = data.T
    data = data.drop(columns=['Codigo region','Comuna','Codigo comuna','Region','Poblacion'])
    data = data.groupby(['Fecha']).sum()
    data = data.loc[str(fecha_inicio):str(fecha_termino)]
    data.rename(columns={'Casos activos':str(region)},inplace=True)
    return data

@st.cache(allow_output_mutation=True)
def filtrar_datos_comuna_fecha(comuna,fecha_inicio,fecha_termino):
    df = obtener_datos()
    df = pd.DataFrame(data=df)
    data = pd.DataFrame()
    for i in range(len(df)):
        if df.loc[i,'Comuna']==comuna:
            data[i] = df.loc[i]
    data = data.T
    data = data.drop(columns=['Region','Codigo region','Codigo comuna','Poblacion','Comuna'])
    data = data.groupby(['Fecha']).sum()
    data = data.loc[str(fecha_inicio):str(fecha_termino)]
    data.rename(columns={'Casos activos':str(comuna)},inplace=True)
    return data

def vista_activos():
    day = now.day
    month = now.month
    year = now.year

    fecha_inicio = obtener_fecha_inicio()

    st.title('Casos Activos')

    start = st.date_input('Fecha de inicio',value=datetime.date(int(fecha_inicio[0:4]),int(fecha_inicio[5:7]),int(fecha_inicio[8:])),key=None)
    end = st.date_input('Fecha de término',value=datetime.date(year,month,day),key=None)

    criterio_comparacion = st.selectbox('Seleccione un criterio a comparar',['Región','Comuna'])

    st.info('INFORMACIÓN: Considere que la frecuencia de actualización de los datos oficiales es cada 2 o 3 días')
    
    if criterio_comparacion=='Región':
        st.title('Total de casos activos por Región')
        r = st.multiselect('Seleccione una o varias regiones',obtener_regiones(),default=['Arica y Parinacota','Tarapaca','Antofagasta'])
        if len(r)>=1:
            data = pd.DataFrame()
            
            data = filtrar_datos_region_fecha(r[0],start,end)

            for i in range(len(r)):
                data[r[i]] = filtrar_datos_region_fecha(r[i],start,end)

            mostrar_datos = st.checkbox('Mostrar datos',value=False,key=None)
            st.success('Información encontrada en el rango de fechas: ' + str(start) + '/' + str(end))
            if mostrar_datos:
                st.table(data)
            st.line_chart(data)
        else:
            st.error('Tiene que seleccionar al menos una región.')
    elif criterio_comparacion=='Comuna':
        st.title('Total de casos activos por Comuna')
        r = st.selectbox('Seleccione una región',obtener_regiones())
        c = st.multiselect('Seleccione una comuna',options=obtener_comunas(r),default=None)
        if len(c)>=1:
            data = pd.DataFrame()
            data = filtrar_datos_comuna_fecha(c[0],start,end)

            for com in range(len(c)):
                data[c[com]] = filtrar_datos_comuna_fecha(c[com],start,end)

            mostrar_datos = st.checkbox('Mostrar datos',value=False,key=None)
            st.success('Información encontrada en el rango de fechas: ' + str(start) + '/' + str(end))
            if mostrar_datos:
                st.table(data)
            st.line_chart(data)

        else:
            st.error('Tiene que seleccionar al menos una comuna.')

    st.markdown('Autor: [Eliaser Concha](https://github.com/eliasercs)')

if __name__=='__main__':
    vista_activos()