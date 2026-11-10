import requests
import streamlit as st

def api_cedears_acciones():
     
    precios = {}
    precios["Acciones"]={}
    precios["Cedears"]={}
    precios["Acciones U$d"]={}

    API_URL = "https://api.iolinversiones.com"

    auth = requests.post(f"{API_URL}/auth/token", json={
        "grant_type": "password",
        "username": "pollomartinezvidal@hotmail.com",
        "password": "Canela71$"})
    headers = {"Authorization": f"Bearer {auth.json()['data']['access_token']}"}

    def cotizaciones(categoria, panel):
        r = requests.get(f"{API_URL}/broker/market-data/screener",
                        params={"country": "AR", "asset_type": categoria,
                                "panel": panel, "term": "T1"}, headers=headers)
        return r.json()["data"]

    misCedears = [
            "MSFT",    # Microsoft
            "NVDA",    # Nvidia
            "MELI",    # Mercado Libre
            "AAPL",    # Apple
            "KO",    # Coca Cola
            "MCD",    # Mc Donalds
            "GERN",    # Geron Corporation
            "BBD"      # Banco Bradesco
        ]

    mis_acciones= [
            "LOMA",   # Loma Negra
            "TGSU2",    # Transp. Gas del Sur
            "TGNO4",  # Transp. Gas del Norte
            "EDN",    # Edenor
            "MOLI",   # Molinos Río de la Plata
            "ALUA",   # Aluar
            "YPFD",   # YPF
            "GGAL",   # Grupo Galicia
            "PAMP",   # Pampa Energía
            "TRAN",   # Transener
            "TXAR",   # Ternium Argentina    
            "HARG"    # Holcim Argentina        
        ]

    misAcciones_usd = ["BBD", "GERN"]

    # ---------- CONSULTA CEDEARS--------------------------------------
    datos_cedears = cotizaciones("cedears", "argcedearstodos")
    for dato in datos_cedears:
        if dato["instrument"]["symbol"] in misCedears:

            # a precios["Cedears"] le arego la llave del Cedear en pesos y le asigno su precio
            precios["Cedears"][dato["instrument"]["name"]]= f"$  {dato["quotes"]["close"] }"

            print(f"{dato["instrument"]["symbol"]} - {dato["instrument"]["name"]} -> {dato["instrument"]["currency"]} {dato["quotes"]["close"]} ")
            
    # def paneles(categoria):
    #     r = requests.get(f"{API_URL}/broker/assets/panels",
    #                      params={"country": "AR", "asset_type": categoria},
    #                      headers=headers)
    #     return r.json()["data"]

    # print(paneles("acciones"))

    # ---------- --------------------------------------

    # ---------- CONSULTA ACCIONES--------------------------------------
    datos_acciones = cotizaciones("acciones", "argaccionespanelgeneral")

    for dato in datos_acciones:
        if dato["instrument"]["symbol"] in mis_acciones:

                # a precios["Acciones"] le arego la llave de la accion en pesos y le asigno su precio
                precios["Acciones"][dato["instrument"]["name"]]= f"$  {dato["quotes"]["close"] }"

                print(f"{dato["instrument"]["symbol"]} - {dato["instrument"]["name"]} -> {dato["instrument"]["currency"]} {dato["quotes"]["close"]} ")


    #  --------------- ACCIONES EN DOLARES-----------------------
    r = requests.get(f"{API_URL}/broker/market-data/screener",
                    params={"country": "US", "asset_type": "adrs",
                            "panel": "todos", "term": "T1"},
                    headers=headers)
    datos_usd = r.json()["data"]


    for dato in datos_usd:
        if dato["instrument"]["symbol"] in misAcciones_usd:

            # a precios["Acciones U$d"] le arego la llave de la accion en dolares y le asigno su precio
            precios["Acciones U$d"][dato["instrument"]["name"]]= f"U$d  {dato["quotes"]["close"]}"

            print(f"{dato["instrument"]["symbol"]} - {dato["instrument"]["name"]} -> {dato["instrument"]["currency"]} {dato["quotes"]["close"]} ")

    # ------------------------------------------------

    # ---------- CONSULTA GERN--------------------------------------

    r = requests.get(f"{API_URL}/broker/market-data/GERN/quote",
                    params={"market": "NASDAQ", "term": "T1"},
                    headers=headers)

    datos_nasdaq = r.json()

    # a precios["Acciones U$d"] le arego la llave de la accion GERN y le asigno su precio
    precios["Acciones U$d"][datos_nasdaq["data"]["symbol"]] = f"U$d  {datos_nasdaq["data"]["prices"]["close"]}"

    print(datos_nasdaq["data"].keys())
    print(datos_nasdaq["data"]["symbol"])
    print(datos_nasdaq["data"]["prices"]["close"])
    print(datos_nasdaq["data"]["currency"])

    print(precios)
    return precios

def muestra_cedear_acciones():
    
        cotizaciones = api_cedears_acciones()
        for rubro in cotizaciones:
            with st.container(border=True):
                st.success(f"{rubro}")

                titulo_col1,col_precio = st.columns([3,1])
                titulo_col1.markdown("<p style='text-align:center'><b>Titulo</b></p>", unsafe_allow_html=True)
                #col_precio.markdown("<p style='text-align:center'><b>Precio</b></p>", unsafe_allow_html=True)
                #col_tiker.write("**Ticker**") # coloco el titulo d ela columna
                col_precio.write("**Precio**") # coloco el titulo d ela columna

                for tiker in cotizaciones[rubro]:
                    col_tiker,col_precio = st.columns([3,1])
                    with col_tiker:
                        st.write(tiker)

                    with col_precio:
                        #st.write(cotizaciones[rubro][tiker])
                        st.write(str(cotizaciones[rubro][tiker]))
