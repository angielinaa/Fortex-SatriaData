import streamlit as st

st.set_page_config(page_title="Fortex | Login", page_icon="🛡️", layout="centered")

if "role" not in st.session_state:
    st.session_state.role = None

def login():
    st.title("🔐 Gerbang Akses Fortex")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Masuk", use_container_width=True)

        if submit:
            if username == "admin" and password == "rahasia":
                st.session_state.role = "admin"
                st.rerun()
            elif username == "warga" and password == "123":
                st.session_state.role = "user"
                st.rerun()
            else:
                st.error("Kredensial salah! Gunakan admin/rahasia atau warga/123.")

def logout():
    st.session_state.role = None
    st.rerun()

admin_page = st.Page("pages/1_Dashboard_Admin.py", title="Dashboard Admin", icon="🗺️")
user_page = st.Page("pages/2_Safe_Space.py", title="Lapor Anonim", icon="🚨")

if st.session_state.role is None:
    login()
else:
    st.sidebar.button("Keluar (Logout)", on_click=logout, use_container_width=True)

    if st.session_state.role == "admin":
        st.sidebar.success("Sesi: Administrator")
        pg = st.navigation([admin_page])
    elif st.session_state.role == "user":
        st.sidebar.info("Sesi: Warga Sipil")
        pg = st.navigation([user_page])

    pg.run()
