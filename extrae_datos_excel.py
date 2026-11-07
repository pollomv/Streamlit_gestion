from openpyxl import load_workbook
import streamlit as st
import requests, io
import requests

def get_data_excel():
    #****************************** esta parte es para conectar a apis*************************
    url_dolar = "https://api.argentinadatos.com/v1/cotizaciones/dolares"
    respuesta = requests.get(url_dolar, timeout=5)
    info_dolar = respuesta.json()

    ultima_cotizacion_oficial = ""
    ultima_cotizacion_blue = ""

    for item in info_dolar:
        if item["casa"] == "oficial":
            ultima_cotizacion_oficial = item["venta"]

        if item["casa"] == "blue":
            ultima_cotizacion_blue = item["venta"]
    
    #****************************** esta parte es para conectar a apis*************************
    url_riesgoPais = "https://api.argentinadatos.com/v1/finanzas/indices/riesgo-pais/ultimo"   
    respuestaRiesgo = requests.get(url_riesgoPais, timeout=5)
    datos_riesgo = respuestaRiesgo.json()
    riesgoPais = datos_riesgo["valor"]

        #****************************** ---------*************************


    # esta parte es para extraer datos del excel ---------------------
    try:
            libro = load_workbook(io.BytesIO(requests.get(f"https://drive.google.com/uc?export=download&id={st.secrets['EXCEL_ID']}").content), data_only=True)
        hoja_INGRESOS = libro["INGRESOS"]

        valor = hoja_INGRESOS["P11"].value
        tramo_1 = hoja_INGRESOS["N16"].value
        tramo_2 = hoja_INGRESOS["O16"].value
        tramo_3 = hoja_INGRESOS["P16"].value
        exceso = round((hoja_INGRESOS["P10"].value)*100)*-1
        print(valor)

        datos = {
            "tramo1": tramo_1,
            "tramo2": tramo_2,
            "tramo3": tramo_3,
            "actual" : valor,
            "exceso" : exceso,
            "dolar_oficial" : ultima_cotizacion_oficial,
            "dolar_blue" : ultima_cotizacion_blue,
            "riesgo_pais" : riesgoPais
        }
        # st.markdown(''':orange[color naranja]''')

    except KeyError as e:
        datos = e

    return datos

def muestra_datos_excel():
    datos = get_data_excel()
    
    col1,col2,col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.metric(label=f"Riesgo pais:", value=datos["riesgo_pais"])

    with col2:
        with st.container(border=True):
            st.metric(label=f"Dolar Blue:", value=datos["dolar_blue"])

    with col3:
        with st.container(border=True):
            st.metric(label=f"Dolar oficial:", value=datos["dolar_oficial"])
    


    with st.container(border=True):
        col1,col2,col3 = st.columns(3)
        with col1:
            with st.container(border=True):
                st.warning("1er tramo")
                v1 = datos["tramo1"]
                color = "green" if v1 >= 0 else "red"
                st.markdown(f"##  :{color}[ \\$ {v1}]")
        with col2:
            with st.container(border=True):
                st.warning("2do tramo")
                v2 = datos["tramo2"]
                color = "green" if v2 >= 0 else "red"
                st.markdown(f"##  :{color}[ \\$ {v2}]")                           
        with col3:
            with st.container(border=True):
                st.warning("3er tramo")
                v3 = datos["tramo3"]
                color = "green" if v3 >= 0 else "red"
                st.markdown(f"##  :{color}[ \\$ {v3}]") # :{color}[ ... ] pinta todo lo que está entre corchetes.
                                                    # \\$ es el signo pesos. Sin la barra, Streamlit lo toma como una fórmula y se rompe.

        col1,col2,col3 = st.columns(3)
        with col2:
            with st.container(border=True):
                st.metric(label=f"Actual:", value=datos["actual"], delta=f" {datos["exceso"]} %")
