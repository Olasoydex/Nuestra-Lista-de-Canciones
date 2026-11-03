import pandas as pd
import streamlit as st
from datetime import datetime, timedelta, timezone
import requests

# Configuración de la página
st.set_page_config(page_title="Lista de Canciones 🐥💝", page_icon="🎵", layout="centered")

SHEET_ID = "1qjGA_JLcrJgDM8QUHTIdRsOszOukowgCtws-qZPpK"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv"
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbww1XIydnPRQvIZbbecLhBaSD7c4OEQgyJa-wpXryeAk6XaT7YXcbR08SpICqptfQim/exec"

# Estilos CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #2e1065 !important;
        color: #fef08a !important;
    }
    h1, h2, h3 {
        color: #fde047 !important;
        font-family: 'Helvetica Neue', sans-serif;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    p, label, .streamlit-expanderHeader, .stMarkdown, span {
        color: #fef08a !important;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .lp-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 10px;
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
    @keyframes fall {
        0% { transform: translateY(-15px); opacity: 0; }
        50% { opacity: 1; }
        100% { transform: translateY(45px); opacity: 0; }
    }
    .rain-container {
        position: relative;
        height: 70px;
        border: 3px solid #fde047;
        border-radius: 12px;
        background: linear-gradient(135deg, #3b0764, #4c1d95);
        display: flex;
        justify-content: space-around;
        align-items: center;
        overflow: hidden;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(253, 224, 71, 0.25);
    }
    .note {
        position: absolute;
        font-size: 20px;
        animation: fall 3s infinite linear;
    }
    .note:nth-child(1) { left: 10%; animation-delay: 0s; }
    .note:nth-child(2) { left: 30%; animation-delay: 1.2s; }
    .note:nth-child(3) { left: 50%; animation-delay: 0.4s; }
    .note:nth-child(4) { left: 70%; animation-delay: 1.8s; }
    .note:nth-child(5) { left: 88%; animation-delay: 0.7s; }
    .vhs-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 25px 0;
    }
    .vhs-tape {
        width: 250px;
        height: 150px;
        background: linear-gradient(145deg, #3b0764, #1e1b4b);
        border: 4px solid #fde047;
        border-radius: 14px;
        position: relative;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .vhs-screw {
        width: 8px;
        height: 8px;
        background: #fde047;
        border-radius: 50%;
        position: absolute;
    }
    .screw-tl { top: 8px; left: 8px; }
    .screw-tr { top: 8px; right: 8px; }
    .screw-bl { bottom: 8px; left: 8px; }
    .screw-br { bottom: 8px; right: 8px; }
    .vhs-label {
        width: 170px;
        height: 55px;
        background: #fde047;
        border-radius: 8px;
        position: absolute;
        top: 15px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: #2e1065;
        font-weight: bold;
        font-size: 16px;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.25);
        border: 1px dashed #7c3aed;
    }
    .vhs-window {
        width: 110px;
        height: 35px;
        background: #11052c;
        border: 2px solid #fde047;
        border-radius: 6px;
        position: absolute;
        bottom: 18px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        padding: 0 10px;
    }
    .reel {
        width: 26px;
        height: 26px;
        background: #3b0764;
        border: 2px solid #f59e0b;
        border-radius: 50%;
        position: relative;
    }
    .reel::after {
        content: '';
        width: 8px;
        height: 8px;
        background: #fde047;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        border-radius: 50%;
    }
    div[data-testid="stDataFrame"], .stDataFrame, [data-testid="stTable"] {
        background-color: #4c1d95 !important;
        border: 2px solid #fde047 !important;
        border-radius: 12px !important;
        padding: 8px !important;
    }
    table {
        background-color: #4c1d95 !important;
    }
    th {
        background-color: #3b0764 !important;
        color: #fde047 !important;
        font-weight: bold !important;
        border-bottom: 2px solid #fde047 !important;
    }
    td, tr {
        background-color: #4c1d95 !important;
        color: #fef08a !important;
        border-bottom: 1px solid #7c3aed !important;
    }
    div[data-testid="stDataFrame"] div, table * {
        background-color: transparent !important;
        color: #fef08a !important;
    }
    div[data-testid="stDataFrame"] th * {
        color: #fde047 !important;
    }
    input, textarea, div[data-baseweb="input"], div[data-baseweb="textarea"] {
        background-color: #3b0764 !important;
        color: #fde047 !important;
        border-radius: 8px !important;
    }
    .stTextInput input, .stTextArea textarea {
        border: 2px solid #fde047 !important;
        color: #fde047 !important;
        background-color: #3b0764 !important;
    }
    input::placeholder, textarea::placeholder {
        color: #fde047 !important;
        opacity: 0.8 !important;
    }
    .stButton > button, div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #f59e0b, #7c3aed) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        font-weight: bold !important;
        border: 2px solid #fde047 !important;
        padding: 0.6rem 1.2rem !important;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4) !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #d97706, #6d28d9) !important;
    }
    [data-testid="stForm"], .marco-contenido {
        border: 3px solid #fde047 !important;
        border-radius: 15px !important;
        padding: 25px !important;
        background-color: #3b0764 !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.4) !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
        background-color: transparent;
        border-bottom: none;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #4c1d95;
        border: 2px solid #fde047 !important;
        border-bottom: none !important;
        border-radius: 10px 10px 0 0 !important;
        color: #fde047 !important;
        font-weight: bold;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3b0764 !important;
        border-top: 4px solid #fde047 !important;
        color: #ffffff !important;
    }
    .card-yellow {
        background-color: #4c1d95;
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
    try:
        df = pd.read_csv(SHEET_URL)
        # Limpiamos nombres de columnas por si tienen espacios
        df.columns = [c.strip() for c in df.columns]
        
        expected_cols = ["N°", "Autor", "Título", "Artista", "Fecha", "Enlace", "Mensaje"]
        for col in expected_cols:
            if col not in df.columns:
                return pd.DataFrame(columns=expected_cols)
        
        df = df.dropna(subset=["Título"])
        return df
    except Exception:
        return pd.DataFrame(columns=["N°", "Autor", "Título", "Artista", "Fecha", "Enlace", "Mensaje"])

def guardar_cancion(autor, titulo, artista, enlace, mensaje):
    colombia_tz = timezone(timedelta(hours=-5))
    fecha_actual = datetime.now(colombia_tz).strftime("%d/%m/%Y %I:%M %p")
    
    payload = {
        "autor": autor,
        "titulo": titulo,
        "artista": artista,
        "fecha": fecha_actual,
        "enlace": enlace if enlace else "",
        "mensaje": mensaje if mensaje else ""
    }
    try:
        requests.post(WEB_APP_URL, json=payload)
    except Exception as e:
        print(f"Error: {e}")

def eliminar_cancion(num):
    # En Google Sheets la fila real es N° + 1 (porque la fila 1 son los encabezados)
    row_index = int(num) + 1
    payload = {
        "action": "delete",
        "rowIndex": row_index
    }
    try:
        requests.post(WEB_APP_URL, json=payload)
    except Exception as e:
        print(f"Error al eliminar: {e}")

# Cabecera con Disco LP girando
st.markdown("""
    <div class="lp-container">
        <div class="lp-record">
            <div class="lp-center">
                <div class="lp-hole"></div>
            </div>
        </div>
    </div>
    <h1 style="text-align: center; color: #fde047;">Lista de Canciones 🐥💝</h1>
    <p style="text-align: center; color: #fde047; font-size: 16px; font-weight: 500; margin-bottom: 25px;">
        Nuestra lista de canciones que nos hemos dedicado, esto quedará, hasta el final de la vida.
    </p>
""", unsafe_allow_html=True)

menu = st.tabs(["Registrar una canción", "Ver y escuchar nuestras listas"])

with menu[0]:
    with st.form("registro_form", clear_on_submit=True):
        st.markdown("<h3 style='color: #fde047; margin-top: 0;'>Registrar una canción</h3>", unsafe_allow_html=True)
        
        st.markdown("""
            <div class="rain-container">
                <div class="note">🎵</div>
                <div class="note">🎶</div>
                <div class="note">🎼</div>
                <div class="note">🎵</div>
                <div class="note">🎶</div>
            </div>
        """, unsafe_allow_html=True)
        
        autor = st.radio("¿Quién está registrando la canción?", ["Santiago 🐥", "Taliana 💝"])
        titulo = st.text_input("Título de la canción", placeholder="Ej. IMU")
        artista = st.text_input("Artista", placeholder="Ej. Jorge Cuellar")
        enlace = st.text_input("Enlace de YouTube (Opcional)", placeholder="Link de la canción")
        mensaje = st.text_area("Mensaje o dedicatoria", placeholder="¿Qué te recuerda de mí esta canción? (Opcional)")
        
        submitted = st.form_submit_button("Registrar Canción")
        
        if submitted:
            if titulo and artista:
                guardar_cancion(autor, titulo, artista, enlace, mensaje)
                st.success(f"¡Canción '{titulo}' registrada con éxito y guardada para siempre en Google Sheets! ✨")
                st.balloons()
                st.rerun()
            else:
                st.error("Por favor, llena al menos el título y el artista.")

with menu[1]:
    st.markdown('<div class="marco-contenido">', unsafe_allow_html=True)
    st.markdown("<h3 style='color: #fde047; margin-top: 0;'>Ver y escuchar nuestras listas</h3>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class="rain-container">
            <div class="note">🎵</div>
            <div class="note">🎶</div>
            <div class="note">🎼</div>
            <div class="note">🎵</div>
            <div class="note">🎶</div>
        </div>
    """, unsafe_allow_html=True)
    
    filtro = st.radio("Filtrar Lista", ["Mis canciones 🐥(Dedicatorias para Tali)", "Mis canciones 💝(Dedicatorias para Puente)", "Ver todas juntas 🐥💝"])
    
    df = cargar_canciones()
    
    if not df.empty:
        # Filtrado por autor
        if "Ver todas" in filtro:
            df_filtrado = df
        elif "🐥" in filtro:
            df_filtrado = df[df["Autor"].str.contains("Santiago", case=False, na=False)]
        elif "💝" in filtro:
            df_filtrado = df[df["Autor"].str.contains("Taliana", case=False, na=False)]
        else:
            df_filtrado = df
            
        st.dataframe(df_filtrado[["N°", "Autor", "Título", "Artista", "Fecha"]], use_container_width=True)
        
        if not df_filtrado.empty:
            st.markdown("---")
            st.markdown("<h3 style='color: #fde047;'>Reproductor y detalles</h3>", unsafe_allow_html=True)
            
            st.markdown("""
                <div class="vhs-container">
                    <div class="vhs-tape">
                        <div class="vhs-screw screw-tl"></div>
                        <div class="vhs-screw screw-tr"></div>
                        <div class="vhs-screw screw-bl"></div>
                        <div class="vhs-screw screw-br"></div>
                        <div class="vhs-label">Tu y Yo 💝</div>
                        <div class="vhs-window">
                            <div class="reel"></div>
                            <div class="reel"></div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            num_seleccionado = st.selectbox("Selecciona el número (N°) de la canción para consultar:", df_filtrado["N°"].tolist())
            
            fila = df[df["N°"] == num_seleccionado].iloc[0]
            
            clase_tarjeta = "card-yellow" if "Santiago" in str(fila['Autor']) else "card-purple"
            
            st.markdown(f"""
                <div class="{clase_tarjeta}">
                    <h3 style="margin: 0; color: #fde047;">{fila['Título']} — {fila['Artista']}</h3>
                    <p style="margin: 5px 0; color: #fef08a;"><b>Registrada por:</b> {fila['Autor']} | <b>Fecha:</b> {fila['Fecha']}</p>
                    <p style="margin-top: 10px;"><b>Dedicatoria:</b> <i>"{fila['Mensaje'] if str(fila['Mensaje']).strip() != '' else 'No tiene dedicatoria :(.'}"</i></p>
                </div>
            """, unsafe_allow_html=True)
            
            link = str(fila["Enlace"])
            if "youtube.com/watch?v=" in link:
                yt_id = link.split("v=")[1].split("&")[0]
                st.video(f"https://www.youtube.com/watch?v={yt_id}")
            elif "youtu.be/" in link:
                yt_id = link.split("youtu.be/")[1].split("?")[0]
                st.video(f"https://www.youtu.be/{yt_id}")
            elif link.strip() != "":
                st.markdown(f"[Abrir enlace externo de audio]({link})")
            else:
                st.info("Esta canción no tiene el link adjunto :(")
                
            st.markdown("---")
            if st.button("Eliminar esta canción"):
                eliminar_cancion(int(num_seleccionado))
                st.warning(f"Canción N° {num_seleccionado} eliminada correctamente.")
                st.rerun()
    else:
        st.info("No hay canciones registradas todavía.")
    st.markdown('</div>', unsafe_allow_html=True)
