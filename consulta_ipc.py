import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options # para que no muestre cuando se abre el navegador
import streamlit as st

def scrap_indice_inflacion():
    ########## para ocultar cuando se abre el navegador ########
    # 1. Configuras para que corra oculto en segundo plano
    options = Options()  # Creás una caja vacía donde vas a meter las configuraciones que vos querés cambiar.
    options.add_argument("--headless")  # no abras la ventana visible, trabajá en segundo plano".
    options.add_argument("--window-size=1920,1080")  # Forzar tamaño de pantalla grande oculto

    # 2. Inicializas el driver pasándole esas opciones
    driver = webdriver.Chrome(options=options) # le pasamos como argumento la configuracion del option
    #driver.maximize_window() # hace que se abra maximizada la web
    ########## ************ ########

    # 1. Inicializamos el navegador y cargamos la página web objetivo
    # driver = webdriver.Chrome()
    driver.get("https://habita.ar/indices/ipc")
    time.sleep(2)  # Pausa inicial para asegurar que cargue el DOM base

    td_periodo = driver.find_elements(By.XPATH,'//td[@class="py-2 first-letter:uppercase"]')
    periodo = td_periodo[0].text

    # comom el indice y la variacion son 2 td y tienen la misma class al 1ro accedo con [1]
    td_indice = driver.find_elements(By.XPATH,'//td[@class="py-2 text-right tabular-nums"][1]')
    indice = td_indice[0].text

    # comom el indice y la variacion son 2 td y tienen la misma class al 1ro accedo con [1]
    td_variacion = driver.find_elements(By.XPATH,'//td[@class="py-2 text-right tabular-nums"][2]')
    variacion = td_variacion[0].text

    datos={}
    datos["periodo"] = periodo    
    datos["indice"] = indice
    
    variacion = variacion.replace("+","").replace("%","").replace(",",".").strip()
    print(variacion)
    variacion = float(variacion)
    datos["variacion"] = variacion

    return datos


def muestra_ipc():
    datos = scrap_indice_inflacion()    
    st.metric(label=f"periodo: {datos["periodo"]}", value=datos["indice"], delta=f" {datos["variacion"]} %")
