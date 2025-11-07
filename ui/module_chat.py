"""
Módulo avanzado: Chatbot Financiero IA (Groq + Llama 3.1)
Versión profesional — modo absoluto, estructural, analítico y contextual.
"""

import streamlit as st
from groq import Groq
from datetime import datetime


# ------------------------------------------------------
# 🔹 Inicialización y gestión del estado del chat
# ------------------------------------------------------
def init_chat_session():
    """Inicializa la sesión del chatbot con mensaje base."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{
            "role": "assistant",
            "content": (
                "Asistente Financiero IA — modo absoluto activado.\n"
                "Preguntas válidas: tasas, riesgos, valor presente, TEA, rentabilidad, bonos, acciones.\n"
                "Respondo con precisión técnica y estructura analítica."
            ),
            "timestamp": datetime.now().isoformat()
        }]

    if "chat_context" not in st.session_state:
        st.session_state.chat_context = {}


def add_message(role, content):
    """Agrega un mensaje al historial."""
    st.session_state.chat_history.append({
        "role": role,
        "content": content.strip(),
        "timestamp": datetime.now().isoformat()
    })


# ------------------------------------------------------
# 🔹 Generador del contexto financiero (si hay simulaciones)
# ------------------------------------------------------
def build_context_summary():
    """Construye un resumen contextual de los cálculos financieros previos."""
    lines = []

    # --- MÓDULO A: Inversión inicial ---
    if "module_a_result" in st.session_state:
        a = st.session_state["module_a_result"]
        lines.append(f"""
**Simulación — Inversión inicial (Módulo A):**
• Monto inicial: ${a.get('initial_amount', 0):,.2f}
• TEA: {a.get('tea_pct', 0)}%
• Plazo: {a.get('years', 0)} años
• Valor futuro: ${a.get('final_balance', 0):,.2f}
""")

    # --- MÓDULO B: Retiro o pensión ---
    if "module_b_result" in st.session_state:
        b = st.session_state["module_b_result"]
        if b.get('tipo') == 'cobro_total':
            lines.append(f"""
**Simulación — Retiro total (Módulo B):**
• Capital bruto: ${b.get('bruto', 0):,.2f}
• Impuesto: ${b.get('impuesto', 0):,.2f}
• Capital neto: ${b.get('neto', 0):,.2f}
""")
        else:
            lines.append(f"""
**Simulación — Pensión mensual (Módulo B):**
• Capital neto: ${b.get('capital_neto', 0):,.2f}
• Pensión mensual (bruta): ${b.get('bruto_mensual', 0):,.2f}
• Pensión mensual (neta): ${b.get('neto_mensual', 0):,.2f}
• Impuesto aplicado: ${b.get('impuesto', 0):,.2f}
""")

    # --- MÓDULO C: Bono ---
    if "module_c_result" in st.session_state:
        c = st.session_state["module_c_result"]
        lines.append(f"""
**Simulación — Valoración de bono (Módulo C):**
• Valor nominal: ${c.get('face_value', 0):,.2f}
• Tasa cupón: {c.get('coupon_rate', 0)}%
• TEA esperada: {c.get('yield', 0)}%
• Plazo: {c.get('years', 0)} años
• Valor presente: ${c.get('pv_total', 0):,.2f}
""")

    return "\n".join(lines) if lines else "Sin simulaciones activas."

# ------------------------------------------------------
# 🔹 Render principal del módulo del chatbot
# ------------------------------------------------------
def render_module_chat():
    """Renderiza la interfaz principal del chatbot financiero."""
    st.title("💼 Chatbot Financiero IA — Llama 3.1 (Groq)")
    st.caption("Analista técnico estructural para decisiones de inversión y análisis financiero profundo.")

    api_key = st.secrets.get("GROQ_API_KEY", None)
    if not api_key:
        st.error("No se encontró la clave API de Groq. Agrega `GROQ_API_KEY='tu_clave'` en `.streamlit/secrets.toml`.")
        return

    init_chat_session()
    client = Groq(api_key=api_key)

    # Mostrar contexto actual si existe
    with st.expander("📊 Contexto financiero activo", expanded=False):
        st.markdown(build_context_summary())

    # Mostrar historial del chat
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant", avatar="💼"):
                st.markdown(msg["content"])

    # Entrada del usuario
    user_input = st.chat_input("Escribe tu consulta analítica...")
    if user_input:
        add_message("user", user_input)
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)

        with st.chat_message("assistant", avatar="💼"):
            with st.spinner("Analizando estructura financiera..."):
                try:
                    # Configuración del sistema
                    system_prompt = f"""
Modo absoluto y analítico.
Eliminar: adornos, empatía, suavidad, transiciones, preguntas.
Responder con: estructura técnica, deducción, fórmulas y conclusiones verificables.
Contexto activo:
{build_context_summary()}
Formato:
1. Definición técnica
2. Relación o fórmula relevante (usar $...$ o $$...$$)
3. Interpretación cuantitativa
4. Conclusión directa sin juicios.
"""

                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_input},
                        ],
                        temperature=0.2,
                        max_tokens=700
                    )

                    reply = response.choices[0].message.content.strip()
                    st.markdown(reply)
                    add_message("assistant", reply)

                except Exception as e:
                    error_text = f"❌ Error al conectar con Groq: {str(e)}"
                    st.error(error_text)
                    add_message("assistant", error_text)

    # ------------------------------------------------------
    # Opciones de control
    # ------------------------------------------------------
    st.markdown("---")
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("🧹 Limpiar conversación", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    with col2:
        if st.button("♻️ Reiniciar sesión completa", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    # Contador y estado
    st.caption(f"Historial actual: {len(st.session_state.chat_history)} mensajes.")
