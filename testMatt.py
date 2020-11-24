import streamlit as st
import pandas as pd
import numpy as np


COL_COMUNA =  "Mejillones"
URL_DATOS = ('https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto55/Positividad_por_comuna.csv')


st.title("Testing streamlit + pandas + numpy")
st.header("Datos de positividad en " + COL_COMUNA )


mycsv = pd.read_csv(URL_DATOS)

st.write(mycsv.loc[mycsv['Comuna'] == COL_COMUNA])




