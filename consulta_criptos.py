from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By  # para poder seleccionar elementos con By
from time import sleep
import streamlit as st


# driver.maximize_window()      # hace que se abra el navegador maximizado
def scrap_criptos():

    misCripto = [
        "PAXG-USD"  # PAX Gold
    ]


    cotizaciones = {}
    cotizaciones["Criptos"]={}

    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    options.add_argument("--headless")  # hace que no se abra el navegador a la vita del usuario
    options.page_load_strategy = "eager"
    # Le dice a Selenium: driver.get() vuelve apenas el HTML base cargó ("eager"),
    # sin esperar anuncios ni trackers. Sin esto, get() se queda esperando en Yahoo.


    driver = webdriver.Chrome(options=options) # le decimos que el creome va a ser nuestro navegador

    #url = f"https://es.finance.yahoo.com/quote/{misCripto}/"
    url = f"https://es-us.finanzas.yahoo.com/quote/{misCripto[0]}"

    driver.get(url)                    # accedemos a la web de yahoo finance    

    # buscador = driver.find_element(By.ID,"ybar-sbq")
    # buscador.send_keys(tiker)

    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as ExpCond

    precio = WebDriverWait(driver,20).until(
        ExpCond.visibility_of_element_located((By.CSS_SELECTOR,'span[data-testid="qsp-price"]'))
    )
    precio = precio.text
    
    precio = f"U$d {float(precio.replace(',', '')):.2f}"
    print(precio)

    nombre = driver.find_element(By.CSS_SELECTOR,'h1[class="heading yf-ndxd9a"]')
    nombre = nombre.text

    print(f"{nombre} --> {precio}")

    cotizaciones["Criptos"][nombre]=precio
    print(cotizaciones)
    driver.quit()   # cierra el navegador
    #print(cotizaciones)  
    return cotizaciones

scrap_criptos()
