import streamlit as st

# ----------------- CONFIG -----------------
st.set_page_config(page_title="Login - Tiendita", layout="centered")

# ----------------- ESTILOS (tu diseño Tailwind adaptado) -----------------
st.markdown("""
<style>
body {
    background-color: #024a86;
}
.login-box {
    background-color: #67e8f9;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

# ----------------- SESSION -----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ----------------- LOGIN UI -----------------
if not st.session_state.logged_in:

    st.markdown('<div class="login-box">', unsafe_allow_html=True)

    st.markdown("## 🔐 Iniciar Sesión")

    st.warning("⚠️ Usando credenciales de prueba (admin / password)")

    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Acceder"):
        if username == "admin" and password == "password":
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Acceso correcto")
            st.rerun()
        else:
            st.error("Credenciales incorrectas")

    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- DESPUÉS DEL LOGIN -----------------
else:
    st.success(f"Bienvenido {st.session_state.username}")

    if st.button("Cerrar sesión"):
        st.session_state.logged_in = False
        st.rerun()