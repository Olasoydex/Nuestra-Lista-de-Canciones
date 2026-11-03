import os
import pandas as pd
import streamlit as st
from datetime import datetime

DATA_FILE = "canciones_dedicadas.csv"

# Configuración de la página
st.set_page_config(page_title="Nuestra Playlist", page_icon="🎵", layout="centered")

# Estilos CSS combinando amarillo y morado con disco LP animado
st.markdown("""
    <style>
    /* Fondo general */
    .stApp {
        background-color: #2e1065;
        color: #f3e8ff;
    }
    
    /* Tipografías y títulos en tonos morados y amarillos */
    h1, h2, h3 {
        color: #fde047 !important;
        font-family: 'Helvetica Neue', sans-serif;
    }

    /* Animación del disco LP (Vinilo morado y acentos amarillos) */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .lp-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }
    .lp-record {
        width: 140px;
        height: 140px;
        background: radial-gradient(circle, #1e1b4b 18%, #f59e0b 19%, #1e1b4b 24%, #4c1d95 40%, #1e1b4b 42%, #5b21b6 60%, #1e1b4b 62%);
        border-radius: 50%;
        border: 4px solid #fde047;
        box-shadow: 0 8px 25px rgba(253, 224, 71, 0.2);
        animation: spin 8s linear infinite;
        position: relative;
    }
    .lp-center {
        width: 45px;
        height: 45px;
        background: #f59e0b;
        border-radius: 50%;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        border: 2px solid #3b0764;
    }
    .lp-hole {
        width: 10px;
        height: 10px;
        background: #2e1065;
        border-radius: 50%;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }

    /* Recuadros de campos de texto decorados en amarillo brillante y fondo morado oscuro */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #3b0764 !important;
        border: 2px solid #fde047 !important;
        border-radius: 8px !important;
        color: #fef08a !important;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #f59e0b !important;
        box-shadow: 0 0 10px rgba(253, 224, 71, 0.4) !important;
    }

    /* Etiquetas de los inputs */
    .stTextInput label, .stTextArea label, .stRadio label {
        color: #fef08a !important;
        font-weight: 500;
    }

    /* Botón principal estilizado */
    .stButton > button {
        background: linear-gradient(135deg, #f59e0b, #7c3aed);
        color: #ffffff !important;
        border-radius: 10px;
        font-weight: bold;
        border: 2px solid #fde047;
        padding: 0.6rem 1.2rem;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #d97706, #6d28d9);
        color: #ffffff !important;
    }

    /* Tarjetas de canciones en combinaciones de amarillo y morado */
    .card-yellow {
        background-color: #422006;
        border-left: 6px solid #fde047;
        border-right: 2px solid #f59e0b;
        padding: 18px;
        border-radius: 12px;
        margin-bottom: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        color: #fef08a;
    }
    .card-purple {
        background-color: #3b0764;
        border-left: 6px solid #a855f7;
        border-right: 2px solid #7c3aed;
        padding: 18px;
        border-radius: 12px;
        margin-bottom: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        color: #f3e8ff;
    }
    </style>
""", unsafe_allow_html=True)

def cargar_canciones():
    expected_cols = ["N°", "Autor", "Título", "Artista", "Fecha", "Enlace", "Mensaje"]
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        for col in expected_cols:
            if col not in df.columns:
                return pd.DataFrame(columns=expected_cols)
        return df
    else:
        return pd.DataFrame(columns=expected_cols)

def guardar_cancion(autor, titulo, artista, enlace, mensaje):
    df = cargar_canciones()
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    nueva_fila = pd.DataFrame([[0, autor, titulo, artista, fecha_actual, enlace if enlace else "", mensaje if mensaje else ""]], 
                              columns=["N°", "Autor", "Título", "Artista", "Fecha", "Enlace", "Mensaje"])
    
    df = pd.concat([df, nueva_fila], ignore_index=True)
    df["N°"] = range(1, len(df) + 1)
    df.to_csv(DATA_FILE, index=False)

def eliminar_cancion(num):
    df = cargar_canciones()
    if df.empty or num < 1 or num > len(df):
        return f"No existe la canción con el número N° {num}."
    
    df = df[df["N°"] != num].reset_index(drop=True)
    if not df.empty:
        df["N°"] = range(1, len(df) + 1)
    
    df.to_csv(DATA_FILE, index=False)
    return f"Canción N° {num} eliminada correctamente."

# Cabecera con Disco LP girando y diseño morado/amarillo
st.markdown("""
    <div class="lp-container">
        <div class="lp-record">
            <div class="lp-center">
                <div class="lp-hole"></div>
            </div>
        </div>
    </div>
    <h1 style="text-align: center;">Nuestra Lista de Canciones</h1>
    <p style="text-align: center; color: #fde047; font-size: 15px;">
        Espacio guardado para la colección de dedicatorias.
    </p>
""", unsafe_allow_html=True)

menu = st.tabs(["Registrar una canción", "Ver y escuchar nuestras listas"])

with menu[0]:
    st.markdown("### Agregar nueva canción")
    
    with st.form("registro_form", clear_on_submit=True):
        autor = st.radio("¿Quién está registrando la canción?", ["Santiago (Para Tali)", "Taliana (Para Puente)"])
        titulo = st.text_input("Título de la canción", placeholder="Ej. IMU")
        artista = st.text_input("Artista", placeholder="Ej. Jorge Cuellar")
        enlace = st.text_input("Enlace de YouTube (Opcional)", placeholder="Link de la canción")
        mensaje = st.text_area("Mensaje o dedicatoria", placeholder="¿Qué te recuerda de mí esta canción? (Opcional)")
        
        submitted = st.form_submit_button("Registrar Canción")
        
        if submitted:
            if titulo and artista:
                guardar_cancion(autor, titulo, artista, enlace, mensaje)
                st.success(f"Canción '{titulo}' registrada correctamente. Los campos se han limpiado para la siguiente entrada.")
            else:
                st.error("Por favor, llena al menos el título y el artista.")

with menu[1]:
    st.markdown("### Repositorio de canciones")
    filtro = st.radio("Filtrar Lista", ["Mis canciones (Dedicatorias para Tali)", "Mis canciones (Dedicatorias para Puente)", "Ver todas juntas"])
    
    df = cargar_canciones()
    
    if not df.empty:
        if "Santiago" in filtro:
            df_filtrado = df[df["Autor"] == "Santiago (Para Tali)"]
        elif "Taliana" in filtro or "Puente" in filtro:
            df_filtrado = df[df["Autor"] == "Taliana (Para Puente)"]
        else:
            df_filtrado = df
            
        st.dataframe(df_filtrado[["N°", "Autor", "Título", "Artista", "Fecha"]], use_container_width=True)
        
        if not df_filtrado.empty:
            st.markdown("---")
            st.markdown("### Reproductor y detalles")
            num_seleccionado = st.selectbox("Selecciona el número (N°) de la canción para consultar:", df_filtrado["N°"].tolist())
            
            fila = df[df["N°"] == num_seleccionado].iloc[0]
            
            clase_tarjeta = "card-yellow" if "Santiago" in str(fila['Autor']) else "card-purple"
            
            st.markdown(f"""
                <div class="{clase_tarjeta}">
                    <h3 style="margin: 0; color: #fde047;">{fila['Título']} — {fila['Artista']}</h3>
                    <p style="margin: 5px 0; color: #fef08a;"><b>Registrada por:</b> {fila['Autor']} | <b>Fecha:</b> {fila['Fecha']}</p>
                    <p style="margin-top: 10px;"><b>Dedicatoria:</b> <i>"{fila['Mensaje'] if fila['Mensaje'] else 'Sin dedicatoria por escrito.'}"</i></p>
                </div>
            """, unsafe_allow_html=True)
            
            link = str(fila["Enlace"])
            if "youtube.com/watch?v=" in link:
                yt_id = link.split("v=")[1].split("&")[0]
                st.video(f"https://www.youtube.com/watch?v={yt_id}")
            elif "youtu.be/" in link:
                yt_id = link.split("youtu.be/")[1].split("?")[0]
                st.video(f"https://www.youtube.com/watch?v={yt_id}")
            elif link.strip() != "":
                st.markdown(f"[Abrir enlace externo de audio]({link})")
            else:
                st.info("Esta canción no cuenta con enlace adjunto.")
                
            st.markdown("---")
            if st.button("Eliminar esta canción"):
                res_del = eliminar_cancion(int(num_seleccionado))
                st.warning(res_del)
                st.rerun()
    else:
        st.info("Aún no hay canciones registradas en la lista.")
