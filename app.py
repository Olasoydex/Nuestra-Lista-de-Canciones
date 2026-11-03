import os
import pandas as pd
import streamlit as st
from datetime import datetime

DATA_FILE = "canciones_dedicadas.csv"

# Configuración de la página
st.set_page_config(page_title="Lista de Canciones 🐥💖", page_icon="🎵", layout="centered")

# Estilos CSS con pestañas estilo navegador y el marco general que dibujaste
st.markdown("""
    <style>
    /* Fondo general morado */
    .stApp {
        background-color: #2e1065;
        color: #fef08a;
    }
    
    /* Textos principales y títulos en amarillo dorado */
    h1, h2, h3 {
        color: #fde047 !important;
        font-family: 'Helvetica Neue', sans-serif;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }

    p, label, .streamlit-expanderHeader, .stMarkdown {
        color: #fef08a !important;
    }

    /* Animación del disco LP */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .lp-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 15px;
    }
    .lp-record {
        width: 130px;
        height: 130px;
        background: radial-gradient(circle, #1e1b4b 18%, #f59e0b 19%, #1e1b4b 24%, #4c1d95 40%, #1e1b4b 42%, #5b21b6 60%, #1e1b4b 62%);
        border-radius: 50%;
        border: 4px solid #fde047;
        box-shadow: 0 8px 20px rgba(253, 224, 71, 0.3);
        animation: spin 8s linear infinite;
        position: relative;
    }
    .lp-center {
        width: 40px;
        height: 40px;
        background: #f59e0b;
        border-radius: 50%;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        border: 2px solid #3b0764;
    }
    .lp-hole {
        width: 8px;
        height: 8px;
        background: #2e1065;
        border-radius: 50%;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }

    /* Marco general que encierra el contenido (como lo dibujaste) */
    .marco-contenido {
        border: 3px solid #fde047;
        border-radius: 0 0 15px 15px;
        padding: 25px;
        background-color: #240c50;
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
        margin-top: -10px;
    }

    /* Cajas de texto con bordes dorados, fondo morado y texto de ejemplo en amarillo dorado */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #3b0764 !important;
        border: 2px solid #fde047 !important;
        border-radius: 8px !important;
        color: #fde047 !important;
    }
    .stTextInput > div > div > input::placeholder, .stTextArea > div > div > textarea::placeholder {
        color: #fde047 !important;
        opacity: 0.8 !important;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #fbbf24 !important;
        box-shadow: 0 0 10px rgba(253, 224, 71, 0.6) !important;
        color: #fde047 !important;
    }

    /* Pestañas (Tabs) estilo navegador Google con rebordeado dorado */
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
        background-color: transparent;
        border-bottom: none;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #3b0764;
        border: 2px solid #fde047 !important;
        border-bottom: none !important;
        border-radius: 10px 10px 0 0 !important;
        color: #fde047 !important;
        font-weight: bold;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #240c50 !important;
        border-top: 4px solid #fde047 !important;
        color: #ffffff !important;
    }

    /* Botón principal estilizado */
    .stButton > button {
        background: linear-gradient(135deg, #f59e0b, #7c3aed);
        color: #ffffff !important;
        border-radius: 10px;
        font-weight: bold;
        border: 2px solid #fde047;
        padding: 0.6rem 1.2rem;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #d97706, #6d28d9);
    }

    /* Tarjetas de visualización */
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

# Cabecera con Disco LP girando y tus textos originales
st.markdown("""
    <div class="lp-container">
        <div class="lp-record">
            <div class="lp-center">
                <div class="lp-hole"></div>
            </div>
        </div>
    </div>
    <h1 style="text-align: center; color: #fde047;">Lista de Canciones 🐥💖</h1>
    <p style="text-align: center; color: #fde047; font-size: 16px; font-weight: 500; margin-bottom: 25px;">
        Nuestra lista de canciones que nos hemos dedicado, esto quedará, hasta el final de la vida.
    </p>
""", unsafe_allow_html=True)

menu = st.tabs(["Registrar una canción", "Ver y escuchar nuestras listas"])

# Abrimos el contenedor con el marco dorado que dibujaste
st.markdown('<div class="marco-contenido">', unsafe_allow_html=True)

with menu[0]:
    st.markdown("<h3 style='color: #fde047; margin-top: 0;'>Registrar una canción</h3>", unsafe_allow_html=True)
    
    with st.form("registro_form", clear_on_submit=True):
        autor = st.radio("¿Quién está registrando la canción?", ["Santiago 🐥(Para Tali)", "Taliana 💖(Para Puente)"])
        titulo = st.text_input("Título de la canción", placeholder="Ej. IMU")
        artista = st.text_input("Artista", placeholder="Ej. Jorge Cuellar")
        enlace = st.text_input("Enlace de YouTube (Opcional)", placeholder="Link de la canción")
        mensaje = st.text_area("Mensaje o dedicatoria", placeholder="¿Qué te recuerda de mí esta canción? (Opcional)")
        
        submitted = st.form_submit_button("Registrar Canción")
        
        if submitted:
            if titulo and artista:
                guardar_cancion(autor, titulo, artista, enlace, mensaje)
                st.success(f"¡Canción '{titulo}' registrada con éxito! Los campos se han limpiado para la siguiente.")
            else:
                st.error("Por favor, llena al menos el título y el artista.")

with menu[1]:
    st.markdown("<h3 style='color: #fde047; margin-top: 0;'>Ver y escuchar nuestras listas</h3>", unsafe_allow_html=True)
    filtro = st.radio("Filtrar Lista", ["Mis canciones 🐥(Dedicatorias para Tali)", "Mis canciones 💖(Dedicatorias para Puente)", "Ver todas juntas 🐥💖"])
    
    df = cargar_canciones()
    
    if not df.empty:
        if "Santiago" in filtro:
            df_filtrado = df[df["Autor"] == "Santiago 🐥(Para Tali)"]
        elif "Taliana" in filtro or "Puente" in filtro:
            df_filtrado = df[df["Autor"] == "Taliana 💖(Para Puente)"]
        else:
            df_filtrado = df
            
        st.dataframe(df_filtrado[["N°", "Autor", "Título", "Artista", "Fecha"]], use_container_width=True)
        
        if not df_filtrado.empty:
            st.markdown("---")
            st.markdown("<h3 style='color: #fde047;'>Reproductor y detalles</h3>", unsafe_allow_html=True)
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

# Cerramos el contenedor del marco dorado
st.markdown('</div>', unsafe_allow_html=True)
