import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Clínica 2026", layout="wide")

@st.cache_data
def load_data():
    file = 'resumen.xlsx'
    # Cargamos las hojas con los nombres exactos que detecté en tu archivo
    df_res = pd.read_excel(file, sheet_name='resumen')
    df_env = pd.read_excel(file, sheet_name='envios')
    df_td = pd.read_excel(file, sheet_name='TD')
    
    # LIMPIEZA CRÍTICA: Quitamos espacios vacíos en los nombres de columnas
    df_res.columns = df_res.columns.str.strip()
    df_env.columns = df_env.columns.str.strip()
    df_td.columns = df_td.columns.str.strip()
    
    return df_res, df_env, df_td

try:
    res, env, td = load_data()

    st.title("🏥 Control Gerencial de Facturación 2026")
    st.markdown("---")

    # --- MÉTRICAS DESDE TU HOJA 'TD' ---
    # Según tus datos: Meta Total = 10,500,000,000
    col1, col2, col3 = st.columns(3)
    total_facturado = res['valor_total'].sum()
    meta = 10500000000
    cumplimiento = (total_facturado / meta)

    with col1:
        st.metric("Facturación Real", f"${total_facturado:,.0f}")
    with col2:
        st.metric("Meta Mensual", "$10,500,000,000")
    with col3:
        st.metric("% Cumplimiento", f"{cumplimiento:.2%}")

    st.divider()

    # --- GRÁFICOS ---
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("📍 Facturación por Sede")
        # Usamos la columna 'SEDE' que detecté en tu archivo
        fig1 = px.pie(res, names='SEDE', values='valor_total', hole=0.4)
        st.plotly_chart(fig1, use_container_width=True)

    with c2:
        st.subheader("📈 Top 10 Aseguradoras")
        top_eps = res.groupby('responsable')['valor_total'].sum().nlargest(10).reset_index()
        fig2 = px.bar(top_eps, x='valor_total', y='responsable', orientation='h', 
                      color='valor_total', color_continuous_scale='Viridis')
        st.plotly_chart(fig2, use_container_width=True)

    # --- TABLA DE AUDITORÍA ---
    st.subheader("🔍 Detalle de Facturas Recientes")
    st.dataframe(res[['num_factura', 'paciente', 'responsable', 'valor_total', 'SEDE']].tail(10), use_container_width=True)

except Exception as e:
    st.error(f"Error técnico: {e}")
    st.info("Revisa que las pestañas del Excel se llamen: resumen, envios y TD.")