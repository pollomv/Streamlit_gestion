import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options # para que no muestre cuando se abre el navegador
import json
import streamlit as st
from pathlib import Path

RUTA_DATOS = Path(__file__).resolve().parent / "data" / "datos_guardados_Churchill.json" # crea ruta absoluta

def scrapChurchill():
    
    #mostrar_info("\nProcesando la web de Churchill...\n","negro")
    
    ########## para ocultar cuando se abre el navegador ########
    # 1. Configuras para que corra oculto en segundo plano
    options = Options()  # Creás una caja vacía donde vas a meter las configuraciones que vos querés cambiar.
    options.add_argument("--headless")  # no abras la ventana visible, trabajá en segundo plano".

    # 2. Inicializas el driver pasándole esas opciones
    driver = webdriver.Chrome(options=options) # le pasamos como argumento la configuracion del option

    ########## ************ ########

    # 1. Inicializamos el navegador y cargamos la página web objetivo
    # driver = webdriver.Chrome()
    driver.get("https://churchill.com.ar/habanos-puros-y-cigarros/")
    time.sleep(3)  # Pausa inicial para asegurar que cargue el DOM base

    # 2. Capturamos la primera tanda de elementos visibles en la página
    print("\nProcesando...\n")   

    productos = {}
    tarjetas = 0
    while True:
        # Bajamos el scroll hasta el fondo para forzar el comportamiento de la página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #En JavaScript, el punto y coma se usa al final
                                                                # de cada instrucción para marcar dónde termina una línea de código
        time.sleep(2)
        
        botones = driver.find_elements(By.XPATH, '//a[contains(text(), "Mostrar más productos")]')
        
        driver.execute_script("arguments[0].click();", botones[0])
        time.sleep(2)  # Breve pausa para que el servidor inyecte los nuevos productos
        lote_nuevo = driver.find_elements(By.XPATH, '//div[@class="product-item-information product-item-information-inner"]')
        
        if lote_nuevo == tarjetas:

            elementos = driver.find_elements(By.XPATH, '//div[@class="product-item-information product-item-information-inner"]')
            for elemento in elementos:
        
                nombre = elemento.find_element(By.XPATH,'.//a').get_attribute("title")
                nombre = nombre.strip()
                # .// → buscá dentro de esta tarjeta, a cualquier profundidad.
                # [ ... ] → pero solo la que cumpla esta condición.
                # @class → el atributo class de esa etiqueta.
                # get_attribute("textContent") le pide al navegador el texto que hay dentro de la etiqueta, sin preguntar si se ve o no. Es lo que está en el código, tal cual.
                precio = elemento.find_element(By.XPATH,'.//span[@class="js-price-display product-item-price"]').get_attribute("textContent")
                precio = precio.replace(".","")
                precio = precio.replace("$","")
                precio = precio.split(",")
                precio = precio[0]
                precio = precio.strip()
                precio = int(precio)
                ### ACLARACION DE BUSQUEDA:
                # ./a (con una barra): Busca únicamente a los hijos directos. O sea, si el link está ahí nomás pegado, lo encuentra.
                #  Pero si está metido un poco más adentro dentro de otros renglones o etiquetas, no lo ve.
                # .//a (con dos barras): Busca el link en cualquier nivel de profundidad hacia adentro de esa caja, sin importar si 
                # está escondido dentro de un <div>, un <span> o más etiquetas

                
                productos[nombre] = precio            
            break
        
        tarjetas = lote_nuevo

    driver.quit()

    misArticulos = [
        "VILLIGER - PREMIUM N° 7 SUMATRA",
        "FLOR DE COPAN - TITAN",
        "DOMINICAN ESTATES SELECCIÓN - ROBUSTO",
        "PRINCIPES - CORONA CARIBBEAN",
        "DOMINICAN ESTATES SELECTION - PYRAMIDE",
        "ROMEO Y JULIETA - SHORT CHURCHILLS",
        "ROSALONES - RESERVA 546",
        "ROSALONES - AUTENTICOS 448",
        "OLIVA SERIE V LIGA ESPECIAL - DOBLE ROBUSTO",
        "CASA TURRENT - SAN ANDRES ROBUSTO",
        "CASA DE GARCIA - TORO CONNECTICUT",
        "MY FATHER LE BIJOU GRAN ROBUSTO",
        "TE AMO SAN ANDRES - ROBUSTO",
        "CASA TURRENT - CUBA ROBUSTO",
        "DIAS DE GLORIA ROBUSTO"
    ]

    prtos_recien_leidos = {}
    for miarticulo in misArticulos:
        if miarticulo in productos:
            prtos_recien_leidos[miarticulo] = productos[miarticulo]    

    # __file__: Es una variable secreta que Python crea automáticamente. Guarda el nombre del archivo donde estás parado en este preciso momento (por ejemplo, persistencia.py).
    # Path(__file__): Convierte ese texto en un objeto de tipo Path (la herramienta de Python para manipular caminos en el sistema de archivos).
    # .resolve(): Es el comando que averigua en qué carpeta del disco duro está ese __file__ y te devuelve la ruta absoluta completa desde el disco C:.
    # .parent: Significa "ir a la carpeta contenedora" (subir un escalón hacia arriba en la estructura de carpetas).
    # .parent.parent: Al ponerlo dos veces, sube dos niveles hacia arriba en tu árbol de carpetas (sale del archivo actual, sale de la subcarpeta donde está, y llega a la raíz del proyecto)

    

    if RUTA_DATOS.exists():
        with open(RUTA_DATOS,"r",encoding="utf-8") as archivo:
                datos_viejos = json.load(archivo) # Cuando leés el archivo con json.load(archivo), Python agarra el JSON y lo transforma a un objeto nativo de Python.
    else:
        # Si NO existe (es la primera vez), arrancamos con un diccionario vacío
        datos_viejos = {}

    ################ si no existe el archivo json guardado lo crea #########
    if not datos_viejos:
        RUTA_DATOS.parent.mkdir(parents=True,exist_ok=True) # exist_ok=True: Le dice a Python: "Si la carpeta data ya existe en el disco, no me tires un error, simplemente no hagas nada y seguí de largo
                                                    # parents=true si no hay las carpetas padres crealas
        with open(RUTA_DATOS,"w",encoding="utf-8") as archivo:
            json.dump(prtos_recien_leidos, archivo, indent=2, ensure_ascii=False) # indent evita el archivo en unsa sola linea y le agraga 2 indentaciones y saltos de lineeas
                                                                            # Con ensure_ascii=False, le decís que escriba las letras, tildes y eñes en castellano tal cual son
                # json.dump() es la función de Python que agarra los datos de la memoria y los vuelca en el disco rígido.
                #  Para funcionar, necesita responder dos preguntas en orden:
                # ¿Qué dato querés guardar? (suscripciones)
                # ¿En qué archivo físico lo querés meter? (archivo)
    # *************************************************************************************

    contador = 0
    cambios = []
    for old_data in datos_viejos:
        if old_data in prtos_recien_leidos:   # si el articulo del json guardado esta en los articulos que scrapeo recien
            precio_nuevo = prtos_recien_leidos[old_data] 
            precio_viejo = datos_viejos[old_data]

            if precio_nuevo != precio_viejo:
                cambios.append({                # ahgrego un dict a la liusta en cada vuelta del for
                                "Producto": old_data,
                                "Precio viejo": precio_viejo,
                                "Precio nuevo": precio_nuevo
                            })                
                contador +=1

    # Prende el interruptor: avisa que el scrapeo ya terminó.
    # app.py lo consulta para no repetir el scrapeo en las próximas ejecuciones.
    st.session_state["scrapeado"] = True          # escribe "scrapeado"
    
    if contador > 0:
        st.session_state["hubo_modificaciones"] = prtos_recien_leidos
        return cambios  # si hubo cambios retormo la lista con los cambios adento
        
    else:        
        st.info("No hubieron modificaciones de precios")
        return []


def guarda_datos_churchill():
    if "hubo_modificaciones" in st.session_state:  # si hubieron modificaciones 
        if st.button("Guarda datos"):
            RUTA_DATOS.parent.mkdir(parents=True,exist_ok=True) # exist_ok=True: Le dice a Python: "Si la carpeta data ya existe en el disco, no me tires un error, simplemente no hagas nada y seguí de largo
                                                                # parents=true si no hay las carpetas padres crealas
            
            ########### guardamos los datos actuales en el archivo precios_guardados.json
            with open(RUTA_DATOS,"w",encoding="utf-8") as archivo:
                json.dump(st.session_state["hubo_modificaciones"],archivo,indent=2,ensure_ascii=False) # indent evita el archivo en unsa sola linea y le agraga 2 indentaciones y saltos de lineeas
                                    # Con ensure_ascii=False, le decís que escriba las letras, tildes y eñes en castellano tal cual son
                    # json.dump() es la función de Python que agarra los datos de la memoria y los vuelca en el disco rígido.
                    #  Para funcionar, necesita responder dos preguntas en orden:
                    # ¿Qué dato querés guardar? (suscripciones)
                    # ¿En qué archivo físico lo querés meter? (archivo)
                #mostrar_info("nuevos datos guardados","verde")
                st.success("nuevos datos guardados")
                st.toast("✅ Datos guardados con exito")
                print("nuevos datos guardados")
                st.session_state.pop("hubo_modificaciones", None)
            
