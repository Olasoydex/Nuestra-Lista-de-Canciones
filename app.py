import os
import pandas as pd
import streamlit as st
from datetime import datetime

DATA_FILE = "canciones_dedicadas.csv"

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
    if not titulo or not artista:
        return "⚠️ Por favor, llena al menos el título y el artista."
    
    df = cargar_canciones()
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    nueva_fila = pd.DataFrame([[0, autor, titulo, artista, fecha_actual, enlace if enlace else "", mensaje if mensaje else ""]], 
                              columns=["N°", "Autor", "Título", "Artista", "Fecha", "Enlace", "Mensaje"])
    
    df = pd.concat([df, nueva_fila], ignore_index=True)
    df["N°"] = range(1, len(df) + 1)
    df.to_csv(DATA_FILE, index=False)
    
    return f"✨ ¡Canción '{titulo}' registrada con éxito en la lista de {autor}! 💖"

def eliminar_cancion(num):
    df = cargar_canciones()
    if df.empty or num < 1 or num > len(df):
        return f"⚠️ No existe la canción con el número N° {num}."
    
    df = df[df["N°"] != num].reset_index(drop=True)
    if not df.empty:
        df["N°"] = range(1, len(df) + 1)
    
    df.to_csv(DATA_FILE, index=False)
    return f"🗑️ Canción N° {num} eliminada correctamente."

# Configuración de la página en Streamlit
st.set_page_config(page_title="Nuestra Playlist 🐥💖", page_icon="🎶", layout="centered")

st.title("🎶 Lista de Canciones 🐥💖")
st.write("Nuestra lista de canciones que nos hemos dedicado, esto quedará, hasta el final de la vida.")

menu = st.tabs(["Registrar una canción", "Ver y escuchar nuestras listas"])

with menu[0]:
    st.subheader("Registrar una canción")
    autor = st.radio("¿Quién está registrando la canción?", ["Santiago 🐥(Para Tali)", "Taliana 💖(Para Puente)"])
    titulo = st.text_input("Título de la canción", placeholder="Ej. IMU")
    artista = st.text_input("Artista", placeholder="Ej. Jorge Cuellar")
    enlace = st.text_input("Enlace de YouTube (Opcional)", placeholder="Link de la canción")
    mensaje = st.text_area("Mensaje o dedicatoria", placeholder="¿Qué te recuerda de mi esta canción? OPCIONAL")
    
    if st.button("Registrar Canción", type="primary"):
        if titulo and artista:
            msg = guardar_cancion(autor, titulo, artista, enlace, mensaje)
            st.success(msg)
        else:
            st.error("⚠️ Por favor, llena al menos el título y el artista.")

with menu[1]:
    st.subheader("Selecciona qué lista deseas explorar:")
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
            st.subheader("📖 Detalles y Reproductor")
            num_seleccionado = st.selectbox("Selecciona el número (N°) de la canción para ver detalles:", df_filtrado["N°"].tolist())
            
            fila = df[df["N°"] == num_seleccionado].iloc[0]
            st.markdown(f"### 🎵 {fila['Título']} - {fila['Artista']}")
            st.write(f"**Registrada por:** {fila['Autor']} | **Fecha:** {fila['Fecha']}")
            st.info(f"Mensaje: *{fila['Mensaje'] if fila['Mensaje'] else 'Sin mensaje especial'}*")
            
            link = str(fila["Enlace"])
            if "youtube.com/watch?v=" in link:
                yt_id = link.split("v=")[1].split("&")[0]
                st.video(f"https://www.youtube.com/watch?v={yt_id}")
            elif "youtu.be/" in link:
                yt_id = link.split("youtu.be/")[1].split("?")[0]
                st.video(f"https://www.youtube.com/watch?v={yt_id}")
            elif link.strip() != "":
                st.markdown(f"🔗 [Abrir enlace externo]({link})")
            else:
                st.write("🎵 Esta canción no tiene enlace adjunto.")
                
            st.markdown("---")
            if st.button("🗑️ Eliminar esta canción"):
                res_del = eliminar_cancion(int(num_seleccionado))
                st.warning(res_del)
                st.rerun()
    else:
        st.info("Aún no hay canciones registradas. ¡Agrega la primera en la pestaña anterior!")
