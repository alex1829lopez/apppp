import streamlit as st
import mysql.connector

# ----------------- CONFIG -----------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="usr",
        password="usr",
        database="tiendita"
    )

# ----------------- LOGIN -----------------
def login():
    st.title("🔐 Login")

    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Iniciar sesión"):
        if username == "admin" and password == "password":
            st.session_state.logged_in = True
            st.success("Sesión iniciada")
            st.rerun()
        else:
            st.error("Credenciales incorrectas")

# ----------------- CRUD -----------------

def ver_compras():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM compras ORDER BY id_compra DESC")
    data = cursor.fetchall()

    st.subheader("📋 Lista de compras")
    st.dataframe(data)

    cursor.close()
    conn.close()


def agregar_compra():
    st.subheader("➕ Agregar compra")

    with st.form("form_add"):
        id_compra = st.number_input("ID", step=1)
        nombre = st.text_input("Nombre")
        marca = st.text_input("Marca")
        modelo = st.text_input("Modelo")
        presentacion = st.text_input("Presentación")
        proveedor = st.text_input("Proveedor")
        unitario = st.number_input("Costo unitario")

        submit = st.form_submit_button("Guardar")

        if submit:
            try:
                conn = get_connection()
                cursor = conn.cursor()

                query = """
                INSERT INTO compras VALUES (%s,%s,%s,%s,%s,%s,%s)
                """
                cursor.execute(query, (id_compra, nombre, marca, modelo, presentacion, proveedor, unitario))
                conn.commit()

                st.success("Compra agregada")

                cursor.close()
                conn.close()

            except Exception as e:
                st.error(f"Error: {e}")


def editar_compra():
    st.subheader("✏️ Editar compra")

    id_buscar = st.number_input("ID a editar", step=1)

    if st.button("Cargar"):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM compras WHERE id_compra=%s", (id_buscar,))
        data = cursor.fetchone()

        cursor.close()
        conn.close()

        if data:
            st.session_state.edit_data = data
        else:
            st.warning("No encontrado")

    if "edit_data" in st.session_state:
        data = st.session_state.edit_data

        nombre = st.text_input("Nombre", data["nombre"])
        marca = st.text_input("Marca", data["marca"])
        modelo = st.text_input("Modelo", data["modelo"])
        presentacion = st.text_input("Presentación", data["presentacion"])
        proveedor = st.text_input("Proveedor", data["proveedor"])
        unitario = st.number_input("Costo", value=float(data["unitario"]))

        if st.button("Actualizar"):
            conn = get_connection()
            cursor = conn.cursor()

            query = """
            UPDATE compras SET nombre=%s, marca=%s, modelo=%s,
            presentacion=%s, proveedor=%s, unitario=%s
            WHERE id_compra=%s
            """

            cursor.execute(query, (nombre, marca, modelo, presentacion, proveedor, unitario, data["id_compra"]))
            conn.commit()

            cursor.close()
            conn.close()

            st.success("Actualizado")
            del st.session_state.edit_data


def eliminar_compra():
    st.subheader("🗑️ Eliminar compra")

    id_delete = st.number_input("ID a eliminar", step=1)

    if st.button("Eliminar"):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM compras WHERE id_compra=%s", (id_delete,))
        conn.commit()

        cursor.close()
        conn.close()

        st.success("Eliminado")


def buscar_compra():
    st.subheader("🔍 Buscar compra")

    id_buscar = st.number_input("ID a buscar", step=1)

    if st.button("Buscar"):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM compras WHERE id_compra=%s", (id_buscar,))
        data = cursor.fetchall()

        cursor.close()
        conn.close()

        if data:
            st.dataframe(data)
        else:
            st.warning("No encontrado")


# ----------------- APP -----------------

def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login()
        return

    st.sidebar.title("Menú")
    opcion = st.sidebar.radio("Ir a", [
        "Ver",
        "Agregar",
        "Editar",
        "Eliminar",
        "Buscar",
        "Cerrar sesión"
    ])

    if opcion == "Ver":
        ver_compras()
    elif opcion == "Agregar":
        agregar_compra()
    elif opcion == "Editar":
        editar_compra()
    elif opcion == "Eliminar":
        eliminar_compra()
    elif opcion == "Buscar":
        buscar_compra()
    elif opcion == "Cerrar sesión":
        st.session_state.logged_in = False
        st.rerun()


if __name__ == "__main__":
    main()