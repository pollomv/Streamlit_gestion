import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options # para que no muestre cuando se abre el navegador
import json
import streamlit as st
from selenium.common.exceptions import NoSuchElementException # para los errores de selenium en except
import pandas as pd
from pathlib import Path

RUTA_DATOS = Path(__file__).resolve().parent / "data" / "precios_Cienfuegos_guardados.json" # crea ruta absoluta

def scrap_Cienfuegos():

    ########## para ocultar cuando se abre el navegador ########
    # 1. Configuras para que corra oculto en segundo plano
    options = Options()  # Creás una caja vacía donde vas a meter las configuraciones que vos querés cambiar.
    options.add_argument("--headless")  # no abras la ventana visible, trabajá en segundo plano".

    # 2. Inicializas el driver pasándole esas opciones
    driver = webdriver.Chrome(options=options) # le pasamos como argumento la configuracion del option

    ########## ************ ########

    # 1. Inicializamos el navegador y cargamos la página web objetivo
    # driver = webdriver.Chrome()
    driver.get("https://tienda.cienfuegosst.com.ar/cigarros/")
    time.sleep(3)  # Pausa inicial para asegurar que cargue el DOM base

    # 2. Capturamos la primera tanda de elementos visibles en la página
    elementos = driver.find_elements(By.XPATH, '//div[@class="item-info-container"]')

    prods = []  # Lista maestra donde acumularemos todos los productos únicos

    # Recorremos cada elemento encontrado ni bien abre el navegador, limpiamos sus espacios y lo guardamos
    for elemento in elementos:
        titulo = elemento.find_element(By.XPATH, './/a').get_attribute("title")
                ### ACLARACION DE BUSQUEDA:
                # ./a (con una barra): Busca únicamente a los hijos directos. O sea, si el link está ahí nomás pegado, lo encuentra.
                #  Pero si está metido un poco más adentro dentro de otros renglones o etiquetas, no lo ve.
                # .//a (con dos barras): Busca el link en cualquier nivel de profundidad hacia adentro de esa caja, sin importar si 
                # está escondido dentro de un <div>, un <span> o más etiquetas
        completo =  elemento.text.strip()
        texto = f"{titulo}\n{completo}"
        prods.append(texto)

    # Guardamos la cantidad inicial para usarla como índice de corte (slicing)
    lote_viejo = len(prods)

    # 3. Bucle principal para manejar la paginación infinita
    while True:
        # Bajamos el scroll hasta el fondo para forzar el comportamiento de la página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #En JavaScript, el punto y coma se usa al final
                                                                # de cada instrucción para marcar dónde termina una línea de código
        time.sleep(2)

        # Localizamos y hacemos clic en el botón "Cargar más" usando JavaScript
        boton = driver.find_element(By.XPATH, '//a[contains(@class, "js-load-more-btn")]')
        driver.execute_script("arguments[0].click();", boton)
        
        time.sleep(2)  # Breve pausa para que el servidor inyecte los nuevos productos

        nuevo_lote = [] # aca cargaremos la tanda de los nuevos arts que arega la pagina

        # Volvemos a escanear todos los elementos actuales del DOM post-clic
        todos_actuales = driver.find_elements(By.XPATH, '//div[@class="item-info-container"]')
        
        # Usamos slicing [lote_viejo:] para aislar únicamente lo que se acaba de cargar
        for actuales in todos_actuales[lote_viejo:]: # [lote_viejo:] desde la cantidad anterior en adelante
            titulo = actuales.find_element(By.XPATH, './/a').get_attribute("title")
            completo =  actuales.text.strip()
            

            ############## en busqueda de la etiqeuta SIN STOCK ######
            try:
                stock_label = actuales.find_element(
                    By.XPATH,
                    "./ancestor::*[contains(@class, 'item-container')][1]//*[@data-store='product-item-label-stock']"
                )          # ./  con el punto arranca desde ahi donde estamos parados / ancestor:: va hacia arriba, padres abuelos etc
                        #  contains ->en todos los niveles de arriba encontra algo que contemga (diferencia con que sea exacto)
                        # [1] de lo que encuentres selecciona el mas proximo 
                        # //* desde ahi donde estamos parados busca cualquier etiqueta (*)
                texto_stock = stock_label.text.strip()
                
                estado_stock = texto_stock if texto_stock else ""
            except NoSuchElementException:      # Es una clase de error específica que Selenium (no Python en general) usa para avisarte: "busqué el elemento que me pediste con find_element, y no encontré
                estado_stock = ""
            
            #####################################################
            
            texto = f"{titulo}\n{completo}\n{estado_stock}"
            nuevo_lote.append(texto)

        # Bandera (interruptor) para detectar si un producto ya existe en la lista maestra
        repetido = False

        # Recorremos el lote recién llegado para validarlo
        for nuevo in nuevo_lote:
            if nuevo in prods:
                repetido = True  # Prendemos la bandera si encontramos duplicado
                break           # Rompemos el bucle interno
            else:
                prods.append(nuevo)  # Si es fresco, lo sumamos a la lista maestra
                # print("Nuevo producto:", nuevo)

        # Si la bandera se encendió, significa que la página dio la vuelta: frenamos todo
        if repetido:
            break

        # Actualizamos el tamaño del lote viejo para que en la próxima vuelta corte desde acá
        lote_viejo = len(prods)

        # 4. Resultado final al salir del bucle de paginación
        # print("Terminado. Total de productos únicos:", len(prods))

    driver.quit()
    productos = {} # aca van a ir todos lo podctos con sus precios

    for prod in prods:
        
        todo_junto = prod.splitlines() # corta en cada salto de linea
       
        
        nombre = todo_junto[0].strip()
        nombre = nombre.replace("–", "-") # reemplazo ese guion raro que viene del title

        if len(todo_junto) > 2:
            precio = todo_junto[2].split("$")
            precio = precio[1] if len(precio)>1 else precio[0]
            precio = precio.strip()
            precio = int(precio.replace('.', ''))
            
        else:
            precio = 0        

        
        if "SIN STOCK" in todo_junto:
            sin_stock = "SIN STOCK"
        else:
            sin_stock = ""
        print(f"{nombre}  -- {sin_stock}")  
        # voy agregando al diccionario de productos los articulos
        #productos[nombre] = precio   # como llave le colcoo el nombreArticulo y le asigno el valor precio 
        productos[nombre] = {"precio" : precio, "sin_stock" : sin_stock }  # como llave le colcoo el nombreArticulo y le asigno el valor precio 
        
        

    misArticulos = [
        "Dominican Estates Pyramide - Unidad",
        "Dominican Estates Robusto - Unidad",
        "Línea Amarilla Torpedo - Unidad",
        "Línea Azul Petit Corona - Unidad",
        "Línea Azul Robusto - Unidad",
        "Línea Azul Toro - Unidad",
        "Línea Bordo Petit Corona - Unidad",
        "Macanudo Inspirado Red Robusto - Unidad",
        "Oliva Serie V Liga Especial Doble Robusto - Unidad",
        "Panter Red - Caja x 10",
        "Panter Small - 10 Cajas x 10",
        "Phillies Blunt Clásico - Caja x 5",
        "Phillies Titan Clásicos - Caja x 5",
        "Príncipes Corona Blond - Unidad",
        "Príncipes Corona Brown - Unidad",
        "Príncipes Corona Caribbean - Unidad",
        "Príncipes Corona Original - Unidad",
        "Príncipes Miniature Blond - Caja x 10",
        "Príncipes Miniature Brown - Caja x 10",
        "Príncipes Miniature Original - Caja x 10",
        "Romeo y Julieta Short Churchills - Unidad",
        "Villiger Premium N° 1 Sumatra - Unidad",
        "Villiger Premium N° 3 Sumatra - Unidad",
        "Villiger Premium N° 7 Sumatra - Unidad",
        "Casa de García Connecticut Toro - Unidad"
    ]

    articulos_filtrados = {} # aca van a ir los articulos que se scrapea en la web y ademas YO los tengo

    for article in misArticulos:
        if article in productos:
            articulos_filtrados[article] = productos[article]

    ############ primero traemos el json con los datos viejos
    
    # Preguntamos si el archivo existe en la carpeta
    if RUTA_DATOS.exists(): # Devuelve un True (si el archivo está en la carpeta) o un False (si no existe).
    # Si existe, lo leemos como venías haciendo
        with open(RUTA_DATOS, "r",encoding="utf-8") as archivo:
            datos_viejos = json.load(archivo)
    else:
        # Si NO existe (es la primera vez), arrancamos con un diccionario vacío
        datos_viejos = {}

    ################ si no existe el archivo json guardado lo crea #########
    if not datos_viejos:
        RUTA_DATOS.parent.mkdir(parents=True,exist_ok=True) # exist_ok=True: Le dice a Python: "Si la carpeta data ya existe en el disco, no me tires un error, simplemente no hagas nada y seguí de largo
                                                            # parents=true si no hay las carpetas padres crealas

        with open(RUTA_DATOS, "w",encoding="utf-8") as archivo:
            json.dump(articulos_filtrados, archivo, indent=2, ensure_ascii=False)

        st.success("Primera vez: se guardó el archivo inicial")
    #####################################################

    contador = 0
    cambios = []

    for dato_old in datos_viejos:
        if dato_old in articulos_filtrados: # si el articulo del json guardado esta en los articulos que scrapeo recien
            precio_nuevo = articulos_filtrados[dato_old]["precio"]
            precio_viejo = datos_viejos[dato_old]["precio"]
            stock =   articulos_filtrados[dato_old]["sin_stock"]
            
            if precio_nuevo != precio_viejo:
                
                # cambios.append(f"{dato_old} de $ {precio_viejo} cambio a $ {precio_nuevo} {stock}")
                cambios.append(
                    {
                        "Articulo" : dato_old,
                        "Precio anterior" : precio_viejo,
                        "Precio Actual" : precio_nuevo,
                        "Observaciones" : stock
                    }
                )
                
                contador +=1

    # Prende el interruptor: avisa que el scrapeo ya terminó.
    # app.py lo consulta para no repetir el scrapeo en las próximas ejecuciones.
    st.session_state["Cienfuego_scrapeado"] = True          # escribe "scrapeado"

    if contador > 0:
        # creamos una sesion avisando que hubo modificaciones y le pasamos los arts filtrados q se van a usar en el json
        st.session_state["hubo_modificaciones"] = articulos_filtrados

        st.error(f"⚠️ Hubieron {contador} modificaciones de precios")
        return cambios
    else:
        st.info("No hubo modificaciones de precios")
        return[]

def guarda_datos_Cienfuegos():
    if "hubo_modificaciones" in st.session_state:  # si hubieron modificaciones 
        if st.button("🗳 Guarda datos"):
            aviso = st.empty() # creo un espacio vacio
            aviso.write("Guardando datos...")
            ########### guardamos los datos actuales en el archivo precios_guardados.json
            with open(RUTA_DATOS, "w",encoding="utf-8") as archivo: # open(...):orden para abrir un archivo. Si el archivo no existe lo crea automáticamente. Si ya existe, lo pisa y lo reemplaza por uno nuevo.
                json.dump( st.session_state["hubo_modificaciones"], archivo,indent=2,ensure_ascii=False)
                

            aviso.empty() 
            st.success("✅ nuevos datos guardados")   
            st.session_state.pop("hubo_modificaciones", None)
            st.toast("✅ Datos guardados con exito")
