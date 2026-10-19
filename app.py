import streamlit as st
import json
import os

st.set_page_config(page_title= "Registro de Cumpleaños FG", layout= "centered")

IMAGEN_PORTADA = "logo.png"
col_centro, col_der = st.columns([2, 1])
with col_centro:
    st.image(IMAGEN_PORTADA, use_container_width=True)

st.title("¡Registra tu cumpleaños!")
st.write("Pon tu nombre y fecha para poder celebrarte junto con tu equipo de trabajo")

FICHERO_JSON = "cumpleanos.json"

def cargar_datos():
    if os.path.exists(FICHERO_JSON):
        with open(FICHERO_JSON, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def guardar_datos(nombre, dia, mes):
    datos= cargar_datos()
    nuevo_registro = {"nombre": nombre, "dia": str(dia), "mes": mes}
    datos.append(nuevo_registro)
    with open(FICHERO_JSON, "w", encoding="utf-8") as f: 
        json.dump(datos, f, ensure_ascii=False, indent=4)

st.markdown("""
    <style>
    h1 
    {
        font-size: 24px !important;
        white-space: nowrap;
    }
    div.stButton>button:first-child, div.stFormSubmitButton>button
    {
        background-color: #FF4B4B;
        border: none;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        width: 100%;
    }
    div.stButton > button:first-child:hover 
    {
        background-color: #FF7575;
        color: white;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stStatusWidget"],
    .stAppDeployDropdown,
    div[class*="stAppDeployDropdown"],
    footer + div,
    iframe + div,
    div[style*="position: fixed"][style*="bottom"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }
""", unsafe_allow_html=True)

with st.form("formulario_cumple", clear_on_submit=True):
    nombre = st.text_input("Tu Nombre: ")

    col1, col2 = st.columns(2)
    with col1:
        dia = st.selectbox("Día:", list(range(1, 32)))
    with col2:
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        mes = st.selectbox("Mes:", meses)

    boton_enviar = st.form_submit_button("Registrar mi cumpleaños")

if boton_enviar:
    if nombre.strip() == "":
        st.error("Por favor escribe tu nombre antes de enviar")
    else:
        guardar_datos(nombre, dia, mes)
        st.success(f"¡Gracias {nombre}! Tu fecha ha sido guardada correctamente")
        st.balloons()
        st.balloons()

st.divider()
with st.expander("Ver lista de Cumpleañeros Registrados (Solo Admin)"):
    clave = st.text_input("Introduce tu Contraseña", type = "password")

    if clave == "0901":
        lista_cumples = cargar_datos()
        if lista_cumples:
            st.write("###  Fechas Registradas:")
            st.table(lista_cumples)
        else:
            st.info("Aun nadie ha registrado su cumpleaños")
    elif clave != "":
        st.error("contraseña incorrecta")
