# 📡 FIBRACELL IA SQL-Engine

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.32-FF4B4B.svg)
![Ollama](https://img.shields.io/badge/Ollama-Llama3.2-orange.svg)
![SQLite](https://img.shields.io/badge/SQLite-3.0-003B57.svg)

**FIBRACELL IA SQL-Engine** es un ecosistema de Inteligencia Artificial operativa diseñado para automatizar la generación de documentación técnica y administrativa de una concesionaria de redes públicas de telecomunicaciones. El sistema utiliza una arquitectura **RAG (Retrieval-Augmented Generation)** optimizada para hardware con recursos limitados (8GB RAM).

## 🚀 Conceptos de Valor de Negocio

*   **Mejora de Negocios con IA:** Reducción del 90% en tiempos de redacción de reportes del NOC.
*   **Automatización de Procesos:** Flujo integral desde dictado por voz (Whisper) hasta documento PDF final.
*   **Aprendizaje Evolutivo:** Base de datos de aprendizaje continuo que ajusta la terminología de la IA según el feedback del usuario.
*   **Escalabilidad:** Capacidad para gestionar más de 200 plantillas PDF mediante indexación SQL inteligente.

## 🛠️ Arquitectura Técnica

El proyecto se basa en cuatro pilares fundamentales:

1.  **Ingesta de Datos:** Extracción de texto y activos visuales (logos) de documentos PDF base mediante `PyMuPDF`.
2.  **Motor de Búsqueda SQL:** Indexación de conocimiento en `SQLite` para minimizar el consumo de memoria y maximizar la relevancia del contexto.
3.  **Procesamiento de Lenguaje (LLM):** Integración con `Ollama (Llama 3.2:3b)` para redacción técnica coherente y sin alucinaciones.
4.  **Generación de Salida:** Motor `FPDF` con "Skills" de limpieza de Markdown para la entrega de documentos profesionales listos para producción.

## 📦 Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/fibracell-ia.git](https://github.com/tu-usuario/fibracell-ia.git)
    cd fibracell-ia
