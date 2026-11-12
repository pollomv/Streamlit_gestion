import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options # para que no muestre cuando se abre el navegador
from selenium.common.exceptions import NoSuchElementException
import streamlit as st

def scrap_noticias():
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
    driver.get("https://www.infobae.com/")
    time.sleep(3)  # Pausa inicial para asegurar que cargue el DOM base

    mis_secciones = ["deportes","economia","sociedad","politica"]
    noticias = {}

    secciones = driver.find_elements(By.XPATH,'//a[@cmp-ltrk="Bloque articulo individual"]')

    for seccion in secciones:
        link = seccion.get_attribute("href")
        rubro = link.replace("https://www.infobae.com/","")
        rubro = rubro.split("/")[0]
        print(rubro)
        if rubro in mis_secciones:

            #div_hermano_seccion = seccion.find_element(By.XPATH,'./following-sibling::div[@class="story-card-info"]')
            try:
                h2_noticias = seccion.find_element(By.XPATH,'.//h2[contains(@class, "headline-link")]')
                h2_noticias = h2_noticias.text
                noticias[h2_noticias] = link

            except NoSuchElementException:
                print("exception")
                print(seccion.get_attribute("outerHTML"))

    
    return noticias

def muestra_noticias():
    with st.container(border=True):
        noticias = scrap_noticias()
        for titulo in noticias:        
            st.markdown(f'<a href="{noticias[titulo]}" target="_blank">{titulo}</a>', unsafe_allow_html=True)
    
