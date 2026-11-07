import pdfplumber
import streamlit as st

def read_pdf_Todopuros():

    from pathlib import Path

    RUTA_CIGARROS = Path(__file__).resolve().parent / "data" / "L5 CIGARROS TODOPUROS.pdf"
    RUTA_HABANOS = Path(__file__).resolve().parent / "data" / "L5 HABANOS TODOPUROS.pdf"

    archivos_pdf = [
        RUTA_CIGARROS,
        RUTA_HABANOS
    #r"C:\MisProyectos\habana_vieja\L5 CIGARROS TODOPUROS.pdf",
    #r"C:\MisProyectos\habana_vieja\L5 HABANOS TODOPUROS.pdf" 
    ]
    # pdf_path = r"C:\MisProyectos\leer_pdf\L5 CIGARROS TODOPUROS.pdf"

    productos = {}

    for pdf_path in archivos_pdf:
    

        with pdfplumber.open(pdf_path) as pdf:
            # page = pdf.pages[0]         # aca usaba sola la 1er pagina del pdf
            for page in pdf.pages:         # 
                text = page.extract_text()  # # Extraemos todo el texto plano que contiene esa página para poder manipularlo como texto
                
                # 1. Cortamos el texto gigante en una lista de líneas
                lineas = text.split("\n")        
                
                line_data = []
                col1=""
                articulo=""
                col3= ""
                # 2. Recorremos cada línea una por una con un bucle
                for index, line in enumerate(lineas):  # con emnumerate crea un indice 0,1,2,3,4....
                # Imprimimos las primeras 30 líneas para inspeccionar cómo arranca el PDF
                    line = line.strip()
                    
                    if "$" in line:
                        #print(f"Línea {index}: {line}")
                        line_data = line.split("$")
                        if len(line_data)<3:
                            continue
                        
                        parte1 = line_data[0].strip().upper()                                         
                        parte2 = line_data[1].strip().replace(" ","")  
                        
                        parte3 = line_data[2].strip().replace(" ","")
                        if parte1.startswith("X ") or parte1.startswith("C "):   # parte1.startswith si comienza con
                            
                            col1 = parte1[0]                 # toma si es X o C
                            if parte1[2:].endswith("*"):      # parte1.endwith -> si termina con
                                articulo = parte1[2:-2].strip()                                                  
                                col3 = parte1[-1]     # toma el ultimo caracter -> *
                            else:
                                articulo = parte1[2:]
                                col3 = ""
                        else:
                            col1 = ""
                            if parte1.endswith("*"):
                                articulo = parte1[0:-2].strip() # desde la 1ra letra hasta dos antes que termine
                                col3 = parte1[-1]
                            else:
                                articulo = parte1
                                col3 = ""
                        prec_vta = parte2
                        costo = parte3
                    else:
                        continue

                    productos[articulo] = {"estado": col1, "cambio": col3, "precio": prec_vta, "costo": costo}    
                
    mis_articulos = [
        "AJ FERNANDEZ DIAS DE GLORIA ROBUSTO (51/2*52)",
        "AX ROBUSTO HABANO",
        "AX PETIT ROBUSTO CONNECTICUT",
        "CASA TURRENT 54 X 5.5 CUBA ROBUSTO X12",
        "CASA TURRENT 54 X 5.5 MIAMI ROBUSTO X12",
        "CASA TURRENT 54 X 5.5 SAN ANDRES ROBUSTO X12",
        "F. DE MIRANDA LINEA AMARILLA TORPEDO X25",
        "F. DE MIRANDA LINEA AZUL CORONA X25",
        "F. DE MIRANDA LINEA AZUL PETIT CORONA X25",
        "F. DE MIRANDA LINEA AZUL ROBUSTO X25",
        "F. DE MIRANDA LINEA AZUL TORO X25",
        "F. DE MIRANDA LINEA BORDO PETIT CORONA X25",
        "JDN ROSALONES RESERVA 546 (5 1/2X46) X20",
        "JDN ROSALONES AUTENTICOS 448 4/34X48",
        "LA AURORA 1987 ROBUSTO CONNEC/ 5X50 20U",
        "MACANUDO INSPIRADO RED ROBUSTO X20 (5X50)",
        "MACANUDO INSPIRADO WHITE ROBUSTO X20 (5X50)",
        "MY FATHER LE BIJOU 1922 GRAND ROBUSTO X23U",
        "OLIVA SERIE V LIGA ESPECIAL DOBLE ROBUSTO X24",
        "PANTER SMALL X10",
        "PANTER RED X10",
        "PHILLIES BLUNT X5",
        "PHILLIES TITAN CHOCOLATE X5",
        "PHILLIES TITAN COGNAC X5",
        "PHILLIES TITAN ORIGINAL X5",
        "PRINCIPES CORONA CARIBBEAN X5 (RON)",
        "PRINCIPES CORONA CHOCOLATE X5 BROWN",
        "PRINCIPES CORONA NATURAL X5",
        "PRINCIPES CORONA VAINILLA X5 BLOND",
        "PRINCIPES MINIATURE BLOND (VAINILLA) X10",
        "PRINCIPES MINIATURE BROWN (CHOCO) X10",
        "PRINCIPES MINIATURE ORIGINAL X10",
        "SOL DE CUBA ROBUSTO X10 CAJA",
        "TE AMO SAN ANDRES ROBUSTO 54X5 CAJA 20U",
        "VILLIGER PREMIUM N1 SUMATRA X5",
        "VILLIGER PREMIUM N3 SUMATRA X5",
        "VILLIGER PREMIUM N7 SUMATRA X5",
        "CASA DE GARCIA TORO 50X5 1/2 MAZO X10",
        "DOMINICAN ESTATES SELECTION PYRAMIDE X25 008",
        "DOMINICAN ESTATES SELECTION ROBUSTO X25 008CU",
        "PARTAGAS SERIE D N 4 X25",
        "ROMEO Y JULIETA PURITOS X25",
        "ROMEO Y JULIETA SHORT CHURCHILLS X10"
    ]
    resultado = []
    

    for mi_articulo in mis_articulos:
        
        if mi_articulo in productos:

            if productos[mi_articulo]["estado"] == "X" and productos[mi_articulo]["cambio"] == "*":
                observaciones = "Aumento $ \n SIN STOCK"
            elif productos[mi_articulo]["estado"] == "X":
                observaciones = "SIN STOCK"
            elif productos[mi_articulo]["cambio"] == "*":
                observaciones = "Aumento $"
            else:
                observaciones = ""

            resultado.append(
                {"Articulo" : mi_articulo,
                 "Precio" : productos[mi_articulo]['precio'],
                 "Costo" : productos[mi_articulo]['costo'],
                "Observaciones" : observaciones
                }
            )
            
    return resultado

def colorear(fila):

    # Creamos una lista vacía de estilos.
    # len(fila) cuenta cuántas columnas tiene la fila.
    # Al principio, ninguna celda tiene un formato especial.
    colores = [""] * len(fila)

    # Guardamos el contenido de Observaciones en una variable.
    observaciones = str(fila["Observaciones"])

    # PRIMERA CONDICIÓN:
    # Si Observaciones contiene "SIN STOCK",
    # aplicamos un fondo amarillo suave a toda la fila.
    # También fijamos las letras en un color oscuro para que se lean bien.
    if "SIN STOCK" in observaciones:
        colores = [
            "background-color: #302b20; color: #e8dfc5;"
        ] * len(fila)

    # SEGUNDA CONDICIÓN:
    # Si Observaciones contiene "Aumento $",
    # buscamos en qué posición está la columna Precio.
    if "Aumento $" in observaciones:

        posicion = fila.index.get_loc("Precio")

        # En esa posición ponemos las letras rojas y en negrita.
        # Si también hay SIN STOCK, conserva el fondo amarillo.
        colores[posicion] += " color: #c62828; font-weight: bold;"

    # Devolvemos los estilos para que Pandas los aplique a la fila.
    return colores
