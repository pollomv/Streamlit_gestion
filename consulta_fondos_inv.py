from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By  # para poder seleccionar elementos con By
from time import sleep
import streamlit as st

def scrap_fdos_inversion():

    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    options.add_argument("--headless")  # hace que no se abra el navegador a la vita del usuario

    options.page_load_strategy = "eager"
    # Le dice a Selenium: driver.get() vuelve apenas el HTML base cargó ("eager"),
    # sin esperar anuncios ni trackers. Sin esto, get() se queda esperando en Yahoo.
    driver = webdriver.Chrome(options=options) 
                   # le deimos que el creome va a ser nuestro navegador    

    fondos_Galicia = [
        "21?clase=21", # Fima acciones
        "68?clase=68", # Fima renta $
        "191?clase=191", # Fima renta Plus
        "663?clase=1370" # Fima Mix I
       
    ]

    fondos_Santander = [
        "149?clase=149", # Super fondo renta $
        "51?clase=51", # Super fondo renta variable
        "631?clase=1278", # Superfondo combinado F.C.I. A
        "226?clase=226" # Superfondo super gestion A
    ]

    fondos = [fondos_Galicia, fondos_Santander]
    data_inversiones={} # diccionario de las inversiones scrapeadas    
    data_inversiones["Fondos Galicia"]={}
    data_inversiones["Fondos Santander"]={}

    for fondo in fondos:
        if fondo == fondos_Galicia:
            tipo_fondo = "Fondos Galicia"
        else:
            tipo_fondo = "Fondos Santander"
            

        for tiker in fondo:

            url = f"https://estadisticas.cafci.org.ar/fondos/{tiker}"
            driver.get(url)                       # accedemos a la web de yahoo finance   

            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as ExpCond

            tabla = WebDriverWait(driver,8).until(
                ExpCond.visibility_of_element_located((By.CSS_SELECTOR,'table[class="tablaRendimientos"]'))
            )

            filas = tabla.find_elements(By.TAG_NAME,"tr")

            fila_nombre_fondo = filas[0].find_elements(By.TAG_NAME,"td")
            nombre_fondo = fila_nombre_fondo[1].text

            fila_valor_cuota = filas[1].find_elements(By.TAG_NAME,"td")
            valor_cuota_parte = fila_valor_cuota[1].text
            valor_cuota_parte = valor_cuota_parte.replace(",","")
            valor_cuota_parte = valor_cuota_parte.split(".")

            
            if len(valor_cuota_parte)>2:
                valor_cuota_parte = f"{valor_cuota_parte[0]}.{valor_cuota_parte[1]},{valor_cuota_parte[2]}" 
            else:
                valor_cuota_parte = f"{valor_cuota_parte[0]},{valor_cuota_parte[1]}"
            #valor_cuota_parte = float(valor_cuota_parte)
            #print(f"{nombre_fondo}  --> {valor_cuota_parte}")
            
            data_inversiones[tipo_fondo][nombre_fondo]=valor_cuota_parte

    driver.quit()   # cierra el navegador
    
    return data_inversiones

def mustra_fondos_inv():

    datos = scrap_fdos_inversion()

    for tipo in datos:
        with st.container(border=True):
            st.warning(f"{tipo}")

            for fondo in datos[tipo]:
                col_tiker,col_precio = st.columns([3,1])
                with col_tiker:
                    st.write(fondo)
            
                with col_precio:
                    st.write(datos[tipo][fondo])
            print(f"fondo {fondo} --> {datos[tipo][fondo]}")
            
    




