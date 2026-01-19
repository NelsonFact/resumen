import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Configuración de la página
st.set_page_config(page_title="Tablero Control TD Interactivo", layout="wide")

@st.cache_data
def load_data():
    file = 'resumen.xlsx'
    # Cargamos Resumen para los filtros y TD para las metas
    df_res = pd.read_excel(file, sheet_name='resumen')
    df_res.columns = df_res.columns.str.strip()
    return df_res

try:
    df_res = load_data()

    # --- BARRA LATERAL (SEGMENTADORES) ---
    st.sidebar.header("🎯 Filtros de Control")
    
    # Segmentador de Sede
    lista_sedes = ["TODAS"] + list(df_res['SEDE'].unique())
    sede_sel = st.sidebar.selectbox("Seleccionar Sede", lista_sedes)

    # Segmentador de Servicio
    lista_servicios = ["TODOS"] + list(df_res['servicio'].unique())
    servicio_sel = st.sidebar.selectbox("Seleccionar Servicio", lista_servicios)

    # Aplicar filtros a los datos para el cálculo "Real"
    df_filtrado = df_res.copy()
    if sede_sel != "TODAS":
        df_filtrado = df_filtrado[df_filtrado['SEDE'] == sede_sel]
    if servicio_sel != "TODOS":
        df_filtrado = df_filtrado[df_filtrado['servicio'] == servicio_sel]

    # --- LÓGICA DE LA HOJA TD ---
    # Valores base de tu hoja TD
    meta_total = 10500000000
    meta_ideal_pct = 0.45
    valor_real = df_filtrado['valor_total'].sum()
    cumplimiento = valor_real / meta_total
    diferencia = (meta_total * meta_ideal_pct) - valor_real

    # Título dinámico según el filtro
    st.title(f"📊 Dashboard Gerencial: {sede_sel}")
    st.markdown(f"**Filtrado por:** Sede: `{sede_sel}` | Servicio: `{servicio_sel}`")
    st.divider()

    # --- BLOQUE 1: KPIs ESTILO TD ---
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.metric("REAL ENTREGADO", f"${valor_real:,.0f}")
    with c2:
        # Si la diferencia es positiva, estamos por debajo de la meta ideal
        color_diff = "inverse" if diferencia > 0 else "normal"
        st.metric("DIFERENCIA VS META IDEAL", f"-${diferencia:,.0f}", delta_color=color_diff)
    with c3:
        st.metric("% CUMPLIMIENTO GLOBAL", f"{cumplimiento:.2%}", 
                  delta=f"{(cumplimiento - meta_ideal_pct):.2%} vs Ideal (45%)")

    st.markdown("---")

    # --- BLOQUE 2: GRÁFICO DE CUMPLIMIENTO (GAUGE) ---
    st.subheader("🎯 Progreso de la Meta Seleccionada")
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = cumplimiento * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        delta = {'reference': 45, 'increasing': {'color': "green"}},
        gauge = {
            'axis': {'range': [None, 100], 'tickcolor': "darkblue"},
            'bar': {'color': "#1f77b4"},
            'steps': [
                {'range': [0, 45], 'color': "#ffcccb"},
                {'range': [45, 100], 'color': "#d1e7dd"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'value': 45}}))

    st.plotly_chart(fig, use_container_width=True)

    # --- BLOQUE 3: DETALLE DE LOS DATOS FILTRADOS ---
    with st.expander("🔍 Ver registros filtrados"):
        st.dataframe(df_filtrado[['fecha_fact', 'responsable', 'paciente', 'valor_total', 'SEDE', 'servicio']], use_container_width=True)

except Exception as e:
    st.error(f"Error al cargar datos: {e}")
    st.info("Asegúrate de que el archivo sea 'resumen.xlsx' con las hojas correctamente nombradas.")