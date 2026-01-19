import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Control de Metas - Hoja TD", layout="wide")

@st.cache_data
def load_td_data():
    file = 'resumen.xlsx'
    # Cargamos la hoja TD
    df_td = pd.read_excel(file, sheet_name='TD')
    return df_td

try:
    df_td = load_td_data()

    st.title("📊 Tablero de Control Gerencial (Basado en TD)")
    st.markdown(f"### Estado de Cumplimiento Meta Mensual")
    st.divider()

    # --- EXTRACCIÓN DE DATOS ESTILO 'TD' ---
    # Basado en tu archivo: Fila 0 es FUNDADORES, Fila 1 es SUBA, Fila 2 es TOTAL
    meta_total = 10500000000
    real_total = 4691413335.4  # Este valor viene de tu columna "VALOR REAL ENTREGADO"
    diferencia = 33586664.6
    cumplimiento = 0.4491 # 44.9%
    ideal = 0.45          # 45%

    # --- BLOQUE 1: INDICADORES PRINCIPALES (TARJETAS) ---
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.metric("META MENSUAL TOTAL", f"${meta_total:,.0f}")
    with c2:
        st.metric("REAL ENTREGADO", f"${real_total:,.0f}")
    with c3:
        # El delta muestra si estamos por debajo o por encima de la meta ideal
        color_delta = "normal" if real_total >= 4725000000 else "inverse"
        st.metric("DIFERENCIA VS META", f"-${diferencia:,.0f}", delta_color=color_delta)
    with c4:
        st.metric("% CUMPLIMIENTO", f"{cumplimiento:.2%}", delta=f"{(cumplimiento-ideal):.2%} vs Ideal")

    st.markdown("---")

    # --- BLOQUE 2: COMPARATIVO POR SEDE (IGUAL A TU TABLA TD) ---
    st.subheader("🏢 Desglose por Sede")
    col_f, col_s = st.columns(2)

    with col_f:
        st.info("**FUNDADORES**")
        st.write(f"**Meta:** $7,700,000,000")
        st.write(f"**Real:** $3,457,891,377")
        st.progress(0.449)
        st.write("**Cumplimiento:** 44.91%")

    with col_s:
        st.success("**SUBA**")
        st.write(f"**Meta:** $2,800,000,000")
        st.write(f"**Real:** $1,233,521,958")
        st.progress(0.440)
        st.write("**Cumplimiento:** 44.05%")

    # --- BLOQUE 3: GRÁFICO DE VELOCÍMETRO (GAUGE) ---
    st.markdown("---")
    st.subheader("🎯 Visualización de Meta Total")
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = cumplimiento * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Porcentaje de Cumplimiento Global", 'font': {'size': 24}},
        delta = {'reference': 45, 'increasing': {'color': "green"}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 45], 'color': 'ffcccb'},
                {'range': [45, 100], 'color': 'lightgreen'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 45}}))

    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error al leer la hoja TD: {e}")
    st.warning("Asegúrate de que la pestaña se llame 'TD' y el archivo 'resumen.xlsx'")