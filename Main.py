import streamlit as st
import pandas as pd
from datetime import date, datetime
import json

st.set_page_config(
    page_title="SindicalIA — STM San Pedro",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── ESTILOS ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #1a3a5c;
    color: white;
}
section[data-testid="stSidebar"] * { color: white !important; }
section[data-testid="stSidebar"] .stRadio label { color: white !important; }

/* Header */
.header-box {
    background: linear-gradient(135deg, #1a3a5c 0%, #2563a8 100%);
    border-radius: 12px;
    padding: 24px 32px;
    margin-bottom: 24px;
    color: white;
}
.header-box h1 { color: white; margin: 0; font-size: 1.8rem; font-weight: 700; }
.header-box p  { color: #a8c4e0; margin: 4px 0 0; font-size: 0.95rem; }

/* Tarjetas métricas */
.metric-card {
    background: white;
    border-radius: 10px;
    padding: 18px 20px;
    border-left: 4px solid #2563a8;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
    margin-bottom: 12px;
}
.metric-card.rojo  { border-left-color: #c0392b; }
.metric-card.verde { border-left-color: #27ae60; }
.metric-card.naranja { border-left-color: #e67e22; }
.metric-label { font-size: 0.75rem; color: #6b7280; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
.metric-value { font-size: 1.9rem; font-weight: 700; color: #1a3a5c; line-height: 1.2; }
.metric-sub   { font-size: 0.8rem; color: #9ca3af; margin-top: 2px; }

/* Badges */
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
}
.badge-ok     { background: #d1fae5; color: #065f46; }
.badge-warn   { background: #fef3c7; color: #92400e; }
.badge-danger { background: #fee2e2; color: #991b1b; }
.badge-info   { background: #dbeafe; color: #1e40af; }

/* Sección */
.seccion {
    background: #f0f4f8;
    border-radius: 8px;
    padding: 10px 16px;
    margin: 16px 0 10px;
    font-weight: 700;
    color: #1a3a5c;
    font-size: 0.9rem;
    letter-spacing: 0.03em;
    text-transform: uppercase;
}

/* Tablas */
.stDataFrame { border-radius: 8px; overflow: hidden; }

/* Botones */
.stButton > button {
    background: #2563a8;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 8px 20px;
}
.stButton > button:hover { background: #1a3a5c; }

/* Alerta custom */
.alerta {
    background: #fff3cd;
    border: 1px solid #ffc107;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 0.88rem;
    color: #664d03;
}
.alerta-roja {
    background: #fee2e2;
    border-color: #f87171;
    color: #7f1d1d;
}
</style>
""", unsafe_allow_html=True)

# ── DATOS DEMO ────────────────────────────────────────────────────────────────
@st.cache_data
def cargar_datos():
    socios = pd.DataFrame([
        {"legajo":"001","nombre":"García, Roberto","area":"Corralón","limite":80000,"activo":True},
        {"legajo":"002","nombre":"Pérez, Laura","area":"Administrativo","limite":60000,"activo":True},
        {"legajo":"003","nombre":"Rodríguez, Carlos","area":"Servicios Sanitarios","limite":70000,"activo":True},
        {"legajo":"004","nombre":"Martínez, Ana","area":"Administrativo","limite":60000,"activo":True},
        {"legajo":"005","nombre":"López, Diego","area":"Corralón","limite":80000,"activo":True},
        {"legajo":"006","nombre":"Fernández, María","area":"Servicios Sanitarios","limite":70000,"activo":True},
        {"legajo":"007","nombre":"González, Héctor","area":"Corralón","limite":80000,"activo":True},
        {"legajo":"008","nombre":"Sánchez, Paula","area":"Administrativo","limite":60000,"activo":True},
        {"legajo":"009","nombre":"Torres, Ramón","area":"Servicios Sanitarios","limite":70000,"activo":False},
        {"legajo":"010","nombre":"Díaz, Silvia","area":"Administrativo","limite":60000,"activo":True},
    ])

    mercaderia = pd.DataFrame([
        {"codigo":"A01","descripcion":"Aceite girasol 1.5L","stock":48,"precio":2200},
        {"codigo":"A02","descripcion":"Arroz largo fino 1kg","stock":60,"precio":1400},
        {"codigo":"A03","descripcion":"Yerba 500g","stock":35,"precio":1800},
        {"codigo":"A04","descripcion":"Azúcar 1kg","stock":52,"precio":1100},
        {"codigo":"A05","descripcion":"Harina 000 1kg","stock":8,"precio":950},
        {"codigo":"A06","descripcion":"Fideos tallarin 500g","stock":40,"precio":800},
        {"codigo":"A07","descripcion":"Detergente 500cc","stock":25,"precio":1600},
        {"codigo":"A08","descripcion":"Leche entera 1L","stock":3,"precio":1250},
    ])

    mes_actual = date.today().strftime("%Y-%m")
    retiros = pd.DataFrame([
        {"fecha":"2025-07-02","legajo":"001","socio":"García, Roberto","item":"Aceite girasol 1.5L","cantidad":2,"monto":4400},
        {"fecha":"2025-07-03","legajo":"003","socio":"Rodríguez, Carlos","item":"Arroz largo fino 1kg","cantidad":5,"monto":7000},
        {"fecha":"2025-07-05","legajo":"002","socio":"Pérez, Laura","item":"Yerba 500g","cantidad":3,"monto":5400},
        {"fecha":"2025-07-08","legajo":"005","socio":"López, Diego","item":"Harina 000 1kg","cantidad":4,"monto":3800},
        {"fecha":"2025-07-10","legajo":"004","socio":"Martínez, Ana","item":"Detergente 500cc","cantidad":2,"monto":3200},
        {"fecha":"2025-07-12","legajo":"001","socio":"García, Roberto","item":"Fideos tallarin 500g","cantidad":6,"monto":4800},
        {"fecha":"2025-07-15","legajo":"007","socio":"González, Héctor","item":"Azúcar 1kg","cantidad":4,"monto":4400},
        {"fecha":"2025-07-18","legajo":"006","socio":"Fernández, María","item":"Aceite girasol 1.5L","cantidad":3,"monto":6600},
    ])

    adelantos = pd.DataFrame([
        {"fecha":"2025-07-01","legajo":"002","socio":"Pérez, Laura","monto":15000,"motivo":"Gastos médicos"},
        {"fecha":"2025-07-04","legajo":"005","socio":"López, Diego","monto":20000,"motivo":"Urgencia familiar"},
        {"fecha":"2025-07-09","legajo":"003","socio":"Rodríguez, Carlos","monto":25000,"motivo":"Gastos médicos"},
        {"fecha":"2025-07-14","legajo":"008","socio":"Sánchez, Paula","monto":18000,"motivo":"Materiales escolares"},
        {"fecha":"2025-07-17","legajo":"010","socio":"Díaz, Silvia","monto":30000,"motivo":"Reparación del hogar"},
    ])

    return socios, mercaderia, retiros, adelantos

socios, mercaderia, retiros, adelantos = cargar_datos()

# Calcular deuda por socio (este mes)
def deuda_socio(legajo):
    ret = retiros[retiros.legajo == legajo]["monto"].sum()
    adel = adelantos[adelantos.legajo == legajo]["monto"].sum()
    return ret + adel

def disponible_socio(legajo):
    s = socios[socios.legajo == legajo].iloc[0]
    return s["limite"] - deuda_socio(legajo)

# ── LOGIN ─────────────────────────────────────────────────────────────────────
USUARIOS = {
    "mono":    {"password": "stm2024", "rol": "admin",    "nombre": "Juan Cruz Acosta"},
    "admin2":  {"password": "stm2024", "rol": "operador", "nombre": "Operador STM"},
    # DEMO
    "demo":    {"password": "demo",    "rol": "operador", "nombre": "Usuario Demo"},
}

if "logueado" not in st.session_state:
    st.session_state.logueado = False
    st.session_state.usuario = None
    st.session_state.rol = None
    st.session_state.nombre_usuario = None

if not st.session_state.logueado:
    col1, col2, col3 = st.columns([1,1.4,1])
    with col2:
        st.markdown("""
        <div class="header-box" style="text-align:center; margin-top:60px;">
            <h1>🏛️ SindicalIA</h1>
            <p>Sindicato de Trabajadores Municipales — San Pedro</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("#### Acceso al sistema")
        usr = st.text_input("Usuario", placeholder="Ingresá tu usuario")
        pwd = st.text_input("Contraseña", type="password", placeholder="Contraseña")
        if st.button("Ingresar", use_container_width=True):
            if usr in USUARIOS and USUARIOS[usr]["password"] == pwd:
                st.session_state.logueado = True
                st.session_state.usuario = usr
                st.session_state.rol = USUARIOS[usr]["rol"]
                st.session_state.nombre_usuario = USUARIOS[usr]["nombre"]
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")
        st.caption("Demo: usuario `demo` / contraseña `demo`")
    st.stop()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"### 🏛️ SindicalIA")
    st.markdown(f"**STM San Pedro**")
    st.markdown("---")
    st.markdown(f"👤 **{st.session_state.nombre_usuario}**")
    st.caption(f"Rol: {st.session_state.rol.capitalize()}")
    st.markdown("---")

    opciones = ["📊 Panel General", "👥 Socios", "🛒 Proveeduría", "💰 Adelantos", "📋 Cierre Mensual"]
    if st.session_state.rol == "admin":
        opciones.append("⚙️ Configuración")

    seccion_actual = st.radio("Navegación", opciones, label_visibility="collapsed")
    st.markdown("---")
    if st.button("Cerrar sesión", use_container_width=True):
        st.session_state.logueado = False
        st.rerun()

# ── PANEL GENERAL ─────────────────────────────────────────────────────────────
if seccion_actual == "📊 Panel General":
    st.markdown("""
    <div class="header-box">
        <h1>📊 Panel General</h1>
        <p>Resumen operativo — Julio 2025</p>
    </div>
    """, unsafe_allow_html=True)

    # Métricas principales
    total_retiros = retiros["monto"].sum()
    total_adelantos = adelantos["monto"].sum()
    total_mes = total_retiros + total_adelantos
    socios_activos = socios[socios.activo == True].shape[0]
    stock_critico = mercaderia[mercaderia.stock <= 5].shape[0]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Socios activos</div>
            <div class="metric-value">{socios_activos}</div>
            <div class="metric-sub">de {socios.shape[0]} registrados</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card verde">
            <div class="metric-label">Retiros mercadería</div>
            <div class="metric-value">${total_retiros:,.0f}</div>
            <div class="metric-sub">este mes</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card naranja">
            <div class="metric-label">Adelantos en dinero</div>
            <div class="metric-value">${total_adelantos:,.0f}</div>
            <div class="metric-sub">este mes</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        color = "rojo" if stock_critico > 0 else "verde"
        st.markdown(f"""<div class="metric-card {color}">
            <div class="metric-label">Stock crítico</div>
            <div class="metric-value">{stock_critico}</div>
            <div class="metric-sub">productos bajo mínimo</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="seccion">⚠️ Alertas del mes</div>', unsafe_allow_html=True)

        # Socios cerca del límite
        alertas = []
        for _, s in socios[socios.activo].iterrows():
            deuda = deuda_socio(s["legajo"])
            pct = deuda / s["limite"] * 100 if s["limite"] > 0 else 0
            if pct >= 80:
                alertas.append((s["nombre"], pct, deuda, s["limite"]))

        if alertas:
            for nombre, pct, deuda, limite in alertas:
                clase = "alerta-roja" if pct >= 100 else "alerta"
                icono = "🔴" if pct >= 100 else "🟡"
                st.markdown(f"""<div class="{clase}">
                    {icono} <b>{nombre}</b> — utilizado {pct:.0f}% del límite
                    (${deuda:,.0f} de ${limite:,.0f})
                </div>""", unsafe_allow_html=True)
        else:
            st.success("Ningún socio supera el 80% de su límite.")

        if stock_critico > 0:
            criticos = mercaderia[mercaderia.stock <= 5]
            for _, p in criticos.iterrows():
                st.markdown(f"""<div class="alerta">
                    📦 Stock bajo: <b>{p['descripcion']}</b> — {p['stock']} unidades
                </div>""", unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="seccion">📦 Últimos movimientos</div>', unsafe_allow_html=True)
        ultimos = pd.concat([
            retiros[["fecha","socio","monto"]].assign(tipo="Mercadería"),
            adelantos[["fecha","socio","monto"]].assign(tipo="Adelanto")
        ]).sort_values("fecha", ascending=False).head(8)
        ultimos["monto"] = ultimos["monto"].apply(lambda x: f"${x:,.0f}")
        ultimos.columns = ["Fecha","Socio","Monto","Tipo"]
        st.dataframe(ultimos, use_container_width=True, hide_index=True)

# ── SOCIOS ────────────────────────────────────────────────────────────────────
elif seccion_actual == "👥 Socios":
    st.markdown("""
    <div class="header-box">
        <h1>👥 Socios</h1>
        <p>Gestión de afiliados y estado de cuenta</p>
    </div>
    """, unsafe_allow_html=True)

    buscar = st.text_input("🔍 Buscar socio (nombre o legajo)", placeholder="Ej: García o 001")

    df = socios.copy()
    if buscar:
        mask = df["nombre"].str.contains(buscar, case=False) | df["legajo"].str.contains(buscar)
        df = df[mask]

    # Agregar columnas calculadas
    df["deuda"] = df["legajo"].apply(deuda_socio)
    df["disponible"] = df["legajo"].apply(disponible_socio)
    df["uso_%"] = (df["deuda"] / df["limite"] * 100).round(1)

    def badge_estado(row):
        if not row["activo"]:
            return "Inactivo"
        if row["uso_%"] >= 100:
            return "🔴 Límite superado"
        if row["uso_%"] >= 80:
            return "🟡 Cerca del límite"
        return "🟢 Normal"

    df["estado"] = df.apply(badge_estado, axis=1)

    tabla = df[["legajo","nombre","area","limite","deuda","disponible","uso_%","estado"]].copy()
    tabla.columns = ["Legajo","Nombre","Área","Límite","Deuda","Disponible","Uso %","Estado"]
    tabla["Límite"]     = tabla["Límite"].apply(lambda x: f"${x:,.0f}")
    tabla["Deuda"]      = tabla["Deuda"].apply(lambda x: f"${x:,.0f}")
    tabla["Disponible"] = tabla["Disponible"].apply(lambda x: f"${x:,.0f}")

    st.dataframe(tabla, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown('<div class="seccion">📄 Detalle de socio</div>', unsafe_allow_html=True)

    socio_sel = st.selectbox("Seleccionar socio", socios["nombre"].tolist())
    leg = socios[socios["nombre"] == socio_sel]["legajo"].values[0]

    c1, c2, c3 = st.columns(3)
    deuda = deuda_socio(leg)
    lim = socios[socios.legajo == leg]["limite"].values[0]
    disp = lim - deuda
    pct = deuda / lim * 100

    with c1:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Límite asignado</div>
            <div class="metric-value">${lim:,.0f}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        color = "rojo" if pct >= 80 else "naranja" if pct >= 60 else "verde"
        st.markdown(f"""<div class="metric-card {color}">
            <div class="metric-label">Deuda actual ({pct:.0f}%)</div>
            <div class="metric-value">${deuda:,.0f}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card {'rojo' if disp < 0 else 'verde'}">
            <div class="metric-label">Disponible</div>
            <div class="metric-value">${disp:,.0f}</div>
        </div>""", unsafe_allow_html=True)

    col_ret, col_adel = st.columns(2)
    with col_ret:
        st.markdown("**Retiros de mercadería**")
        r = retiros[retiros.legajo == leg][["fecha","item","cantidad","monto"]]
        if r.empty:
            st.info("Sin retiros este mes.")
        else:
            r["monto"] = r["monto"].apply(lambda x: f"${x:,.0f}")
            r.columns = ["Fecha","Producto","Cant.","Monto"]
            st.dataframe(r, use_container_width=True, hide_index=True)

    with col_adel:
        st.markdown("**Adelantos en dinero**")
        a = adelantos[adelantos.legajo == leg][["fecha","monto","motivo"]]
        if a.empty:
            st.info("Sin adelantos este mes.")
        else:
            a["monto"] = a["monto"].apply(lambda x: f"${x:,.0f}")
            a.columns = ["Fecha","Monto","Motivo"]
            st.dataframe(a, use_container_width=True, hide_index=True)

# ── PROVEEDURÍA ───────────────────────────────────────────────────────────────
elif seccion_actual == "🛒 Proveeduría":
    st.markdown("""
    <div class="header-box">
        <h1>🛒 Proveeduría</h1>
        <p>Stock y registro de retiros</p>
    </div>
    """, unsafe_allow_html=True)

    col_stock, col_form = st.columns([1.2, 1])

    with col_stock:
        st.markdown('<div class="seccion">📦 Stock actual</div>', unsafe_allow_html=True)
        stock_view = mercaderia.copy()
        def badge_stock(s):
            if s <= 5:   return f"🔴 {s} (crítico)"
            if s <= 15:  return f"🟡 {s} (bajo)"
            return f"🟢 {s}"
        stock_view["stock_badge"] = stock_view["stock"].apply(badge_stock)
        stock_view["precio_fmt"] = stock_view["precio"].apply(lambda x: f"${x:,.0f}")
        st.dataframe(
            stock_view[["codigo","descripcion","stock_badge","precio_fmt"]].rename(
                columns={"codigo":"Código","descripcion":"Producto","stock_badge":"Stock","precio_fmt":"Precio"}),
            use_container_width=True, hide_index=True
        )

    with col_form:
        st.markdown('<div class="seccion">➕ Registrar retiro</div>', unsafe_allow_html=True)
        with st.form("form_retiro"):
            socio_r = st.selectbox("Socio", socios[socios.activo]["nombre"].tolist())
            producto_r = st.selectbox("Producto", mercaderia["descripcion"].tolist())
            cantidad_r = st.number_input("Cantidad", min_value=1, max_value=20, value=1)

            precio_unit = mercaderia[mercaderia.descripcion == producto_r]["precio"].values[0]
            monto_r = precio_unit * cantidad_r
            st.info(f"💵 Monto: **${monto_r:,.0f}**")

            leg_r = socios[socios.nombre == socio_r]["legajo"].values[0]
            disp_r = disponible_socio(leg_r)
            if monto_r > disp_r:
                st.warning(f"⚠️ Disponible: ${disp_r:,.0f} — supera el límite.")

            submitted = st.form_submit_button("✅ Registrar retiro", use_container_width=True)
            if submitted:
                if monto_r > disp_r:
                    st.error("No se puede registrar: supera el límite disponible.")
                else:
                    st.success(f"Retiro registrado: {socio_r} — {producto_r} x{cantidad_r} = ${monto_r:,.0f}")
                    st.caption("(En producción se guardaría en Google Sheets)")

    st.markdown("---")
    st.markdown('<div class="seccion">📋 Historial de retiros del mes</div>', unsafe_allow_html=True)
    hist = retiros.copy()
    hist["monto"] = hist["monto"].apply(lambda x: f"${x:,.0f}")
    hist.columns = ["Fecha","Legajo","Socio","Producto","Cantidad","Monto"]
    st.dataframe(hist[["Fecha","Socio","Producto","Cantidad","Monto"]], use_container_width=True, hide_index=True)

# ── ADELANTOS ─────────────────────────────────────────────────────────────────
elif seccion_actual == "💰 Adelantos":
    st.markdown("""
    <div class="header-box">
        <h1>💰 Adelantos en dinero</h1>
        <p>Registro y control de préstamos a socios</p>
    </div>
    """, unsafe_allow_html=True)

    col_form2, col_hist2 = st.columns([1, 1.3])

    with col_form2:
        st.markdown('<div class="seccion">➕ Registrar adelanto</div>', unsafe_allow_html=True)
        with st.form("form_adelanto"):
            socio_a = st.selectbox("Socio", socios[socios.activo]["nombre"].tolist())
            monto_a = st.number_input("Monto ($)", min_value=1000, max_value=100000, step=1000, value=10000)
            motivo_a = st.selectbox("Motivo", ["Gastos médicos","Urgencia familiar","Materiales escolares","Reparación del hogar","Otro"])
            fecha_a = st.date_input("Fecha", value=date.today())

            leg_a = socios[socios.nombre == socio_a]["legajo"].values[0]
            disp_a = disponible_socio(leg_a)
            st.info(f"Disponible del socio: **${disp_a:,.0f}**")

            sub_a = st.form_submit_button("✅ Registrar adelanto", use_container_width=True)
            if sub_a:
                if monto_a > disp_a:
                    st.error(f"Supera el límite disponible (${disp_a:,.0f})")
                else:
                    st.success(f"Adelanto registrado: {socio_a} — ${monto_a:,.0f}")
                    st.caption("(En producción se guardaría en Google Sheets)")

    with col_hist2:
        st.markdown('<div class="seccion">📋 Adelantos del mes</div>', unsafe_allow_html=True)
        adel_view = adelantos.copy()
        adel_view["monto"] = adel_view["monto"].apply(lambda x: f"${x:,.0f}")
        adel_view.columns = ["Fecha","Legajo","Socio","Monto","Motivo"]
        st.dataframe(adel_view[["Fecha","Socio","Monto","Motivo"]], use_container_width=True, hide_index=True)

        total_adel = adelantos["monto"].sum()
        st.markdown(f"""<div class="metric-card naranja" style="margin-top:12px;">
            <div class="metric-label">Total adelantado este mes</div>
            <div class="metric-value">${total_adel:,.0f}</div>
        </div>""", unsafe_allow_html=True)

# ── CIERRE MENSUAL ────────────────────────────────────────────────────────────
elif seccion_actual == "📋 Cierre Mensual":
    st.markdown("""
    <div class="header-box">
        <h1>📋 Cierre Mensual</h1>
        <p>Resumen de descuentos a liquidar por socio — Julio 2025</p>
    </div>
    """, unsafe_allow_html=True)

    st.info("Este resumen se entrega al área de liquidación de sueldos para aplicar los descuentos del mes.")

    cierre = []
    for _, s in socios[socios.activo].iterrows():
        ret = retiros[retiros.legajo == s["legajo"]]["monto"].sum()
        adel = adelantos[adelantos.legajo == s["legajo"]]["monto"].sum()
        total = ret + adel
        if total > 0:
            cierre.append({
                "Legajo": s["legajo"],
                "Nombre": s["nombre"],
                "Área": s["area"],
                "Mercadería": f"${ret:,.0f}",
                "Adelantos": f"${adel:,.0f}",
                "TOTAL A DESCONTAR": f"${total:,.0f}",
            })

    df_cierre = pd.DataFrame(cierre)
    st.dataframe(df_cierre, use_container_width=True, hide_index=True)

    total_general = retiros["monto"].sum() + adelantos["monto"].sum()
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Socios con descuento</div>
            <div class="metric-value">{len(cierre)}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card verde">
            <div class="metric-label">Total mercadería</div>
            <div class="metric-value">${retiros['monto'].sum():,.0f}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card naranja">
            <div class="metric-label">Total a descontar</div>
            <div class="metric-value">${total_general:,.0f}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("⬇️ Exportar para liquidación (CSV)", use_container_width=False):
        st.download_button(
            label="Descargar CSV",
            data=df_cierre.to_csv(index=False).encode("utf-8"),
            file_name=f"cierre_STM_julio2025.csv",
            mime="text/csv"
        )

# ── CONFIGURACIÓN ─────────────────────────────────────────────────────────────
elif seccion_actual == "⚙️ Configuración":
    st.markdown("""
    <div class="header-box">
        <h1>⚙️ Configuración</h1>
        <p>Solo disponible para administradores</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="seccion">👤 Usuarios del sistema</div>', unsafe_allow_html=True)
    df_usr = pd.DataFrame([
        {"Usuario": "mono",   "Nombre": "Juan Cruz Acosta", "Rol": "Administrador"},
        {"Usuario": "admin2", "Nombre": "Operador STM",     "Rol": "Operador"},
    ])
    st.dataframe(df_usr, use_container_width=True, hide_index=True)

    st.markdown('<div class="seccion">🔗 Conexión Google Sheets</div>', unsafe_allow_html=True)
    st.warning("⚠️ Modo demo activo — los datos no se guardan. La conexión a Google Sheets se configura al confirmar la implementación.")
    st.code("""# secrets.toml
[gcp_service_account]
type = "service_account"
project_id = "stm-san-pedro"
...

[sheets]
id = "ID_DEL_SPREADSHEET"
""", language="toml")
