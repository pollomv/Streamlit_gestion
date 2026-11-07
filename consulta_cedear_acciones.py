from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By  # para poder seleccionar elementos con By
from time import sleep
import streamlit as st


# driver.maximize_window()      # hace que se abra el navegador maximizado
def scrap_cedears_acciones():

    mis_acciones= [
        "LOMA.BA",   # Loma Negra
        "TGSU2.BA",    # Transp. Gas del Sur
        "TGNO4.BA",  # Transp. Gas del Norte
        "EDN.BA",    # Edenor
        "MOLI.BA",   # Molinos Río de la Plata
        "ALUA.BA",   # Aluar
        "YPFD.BA",   # YPF
        "GGAL.BA",   # Grupo Galicia
        "PAMP.BA",   # Pampa Energía
        "TRAN.BA",   # Transener
        "TXAR.BA",   # Ternium Argentina    
        "HARG.BA"    # Holcim Argentina        
    ]

    misCedears = [
        "MSFT.BA",    # Microsoft
        "NVDA.BA",    # Nvidia
        "MELI.BA",    # Mercado Libre
        "AAPL.BA",    # Apple
        "KO.BA",    # Coca Cola
        "MCD.BA",    # Mc Donalds
        "GERN",    # Geron Corporation
        "BBD"      # Banco Bradesco
    ]

    misCripto = [
        "PAXG-USD"  # PAX Gold
    ]

    activos = [ mis_acciones, misCedears, misCripto]

    cotizaciones = {}
    cotizaciones["Acciones"]={}
    cotizaciones["Cedears"]={}
    cotizaciones["Criptos"]={}

    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    options.add_argument("--headless")  # hace que no se abra el navegador a la vita del usuario
    options.page_load_strategy = "eager"
    # Le dice a Selenium: driver.get() vuelve apenas el HTML base cargó ("eager"),
    # sin esperar anuncios ni trackers. Sin esto, get() se queda esperando en Yahoo.


    driver = webdriver.Chrome(options=options)                # le decimos que el creome va a ser nuestro navegador

    for activo in activos:
        if activo == mis_acciones:
            tipo = "Acciones"
            print("\nAcciones")

        elif activo == misCedears:
            tipo = "Cedears"
        else:
            tipo = "Criptos"
            print("\nCedears")


        for tiker in activo:

            url = f"https://es-us.finanzas.yahoo.com/quote/{tiker}"
            
            driver.get(url)                    # accedemos a la web de yahoo finance    

            # buscador = driver.find_element(By.ID,"ybar-sbq")
            # buscador.send_keys(tiker)

            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as ExpCond

            # buscar =  WebDriverWait(driver,4).until(                  # esperar 10 segundos 
                #ExpCond.element_to_be_clickable((By.ID,"ybar-search"))  # No intentes escribir hasta que el elemento con ese ID aparezca físicamente
            #)                                                       # Esperá que el botón no solo exista, sino que esté habilitado y listo para recibir un clic
            #buscar.click()

            #  ********* Cuando vas a extraer un dato o leer texto (como un precio o un título) ********
                            # --> visibility_of_element_located   -- el eleemnt solo tiene q esxistir

            #  ********* Cuando vas a hacer clic en un botón (como una lupa o un menú) ********
                            # --> element_to_be_clickable

            precio = WebDriverWait(driver,20).until(
                ExpCond.visibility_of_element_located((By.CSS_SELECTOR,'span[data-testid="qsp-price"]'))
            )
            precio = precio.text

            nombre = driver.find_element(By.CSS_SELECTOR,'h1[class="heading yf-ndxd9a"]')
            nombre = nombre.text

            print(f"{nombre} --> {precio}")

            cotizaciones[tipo][nombre]=precio

    driver.quit()   # cierra el navegador
    #print(cotizaciones)  
    return cotizaciones
    
       # sleep(10)   # pausa para que no se cierre el navegador de golpe 1 vz que termona de leer todo el codigo

def muestra_cedear_acciones():
    
        cotizaciones = scrap_cedears_acciones()
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
                        st.write(cotizaciones[rubro][tiker])