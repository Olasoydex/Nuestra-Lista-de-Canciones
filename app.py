import os
import pandas as pd
import streamlit as st
from datetime import datetime

DATA_FILE = "canciones_dedicadas.csv"

# Configuración de la página
st.set_page_config(page_title="Nuestra Playlist 🐥💖", page_icon="🎶", layout="centered")

# Estilos visuales personalizados (Tonos morados, amarillos y temática LP romántica)
st.markdown("""
    <style>
    .main {
        background-color: #f9f6fc;
    }
    h1, h2, h3 {
        color: #5b21b6 !important;
    }
    .stButton>button {
        background: linear-gradient(135deg, #7c3aed, #d97706);
        color: white;
        border-radius: 12px;
        font-weight: bold;
        border: none;
        padding: 0.5rem 1rem;
        box-shadow: 0 4px 6px rgba(124, 58, 237, 0.2);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #6d28d9, #b45309);
        color: white;
    }
    .vinyl-card {
        background: linear-gradient(135deg, #f3e8ff, #fef3c7);
        padding: 20px;
        border-radius: 15px;
        border-left: 6px solid #7c3aed;
        border-right: 6px solid #d97706;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
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
        return f"⚠️ No existe la canción con el número N° {num}."
    
    df = df[df["N°"] != num].reset_index(drop=True)
    if not df.empty:
        df["N°"] = range(1, len(df) + 1)
    
    df.to_csv(DATA_FILE, index=False)
    return f"🗑️ Canción N° {num} eliminada correctamente."

# Inicializar estados para limpiar formularios
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

st.markdown("<h1 style='text-align: center;'>🎶 Nuestra Playlist de Discos 💿 🐥💖</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #6b7280;'>Nuestra lista de canciones que nos hemos dedicado, esto quedará hasta el final de la vida. 💜💛</p>", unsafe_allow_html=True)

menu = st.tabs(["✨ Registrar una canción", "🎧 Ver y escuchar listas"])

with menu[0]:
    st.markdown("### 💽 Agregar a nuestro Vinilo Musical")
    
    with st.form("registro_form", clear_on_submit=True):
        autor = st.radio("¿Quién está registrando la canción?", ["Santiago 🐥(Para Tali)", "Taliana 💖(Para Puente)"])
        titulo = st.text_input("Título de la canción", placeholder="Ej. IMU")
        artista = st.text_input("Artista", placeholder="Ej. Jorge Cuellar")
        enlace = st.text_input("Enlace de YouTube (Opcional)", placeholder="Link de la canción")
        mensaje = st.text_area("Mensaje o dedicatoria", placeholder="¿Qué te recuerda de mí esta canción? OPCIONAL")
        
        submitted = st.form_submit_button("Registrar Canción 🎵")
        
        if submitted:
            if titulo and artista:
                guardar_cancion(autor, titulo, artista, enlace, mensaje)
                st.success(f"✨ ¡Canción '{titulo}' registrada con éxito! Ya se ha limpiado el formulario para la siguiente 💖")
            else:
                st.error("⚠️ Por favor, llena al menos el título y el artista.")

with menu[1]:
    st.subheader("🎧 Explora nuestro Repositorio Musical")
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
            st.markdown("### 🎛️ Reproductor y Detalles del LP")
            num_seleccionado = st.selectbox("Selecciona el número (N°) de la canción para reproducir:", df_filtrado["N°"].tolist())
            
            fila = df[df["N°"] == num_seleccionado].iloc[0]
            
            # Tarjeta estilizada con los colores morado y amarillo estilo disco LP
            st.markdown(f"""
                <div class="vinyl-card">
                    <h2 style="margin: 0; color: #5b21b6;">📀 {fila['Título']} - <b>{fila['Artista']}</b></h2>
                    <p style="margin: 5px 0; color: #4b5563;"><b>Registrada por:</b> {fila['Autor']} &nbsp;|&nbsp; <b>Fecha:</b> {fila['Fecha']}</p>
                    <p style="margin-top: 10px; font-style: italic; color: #1f2937;">"{fila['Mensaje'] if fila['Mensaje'] else 'Un disco guardado sin mensaje, pero con mucho sentimiento.'}"</p>
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
                st.markdown(f"🔗 [Abrir enlace externo de audio]({link})")
            else:
                st.info("🎵 Este disco LP no tiene enlace de video adjunto, ¡pero el recuerdo está a salvo!")
                
            st.markdown("---")
            if st.button("🗑️ Eliminar esta canción del disco"):
                res_del = eliminar_cancion(int(num_seleccionado))
                st.warning(res_del)
                st.rerun()
    else:
        st.info("Aún no hay canciones en el disco. ¡Agrega la primera en la pestaña de registro!")
