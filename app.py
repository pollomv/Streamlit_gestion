import streamlit as st
from verificaChurchill import scrapChurchill, guarda_datos_churchill
import pandas as pd

st.set_page_config(page_title="App gestion",page_icon="⚜️",layout="wide")
# layout="wide": la app usa todo el ancho de la pantalla (si no, queda angosta y centrada).

def main():
    st.header("Gestion de tareas",divider="rainbow") 
    # Al cargar por primera vez nadie eligió nada, entonces "eleccion" no existe
    # y daría KeyError. La creamos con "inicio".
    # Si ya se eligió algo (se tocó un botón), no se pisa.   
    if "eleccion" not in st.session_state:
        st.session_state["eleccion"] = "inicio"

    with st.sidebar:
        st.title("Menu")        

        if st.button("🗞️ Ultimas noticias", width="stretch"):
            st.session_state["eleccion"] = "ultimas_noticias"

        with st.expander("🗂️ Varios"):
            if st.button(" ☔ pronostico del tiempo", width="stretch"):
                st.session_state["eleccion"] = "pronostico_tiempo"

            if st.button("⚽ Partidos de futol", width="stretch"):
                st.session_state["eleccion"] = "partidos_futbol"

            if st.button("📠 Presupuesto gastos", width="stretch"):
                st.session_state["eleccion"] = "ppto_gto"  

        with st.expander("📈 Cotizaciones"):
            if st.button("🪙 Acciones-cedears", width="stretch"):
                st.session_state["eleccion"] = "cedears_acciones"

            if st.button("📊 Fondos de inversiones", width="stretch"):
                st.session_state["eleccion"] = "fdos_inv"
            

            if st.button("🧮 Indice Precios al consumidor", width="stretch"):
                st.session_state["eleccion"] = "indice_ipc"          

        with st.expander("📉 Modificaciones de precio"):
            if st.button("🚬 Churchill cicars", width="stretch"):
                st.session_state["eleccion"] = "Churchill"

                # Borra la nota "scrapeado" (apaga el interruptor).                
                st.session_state.pop("scrapeado", None) # Así, la próxima vez que se llegue al if de abajo, se va a scrapear de nuevo.

            if st.button("🚬 Cien fuegos cicars", width="stretch"):
                st.session_state["eleccion"] = "CienFuegos"

                # Borra la nota "scrapeado" (apaga el interruptor).                
                st.session_state.pop("Cienfuego_scrapeado", None) # Así, la próxima vez que se llegue al if de abajo, se va a scrapear de nuevo.

            if st.button("📝 Lee PDF Todopuros", width="stretch"):
                st.session_state["eleccion"] = "lee_pdf"

        st.divider()    # línea divisoria

        

    if st.session_state["eleccion"] == "Churchill":
        st.subheader("Verificando variacion de precios en Churchill cigar")
        # Muestra el cartelito girando mientras corre lo de adentro

         # "scrapeado" es un interruptor:
        # - Si NO existe (apagado): hay que scrapear.
        # - Si existe (prendido): ya se scrapeó, NO se vuelve a scrapear.
        # Esto evita que al apretar "Guarda datos" se repita el scrapeo,
        # porque Streamlit vuelve a correr todo el archivo en cada click.
        if "scrapeado" not in st.session_state:
            with st.spinner("Scrapeando la web Churchill..."):            
                cambios = scrapChurchill()
                if cambios:
                    st.dataframe(cambios)

        guarda_datos_churchill()
                    
    elif st.session_state["eleccion"] == "CienFuegos":
        from verificaCienfuegos import scrap_Cienfuegos, guarda_datos_Cienfuegos
        st.subheader("Variacion de precios en Cienfuegos cigar")

        if "Cienfuego_scrapeado" not in st.session_state:
            
            with st.spinner("Scrapeando la web Cienfuego..."):            
                cambios = scrap_Cienfuegos() # de la Fn  scrap_Cienfuegos() obtenemos con return los cambios
                if cambios:
                    st.dataframe(cambios)

        guarda_datos_Cienfuegos()

        
    elif st.session_state["eleccion"] == "lee_pdf":
        from lee_pdf_Todopuros import read_pdf_Todopuros, colorear

        st.subheader("📋 Lista de precios TODOPUROS")
        with st.spinner("Extrayendo datos del PDF..."): 
            # Recibimos los datos del scraping
            datos = read_pdf_Todopuros()

            # Convertimos la lista en un DataFrame
            df = pd.DataFrame(datos)

            # Aplicamos la función al DataFrame
            st.dataframe(df.style.apply(colorear, axis=1))
            
            st.toast("Articulo guardado",icon="✅")

    elif st.session_state["eleccion"] == "pronostico_tiempo":
        from consulta_pronostico import muestra_pronostico
        st.subheader(" ⛈️ Pronostico del tiempo")
        with st.spinner("Consultando pronostico del tiempo..."): 
            muestra_pronostico()

    elif st.session_state["eleccion"] == "partidos_futbol":
        from consulta_partidos import muestra_partidos

        st.subheader("⚽ Fecha Liga profesional")
        with st.spinner("Consultando fixture de la liga profesional..."): 
                muestra_partidos()

    elif st.session_state["eleccion"] == "ultimas_noticias":
            from consulta_noticias import muestra_noticias
    
            st.subheader("📻 Ultimas noticias")
            with st.spinner("Consultando ultimas noticias..."): 
                    muestra_noticias()

    elif st.session_state["eleccion"] == "cedears_acciones":
        #from consulta_cedear_acciones import muestra_cedear_acciones
        from consulta_api_cedears_acciones import muestra_cedear_acciones
        
        st.subheader("🪙 Cotizacion Cedears y Acciones")
        with st.spinner("Obteniendo cotizaciones de Cedears y acciones..."): 
            muestra_cedear_acciones()

    elif st.session_state["eleccion"] == "indice_ipc":
            from consulta_ipc import muestra_ipc
            
            st.subheader("🛒 Indice Precios al Consumidor")
            with st.spinner("Obteniendo Indice IPC..."): 
                muestra_ipc()

    elif st.session_state["eleccion"] == "fdos_inv":
        from consulta_fondos_inv import mustra_fondos_inv
        
        st.subheader("📊 Fondos comunes de inversion")
        with st.spinner("Obteniendo datos de los fondos..."): 
            mustra_fondos_inv()

    elif st.session_state["eleccion"] == "ppto_gto":
            from extrae_datos_excel import muestra_datos_excel
            
            st.subheader("📊 Situacion presupuesto Gastos")
            with st.spinner("Obteniendo datos del excel..."): 
                muestra_datos_excel()
    
        
    



if __name__ == "__main__":
    main()
