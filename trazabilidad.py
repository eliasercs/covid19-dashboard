import streamlit as st
import pandas as pd
import datetime
import casos_activos
import examenlab

now = datetime.datetime.now()

regiones = [
    'Tarapacá','Antofagasta','Atacama','Coquimbo','Valparaíso','O’Higgins','Maule','Biobío',
    'Araucanía','Los Lagos','Aysén','Magallanes','Metropolitana','Los Ríos','Arica y Parinacota',
    'Ñuble'
]

def obtener_confirmacion_temprana_regional_fecha(region,f1,f2):
    df = confirmacion_temprana_regional()
    carga = []
    r = []
    fecha = []
    for i in df.index:
        if df['Region'][i] == region and df['prop3d'][i] != 'NaN':
            carga.append(df['prop3d'][i])
            r.append(df['Region'][i])
            fecha.append(df['fecha_primeros_sintomas'][i])
    d = {'Región':r,'Fecha':fecha,'Carga':carga}
    df = pd.DataFrame(data=d)
    df = df.groupby(['Fecha']).sum()
    return df.loc[str(f1):str(f2)]

def obtener_consulta_temprana_regional_fecha(region,f1,f2):
    df = consulta_temprana_regional()
    carga = []
    r = []
    fecha = []
    for i in df.index:
        if df['Región'][i] == region and df['Carga'][i] != 'NaN':
            carga.append(df['Carga'][i])
            r.append(df['Región'][i])
            fecha.append(df['Fecha'][i])
    d = {'Región':r,'Fecha':fecha,'Carga':carga}
    df = pd.DataFrame(data=d)
    df = df.groupby(['Fecha']).sum()
    return df.loc[str(f1):str(f2)]

def obtener_confirmacion_temprana_nacional_fecha(f1,f2):
    df = confirmacion_temprana_nacional()
    df = df.groupby(['Fecha']).sum()
    return df.loc[str(f1):str(f2)]

def obtener_consulta_temprana_nacional_fecha(f1,f2):
    df = consulta_temprana_nacional()
    df = df.groupby(['Fecha']).sum()
    return df.loc[str(f1):str(f2)]

def confirmacion_temprana_nacional():
    url = 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto70/total72.nacional.csv'
    return pd.read_csv(url,header=0,names=['Fecha','Carga'])

def confirmacion_temprana_regional():
    url = 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto70/total72.regional.csv'
    return pd.read_csv(url,header=0)

def consulta_temprana_nacional():
    url = 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto71/not48.nacional.csv'
    return pd.read_csv(url,header=0,names=['Fecha','Carga'])

def consulta_temprana_regional():
    url = 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto71/not48.regional.csv'
    return pd.read_csv(url,header=0,names=['Región','Código','Fecha','Carga'])

def vista_confirmacion_temprana():
    comparacion = st.selectbox('Seleccione un indicador a comparar',['Nacional','Regional'])
    day = now.day
    month = now.month
    year = now.year
    fecha_inicio = st.date_input('Fecha de inicio',value=datetime.date(year,month,day),key=None)
    fecha_final = st.date_input('Fecha de término',value=datetime.date(year,month,day),key=None)
    st.markdown('## Confirmación temprana de casos a nivel '+comparacion)
    if comparacion=='Nacional':
        carga = obtener_confirmacion_temprana_nacional_fecha(fecha_inicio,fecha_final)
        if carga.empty:
            st.error('No existen datos en el rango de fechas: ' + str(fecha_inicio) + '-' + str(fecha_final))
        else:
            st.success('Datos encontrados en el rango de fechas: ' + str(fecha_inicio) + '-' + str(fecha_final))
            st.line_chart(carga)
    elif comparacion=='Regional':
        region = st.selectbox('Seleccione una o varias regiones:',regiones)
        ds = obtener_confirmacion_temprana_regional_fecha(region,fecha_inicio,fecha_final)
        if ds.empty:
            st.error('No existen datos en el rango de fechas: ' + str(fecha_inicio) + '/' + str(fecha_final))
        else:
            st.success('Datos encontrados en el rango de fechas: ' + str(fecha_inicio) + '/' + str(fecha_final))
            show_hide = st.checkbox('Mostrar/Ocultar carga',value=False,key=None)
            if show_hide:
                st.table(ds)
            st.line_chart(ds)

def vista_consulta_temprana():
    comparacion = st.selectbox('Seleccione un indicador a comparar',['Nacional','Regional'])
    day = now.day
    month = now.month
    year = now.year
    fecha_inicio = st.date_input('Fecha de inicio',value=datetime.date(year,month,day),key=None)
    fecha_final = st.date_input('Fecha de término',value=datetime.date(year,month,day),key=None)
    st.markdown('## Consulta temprana de casos a nivel '+comparacion)
    if comparacion=='Nacional':
        carga = obtener_consulta_temprana_nacional_fecha(fecha_inicio,fecha_final)
        if carga.empty:
            st.error('No existen datos en el rango de fechas: ' + str(fecha_inicio) + '/' + str(fecha_final))
        else:
            st.success('Datos encontrados en el rango de fechas: ' + str(fecha_inicio) + '/' + str(fecha_final))
            st.line_chart(carga)
    elif comparacion=='Regional':
        region = st.selectbox('Seleccione una o varias regiones',
            regiones
        )
        ds = obtener_consulta_temprana_regional_fecha(region,fecha_inicio,fecha_final)
        if ds.empty:
            st.error('No existen datos en el rango de fechas: ' + str(fecha_inicio) + '/' + str(fecha_final))
        else:
            st.success('Datos encontrados en el rango de fechas: ' + str(fecha_inicio) + '/' + str(fecha_final))
            show_hide = st.checkbox('Mostrar/Ocultar carga',value=False,key=None)
            if show_hide:
                st.table(ds)
            st.line_chart(ds)

def vista():
    st.title('Trazabilidad y aislamiento')
    st.markdown('El objetivo de la trazabilidad y aislamiento es detectar de forma adecuada los casos y '+
    'aislarlos identificando los contactos e indicar cuarentena junto con dar seguimiento y apoyo para '+
    'cumplir con las medidas sanitarias y contener un eventual nuevo brote de Sars-Cov-II.')
    st.markdown('Este proceso requiere ser monitoreado con indicadores que permitan dar cuenta de conceptos '
    +'relevantes para la efectividad:')
    st.markdown('* Velocidad o precocidad del aislamiento de casos y cuarentena de contactos.')
    st.markdown('* Cobertura: cuántos casos y contactos totales están aislados y en cuarentena.')
    st.markdown('A pesar de que actualmente Chile reporte casos a través de los informes epidemiológicos, '
    +'es necesario complementar con otros indicadores que den cuenta de la velocidad y cobertura de aislamiento '
    +'de casos sintomáticos y los tiempos asociados a la aplicación de exámenes en laboratorios.')
    st.markdown('El problema con los registros epidemiológicos es que es dificil reportar el momento en el que '
    +'el paciente debe tomar el aislamiento, para estos casos se toma en consideración el momento en el que el '
    +'el paciente consulta al médico y es ingresado al sistema de registros como posible contagio (sospechoso). '
    +'El problema con esto, es que el seguimiento que se realiza no es lo suficientemente efectivo debido al '
    +'transcurso del tiempo ocurrido entre contraer la enfermedad y consultar un médico.')
    st.markdown('A continuación, se describen los indicadores que intentan describir la velocidad y cobertura de '
    +'distintos hitos de testeo, aislamiento y trazabilidad cuya interpretación debe considerar la limitación antes mencionada')

    indicador = st.selectbox('Seleccione un indicador',
        ['Confirmación temprana de casos','Consulta temprana','Tiempo de examen y laboratorio'])

    if indicador=='Confirmación temprana de casos':
        vista_confirmacion_temprana()
    elif indicador=='Consulta temprana':
        vista_consulta_temprana()
    elif indicador=='Tiempo de examen y laboratorio':
        examenlab.show_data()


if __name__ == "__main__":
    vista()