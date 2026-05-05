import streamlit as st
import ollama
import fitz  # PyMuPDF
import sqlite3
import os
import hashlib
from faster_whisper import WhisperModel
from fpdf import FPDF
from audio_recorder_streamlit import audio_recorder
from datetime import datetime

# --- CONFIGURACIÓN DE ENTORNO ---
st.set_page_config(page_title="FIBRACELL IA", layout="wide", page_icon="📡")

# Inicialización de directorios de sistema
for path in ['brain', 'brain/assets', 'input']:
    if not os.path.exists(path):
        os.makedirs(path)

# --- CLASE MAESTRA DE PDF (DISEÑO PROFESIONAL) ---
class ReportePro(FPDF):
    def __init__(self, titulo, usuario):
        super().__init__()
        self.titulo_rep = titulo
        self.user = usuario
        self.azul_fibracell = (30, 58, 138)

    def header(self):
        # Banner Superior Corporativo
        self.set_fill_color(*self.azul_fibracell)
        self.rect(0, 0, 210, 40, 'F')
        
        # Logo de Empresa
        ruta_logo = "brain/assets/logo_empresa.png"
        if os.path.exists(ruta_logo):
            self.image(ruta_logo, 10, 8, 25)
            self.set_x(40)
        
        self.set_font('Arial', 'B', 15)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, self.titulo_rep, 0, 1, 'C')
        self.set_font('Arial', 'I', 8)
        self.cell(0, 5, "FIBRACELL S.A. DE C.V. - Concesionaria de Redes Públicas", 0, 1, 'C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Generado por {self.user} | {datetime.now().strftime('%d/%m/%Y')} | Pág {self.page_no()}", 0, 0, 'C')

# --- SISTEMA DE BASE DE DATOS (SQLite) ---
def init_db():
    conn = sqlite3.connect('brain/fibracell_core.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS modelos (id TEXT PRIMARY KEY, nombre TEXT, contenido TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS aprendizaje (id INTEGER PRIMARY KEY AUTOINCREMENT, mejora TEXT, fecha DATETIME)')
    conn.commit()
    conn.close()

def buscar_contexto_sql(orden):
    conn = sqlite3.connect('brain/fibracell_core.db')
    palabras = orden.split()
    if not palabras: return ""
    query = "SELECT contenido FROM modelos WHERE " + " OR ".join(["contenido LIKE ?"] * len(palabras))
    params = [f'%{p}%' for p in palabras]
    res = conn.execute(query, params).fetchall()
    conn.close()
    return "\n".join([r[0][:1200] for r in res[:2]])

# --- SKILLS DE PROCESAMIENTO ---
def skill_limpieza_pdf(texto):
    """Elimina artefactos de Markdown y corrige caracteres para el PDF."""
    texto = texto.replace('*', '')  # Adiós asteriscos
    texto = texto.replace('#', '')  # Adiós hashtags de títulos
    texto = texto.replace('—', '-').replace('–', '-') # Guiones compatibles
    return texto.strip()

def skill_razonamiento_fibracell(orden, contexto, mejoras):
    """Genera contenido usando lógica de negocio de la empresa."""
    prompt = f"""
    Eres el redactor senior de FIBRACELL S.A. DE C.V.
    CONTEXTO DE PLANTILLA: {contexto}
    REGLAS DE APRENDIZAJE: {mejoras}
    ORDEN DEL USUARIO: {orden}
    
    INSTRUCCIONES:
    1. Escribe el documento completo.
    2. No uses asteriscos para negritas.
    3. Usa lenguaje técnico de telecomunicaciones.
    4. Omite introducciones como 'Aquí tienes el reporte'.
    """
    res = ollama.generate(model='llama3.2:3b', prompt=prompt)
    return res['response']

# --- INTERFAZ PRINCIPAL ---
init_db()
st.sidebar.title("📡 Panel FIBRACELL")
rol_actual = st.sidebar.selectbox("Rol:", ["Administrador", "Operador NOC", "Gerente"])

if rol_actual == "Administrador":
    up = st.sidebar.file_uploader("Indexar Plantilla (PDF)", type="pdf")
    if up and st.sidebar.button("Guardar en Biblioteca"):
        with fitz.open(stream=up.read(), filetype="pdf") as doc:
            texto = "".join([p.get_text() for p in doc])
            m_id = hashlib.md5(texto.encode()).hexdigest()
            conn = sqlite3.connect('brain/fibracell_core.db')
            conn.execute("INSERT OR REPLACE INTO modelos VALUES (?, ?, ?)", (m_id, up.name, texto))
            conn.commit()
            conn.close()
            # Intento de extraer logo
            if not os.path.exists("brain/assets/logo_empresa.png"):
                for pag in doc:
                    imgs = pag.get_images()
                    if imgs:
                        xref = imgs[0][0]
                        base = doc.extract_image(xref)
                        with open("brain/assets/logo_empresa.png", "wb") as f: f.write(base["image"])
                        break
        st.sidebar.success("Modelo e identidad visual indexados.")

# --- FLUJO DE TRABAJO ---
st.header("🧠 Agente Office Fibracell")
audio = audio_recorder(text="Dictar Orden", icon_size="2x", neutral_color="#1E3A8A")
st.text("Este proyecto genera documentacion con base a la inforacion proporcionada de parte del administrador, todo analizado por una inteligencia artificial")

instruccion = ""
if audio:
    with st.spinner("Escuchando..."):
        with open("temp.wav", "wb") as f: f.write(audio)
        model_w = WhisperModel("tiny", device="cpu", compute_type="int8")
        segs, _ = model_w.transcribe("temp.wav")
        instruccion = " ".join([s.text for s in segs])

txt_orden = st.text_area("Instrucción del documento:", value=instruccion)

if st.button("🚀 Generar con Skills de Producción"):
    if txt_orden:
        contexto = buscar_contexto_sql(txt_orden)
        conn = sqlite3.connect('brain/fibracell_core.db')
        mejoras = [r[0] for r in conn.execute("SELECT mejora FROM aprendizaje ORDER BY fecha DESC LIMIT 5").fetchall()]
        conn.close()

        with st.spinner("Razonando y aplicando limpieza..."):
            # Aplicar Skill de Razonamiento
            respuesta_cruda = skill_razonamiento_fibracell(txt_orden, contexto, mejoras)
            # Aplicar Skill de Limpieza (Eliminar asteriscos aquí también)
            st.session_state['resultado_ia'] = skill_limpieza_pdf(respuesta_cruda)

# --- REVISIÓN Y DESCARGA ---
if 'resultado_ia' in st.session_state:
    st.divider()
    texto_final = st.text_area("Revisión final:", value=st.session_state['resultado_ia'], height=300)
    
    c1, c2 = st.columns(2)
    with c1:
        feedback = st.text_input("Corrección para el aprendizaje:")
        if st.button("💾 Aprender"):
            conn = sqlite3.connect('brain/fibracell_core.db')
            conn.execute("INSERT INTO aprendizaje (mejora, fecha) VALUES (?, ?)", (feedback, datetime.now()))
            conn.commit()
            conn.close()
            st.success("Feedback guardado.")

    with c2:
        pdf = ReportePro("REPORTE OFICIAL FIBRACELL", rol_actual)
        pdf.add_page()
        pdf.set_font("Arial", size=11)
        
        # Limpieza final de seguridad para el motor FPDF
        txt_pdf = texto_final.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 8, txt_pdf)
        
        pdf_bytes = pdf.output(dest='S')
        if isinstance(pdf_bytes, bytearray): pdf_bytes = bytes(pdf_bytes)

        st.download_button(
            label="📥 Descargar PDF Limpio",
            data=pdf_bytes,
            file_name=f"Fibracell_Final_{datetime.now().strftime('%H%M%S')}.pdf",
            mime="application/pdf"
        )