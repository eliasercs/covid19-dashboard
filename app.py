import streamlit as st
import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
import plotly.express as px
import datetime
import calendar

import defunciones_registro
import casos_covid
import vista_deis
import ocupacion_hospitalaria
import vista_icovid
import tasa_pcr
import r_efectivo
import examenlab
import indicador_carga

# cd Downloads\Python\Streamlit
# streamlit run app.py    

# Config
st.beta_set_page_config(
    page_title="Covid-19 Chile",
 	layout="centered",
 	initial_sidebar_state="expanded",
)

# Sidebar   
st.sidebar.title('Navegación')
opt = st.sidebar.radio("",
    ("Casos", "Defunciones Registro Civil", "Datos Deis",
     "Ocupación Hospitalaria","Positivad Diaria",
      "Tasa PCR", "Índice R", "Tiempo de examen y laboratorio",
      "Indicador de carga"
      )
)
if opt == "Defunciones Registro Civil":
    defunciones_registro.main()

if opt == "Casos":
    casos_covid.main()

if opt == "Datos Deis":
    vista_deis.main()

if opt == "Ocupación Hospitalaria":
    ocupacion_hospitalaria.main()

if opt == "Positivad Diaria":
    vista_icovid.main()

if opt == "Tasa PCR":
    tasa_pcr.show_data()

if opt == "Índice R":
    r_efectivo.show_data()

if opt == "Indicador de carga":
    indicador_carga.show_data()

if opt == "Tiempo de examen y laboratorio":
    examenlab.show_data()