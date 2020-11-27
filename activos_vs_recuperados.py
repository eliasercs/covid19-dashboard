import streamlit as st
import pandas as pd
import datetime
import altair as alt

now = datetime.datetime.now()

def curva_activos_recuperados(f_inicio,f_termino):
    df = obtener_datos()
    data = pd.DataFrame(data=df)
    data = data.groupby(['Fecha']).sum()
    return data.loc[str(f_inicio):str(f_termino)]

def obtener_datos():
    url = 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto46/activos_vs_recuperados.csv'
    return pd.read_csv(url,header=0,names=['Fecha','Activos','Recuperados'])

def vista():

    day = now.day
    month = now.month
    year = now.year

    st.title('Cantidad de casos activos vs casos recuperados')

    start = st.date_input('Fecha de inicio',value=datetime.date(year,month,day),key=None)
    end = st.date_input('Fecha de término',value=datetime.date(year,month,day),key=None)

    data = curva_activos_recuperados(start,end)

    if data.empty:
        st.error('No existen datos en el rango de fechas: ' + str(start) + '/' + str(end))
    else:
        st.success('Datos encontrados en el rango de fechas: ' + str(start) + '/' + str(end))
        show_hide = st.checkbox('Mostrar/Ocultar información',value=False,key=None)
        if show_hide:
            st.table(data)
        array = []
        for i in data.index:
            array.append(i)
        datos = pd.DataFrame({'Fecha':array,'Activos':data['Activos'],'Recuperados':data['Recuperados']})

        grafico_casos_activos = alt.Chart(datos).mark_area(
            color='red',
            interpolate='step-after',
            line=True
        ).encode(
            alt.X('Fecha:T',title='Fecha'),
            alt.Y('Activos:Q',title='Casos Activos')
        )

        grafico_casos_recuperados = alt.Chart(datos).mark_area(
            color='green',
            interpolate='step-after',
            line=True
        ).encode(
            alt.X('Fecha:T',title='Fecha'),
            alt.Y('Recuperados:Q',title='Casos Recuperados')
        )

        graficos_separados = st.checkbox('Mostrar/Ocultar gráficos por separado',value=False,key=None)
        if graficos_separados:
            st.altair_chart(grafico_casos_activos,use_container_width=True)
            st.altair_chart(grafico_casos_recuperados,use_container_width=True)
        st.line_chart(data)
    st.markdown('Autor: [Eliaser Concha](https://github.com/eliasercs)')

if __name__=='__main__':
    vista()