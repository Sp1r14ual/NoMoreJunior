import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.title("Вход")

with st.form("login_form"):
    username = st.text_input("Имя пользователя", placeholder="alice")
    password = st.text_input("Пароль", type="password")
    submit = st.form_submit_button("Войти", type="primary")

    if submit:
        try:
            r = requests.post(
                f"{st.session_state.get('API_BASE', 'http://localhost:8000')}/auth/token",
                data={"username": username, "password": password}
            )
            r.raise_for_status()
            data = r.json()
            st.session_state.token = data["access_token"]
            
            # Получаем информацию о пользователе
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            user_r = requests.get(f"{API_BASE}/auth/me", headers=headers)
            if user_r.ok:
                st.session_state.user = user_r.json()
                st.session_state.is_admin = st.session_state.user.get("is_admin", False)
            
            st.success("Успешный вход!")
            st.rerun()
        except Exception as e:
            st.error(f"Ошибка входа: {e}")