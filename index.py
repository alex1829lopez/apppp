import streamlit as st
import mysql.connector
import pandas as pd

# ----------------- DB -----------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="usr",
        password="usr",
        database="tiendita"
    )

# ----------------- ESTILO (similar a Tailwind) -----------------
st.set_page_config(page_title="Tiendita", layout="wide")

st.markdown("""
<style>
body {
    background-color: #f3f4f6;
}
.main-box {
    background-color: #fafafa;
    padding: 20px;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

# ----------------- LOGIN -----------------
if "login" not in st.session_state:
    st.session_state.login = False

if not st.session_state.login:
    st.title("🔐 Login")

    user = st.text_input("Usuario")
    pwd = st.text_input("Contraseña", type="password")

    if st.button("Entrar"):
        if user == "admin" and pwd == "password":
            st.session_state.login = True
            st.session_state.user = user
            st.rerun()
        else:
            st.error("Credenciales incorrectas")

    st.stop()

# ----------------- HEADER -----------------
col1, col2 = st.columns([3,1])

with col1:
    st.title("🛒 Sistema de Compras - Tiendita")

with col2:
    st.write(f"👤 {st.session_state.user}")
    if st.button("Cerrar sesión"):
        st.session_state.login = False
        st.rerun()

# ----------------- FUNCIONES -----------------
def get_data(query, params=None):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def execute(query, params):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    cursor.close()
    conn.close()

# ----------------- BUSCAR -----------------
st.subheader("🔍 Buscar compra")

search_id = st.number_input("ID compra", step=1)

if st.button("Buscar"):
    data = get_data("SELECT * FROM compras WHERE id_compra=%s", (search_id,))
    if data:
        st.success("Encontrado")
        st.dataframe(pd.DataFrame(data))
    else:
        st.warning("No encontrado")

# ----------------- FORMULARIO -----------------
st.subheader("➕ Registrar / Editar compra")

with st.form("form"):
    id_compra = st.number_input("ID", step=1)
    nombre = st.text_input("Nombre")
    marca = st.text_input("Marca")
    modelo = st.text_input("Modelo")
    presentacion = st.text_input("Presentación")
    proveedor = st.text_input("Proveedor")
    unitario = st.number_input("Costo", step=0.01)

    col1, col2 = st.columns(2)

    add = col1.form_submit_button("Agregar")
    update = col2.form_submit_button("Actualizar")

    if add:
        try:
            execute("""
            INSERT INTO compras VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (id_compra, nombre, marca, modelo, presentacion, proveedor, unitario))
            st.success("Compra agregada")
        except Exception as e:
            st.error(e)

    if update:
        try:
            execute("""
            UPDATE compras SET nombre=%s, marca=%s, modelo=%s,
            presentacion=%s, proveedor=%s, unitario=%s
            WHERE id_compra=%s
            """, (nombre, marca, modelo, presentacion, proveedor, unitario, id_compra))
            st.success("Actualizado")
        except Exception as e:
            st.error(e)

# ----------------- TABLA -----------------
st.subheader("📋 Historial de compras")

data = get_data("SELECT * FROM compras ORDER BY id_compra DESC")

if data:
    df = pd.DataFrame(data)

    st.dataframe(df)

    st.subheader("🗑️ Eliminar")

    delete_id = st.number_input("ID a eliminar", step=1, key="delete")

    if st.button("Eliminar"):
        execute("DELETE FROM compras WHERE id_compra=%s", (delete_id,))
        st.success("Eliminado")
else:
    st.info("No hay registros")