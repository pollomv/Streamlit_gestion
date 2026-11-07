import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options # para que no muestre cuando se abre el navegador
from selenium.common.exceptions import NoSuchElementException
import streamlit as st


def scrap_pronostico():
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
    driver.get("https://weather.com/es-AR/ar/corrientes/city/corrientes/today")
    time.sleep(2)  # Pausa inicial para asegurar que cargue el DOM base
    
    caja_temp_actual = driver.find_element(By.XPATH,'//span[@class="text-[104px] leading-[88px] font-extrabold tracking-[-0.04em] text-white @lg/current-conditions:text-[120px] @lg/current-conditions:leading-[104px]"]')
    temp_actual = caja_temp_actual.find_element(By.XPATH,'.//span[@data-testid="TemperatureValue"]').text
    temp_actual = int(temp_actual.replace("°","").strip())
    # convertimos de Farenheit a Celsius
    temp_actual = round((temp_actual - 32) * 5 / 9)

    temp_min  = temp_actual
    resultado = {}

    containers_dias = driver.find_elements(By.XPATH,'//div[@class="border-grey-500 @container/dailyItem overflow-hidden max-sm:border-b"]')
    
    for div_dia in containers_dias:
        # para la 1ra lectura se toma la minima 
        # temp_pivote arrastra la minima al siguiente dia
        temp_pivote = temp_min
        dia = div_dia.find_element(By.XPATH,'.//span[@class="text-sm leading-loose tracking-normal font-bold text-gray-900 w-14 shrink-0 whitespace-nowrap @lg/dailyItem:w-19"]')
        dia = dia.text

        porcentaje_lluvia = div_dia.find_element(By.XPATH, './/span[@data-testid="PercentageValue"]' )  
        porcentaje_lluvia = porcentaje_lluvia.text
        porc_lluvia_en_numeros = int(porcentaje_lluvia.replace("%","").strip())

        caja_temp_min = div_dia.find_element(By.XPATH, './/span[@class="text-base leading-loose tracking-tight font-medium text-gray-500 w-7 shrink-0 text-left whitespace-nowrap @max-lg/dailyItem:text-sm @lg/dailyItem:w-8 @lg/dailyItem:text-right"]' )
        temp_min = caja_temp_min.find_element(By.XPATH, './/span[@data-testid="TemperatureValue"]' )   
        temp_min = int(temp_min.text.replace("°","").strip())
        # convertimos de Farenheit a Celsius
        temp_min = round((temp_min - 32) * 5 / 9)

        caja_temp_max = div_dia.find_element(By.XPATH, './/span[@class="text-base leading-loose tracking-tight font-bold text-gray-900 w-7 shrink-0 text-right whitespace-nowrap @max-lg/dailyItem:text-sm @lg/dailyItem:w-8 @lg/dailyItem:text-left"]' )
        temp_max = caja_temp_max.find_element(By.XPATH, './/span[@data-testid="TemperatureValue"]' )                                    
        temp_max = int(temp_max.text.replace("°","").strip())
        # convertimos de Farenheit a Celsius
        temp_max = round((temp_max - 32) * 5 / 9)

        detalle = div_dia.find_element(By.XPATH,'.//span[@class="text-base leading-loose tracking-tight font-medium text-gray-900 hidden w-44 shrink-0 @2xl/dailyItem:line-clamp-2"]')
        
        detalle = detalle.text
        print(dia)
        resultado[dia] = {
            "Temp_min" : temp_pivote,
            "Temp_max" : temp_max,
            "porc_lluvia" : porcentaje_lluvia,
            "detalle" : detalle
        }

       # print(resultado)
        if temp_pivote < 11:
            color = "purpura"
        elif temp_pivote < 15:
            color = "magenta"
        elif temp_pivote < 18.5:
            color = "azul"
        elif temp_pivote < 22:
            color = "naranja"
        else:
            color = "rojo"

        
        #print(f"{detalle} -temp minima {temp_pivote} y maxima {temp_max}")  

    driver.quit()   # cierra el navegador

    return resultado

def muestra_pronostico():
    datos = scrap_pronostico()
    for dato in datos:
        with st.container(border=True):
            # preparamos los colores de fondo
            if datos[dato]["Temp_min"] < 11:
                bg_color = "#C902D1"
            elif datos[dato]["Temp_min"] < 15:
                bg_color = "#9991FF"
            elif datos[dato]["Temp_min"] < 18.5:
                bg_color = "#02D1A4"
            elif datos[dato]["Temp_min"] < 22:
                bg_color = "#FFFD8A"
            else:
                bg_color = "#FF8080"

            detalle = datos[dato]["detalle"].lower()
            # obtener icono
            if "parcial" in detalle or "mayormente" in detalle:
                icono ="⛅"  # Parcialmente nublado / Mayormente soleado
            elif "nublado" in detalle:
                icono = "☁️"  # Nublado
            elif "soleado" in detalle:
                icono = "☀️"  # Soleado
            elif "chubascos" in detalle:
                icono = "🌧️"  # Soleado
            elif "tormentas" in detalle:
                icono=  "🌩️"  # Soleado
            else:
                icono=  "🌡️"  # Por defecto
                          

        # Creamos una tarjeta con HTML y CSS.
            st.markdown(f"""
            <div style="
                background-color: {bg_color};
                padding: 3px;
                border-radius: 12px;
                text-align: center;
                color: #263747;
                width: 100%;
                line-height: 1.2;   
            ">
                <h4>📆{dato}</h4>
                <h5>Mínima: {datos[dato]["Temp_min"]}° - Maxima: {datos[dato]["Temp_max"]}°</h5>
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px;">
                <h2 style="margin: 0;">{icono}</h2>
                <h4 style="margin: 0;">{datos[dato]["detalle"]}</h4>
            </div>
                <h6> Porc. de lluvia: {datos[dato]["porc_lluvia"]} °</h6>"                
                
            </div>
            """, unsafe_allow_html=True)



        
        