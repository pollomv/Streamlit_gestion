import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options # para que no muestre cuando se abre el navegador
from selenium.common.exceptions import NoSuchElementException
import streamlit as st

def busca_partidos():

    ########## para ocultar cuando se abre el navegador ########
    # 1. Configuras para que corra oculto en segundo plano
    options = Options()  # Creás una caja vacía donde vas a meter las configuraciones que vos querés cambiar.
    options.add_argument("--headless")  # no abras la ventana visible, trabajá en segundo plano".

    # 2. Inicializas el driver pasándole esas opciones
    driver = webdriver.Chrome(options=options) # le pasamos como argumento la configuracion del option

    ########## ************ ########

    # 1. Inicializamos el navegador y cargamos la página web objetivo
    # driver = webdriver.Chrome()
    driver.get("https://www.ole.com.ar/agenda-deportiva")
    time.sleep(2)  # Pausa inicial para asegurar que cargue el DOM base

    # busco con --> contains(dónde buscar, qué buscar)
    fechas = driver.find_elements(By.XPATH, '//*[contains(@class, "sc-3ec32152-1") or contains(@class, "sc-3ec32152-2")]')

    partidos ={}

    for fecha in fechas:
        
        # ./ (El punto y la barra) ->  "empezá a buscar desde la posición actual". poner el punto al ppio para que arranque estrictamente desde fecha y no desde la raíz del sitio web.
        # mirá hacia arriba en el árbol del código HTML y buscá únicamente entre los elementos padres, abuelos
        # div que sea un div
        # [1] (El índice de cercanía):
        # El [1] se refiere al primer div inmediatamente superior que envuelve a fecha
        div_container_fecha = fecha.find_element(By.XPATH,'./ancestor::div[1]')
        
        try:
            
            # identificamos el h2 cuyo text() = LIGA PROFESIONAL
            tipo_partido = div_container_fecha.find_element(By.XPATH,".//h2[text()='Liga Profesional']")

            # subimos hasta encontrar el div con una determinada class
            div_ancestor_tipo = tipo_partido.find_element(By.XPATH,'./ancestor::div[@class="tournament-type"]')

            # buscamos en el mimso nivel/hermano (following-sibling) un dic con una class "events"
            div_hermano_tipo_partido = div_ancestor_tipo.find_element(By.XPATH,'./following-sibling::div[@class="events"]')

            # desde ese div hernano con class events buscamos hacia abajo un div que contiene todos los partidos que esten dentro de la fecha
            divs_partidos = div_hermano_tipo_partido.find_elements(By.XPATH,'.//div[@class="event-info div1"]')
            
            fecha = fecha.text
            if "Agenda Deportiva del " in fecha:
                
                fecha = fecha.replace("Agenda Deportiva del","").strip()
                

            partidos[fecha] = []
            for div_partido in divs_partidos:
                
                div_local = div_partido.find_element(By.XPATH,'.//div[@class="event-info_team_group home"]')
                team_local = div_local.find_element(By.XPATH,'.//h3[contains(@class, "event-name ")]').text
                
                try: # si encuentra el div con class "event-time" lo toma
                    horario = div_partido.find_element(By.XPATH,'.//div[@class="event-time"]').text
                    #score = div_partido.find_element(By.XPATH,'.//p[@class="futbol-mam-score"]').text
                except: # si no encuentra coloca "finalizado"

                    try:
                        tiempo = div_partido.find_element(By.XPATH,'.//p[@class="futbol-mam-period-game"]').text
                    except:
                        tiempo = ""

                    score = div_partido.find_element(By.XPATH,'.//p[@class="futbol-mam-score"]').text
                    
                    
                    horario = f"{tiempo}   ({score})"

                div_visitante = div_partido.find_element(By.XPATH,'.//div[@class="event-info_team_group visitor"]')
                team_visitante = div_visitante.find_element(By.XPATH,'.//h3[contains(@class, "event-name ")]').text
                #print(f"\n{fecha.text}-{horario} \n{team_local} vs {team_visitante}")
                

                # partidos[fecha][f"{team_local} vs {team_visitante}"] = horario
                partidos[fecha].append({
                    "match" : f"{team_local} vs {team_visitante}",
                    "horario" : horario
                })
            
                
        except NoSuchElementException:
            continue

    driver.quit()   # cierra el navegador
    
    return partidos 

def muestra_partidos():
    partidos = busca_partidos()  
    if not partidos:
        st.error("No hay partidos esta semana")
    else:
        
        for por_dia in partidos:
            with st.container(border=True):
                st.markdown(f"#### 📅 {por_dia}")

                st.divider()
                
                for partido in partidos[por_dia]:
                    
                    print(f"dia {por_dia}")
                    print(f"match {partido["match"]}")
                    print(f"horario {partido["horario"]}")
                    col_equipos, col_estado = st.columns([3, 1])
                    
                    with col_equipos:
                        
                        if "Independiente" in partido["match"] and "ivadavia" not in partido["match"]:
                            st.warning(f"{partido["match"]}")
                        else:
                            st.write(f"⚽ ***{partido["match"]}***")
                        
                    with col_estado:
                        # Muestra la hora si no se jugó, o el resultado si ya terminó
                        st.write(partido["horario"])
