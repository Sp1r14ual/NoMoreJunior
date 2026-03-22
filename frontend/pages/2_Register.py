import streamlit as st
import requests

API_BASE = "http://backend:8000"

st.title("Регистрация")

with st.form("register_form"):
    email = st.text_input("Email")
    username = st.text_input("Имя пользователя")
    password = st.text_input("Пароль", type="password")
    password2 = st.text_input("Повторите пароль", type="password")
    
    submit = st.form_submit_button("Зарегистрироваться", type="primary")

    if submit:
        if password != password2:
            st.error("Пароли не совпадают")
        elif not all([email, username, password]):
            st.error("Заполните все поля")
        else:
            try:
                r = requests.post(
                    f"{API_BASE}/auth/register",
                    json={
                        "email": email,
                        "username": username,
                        "password": password
                    }
                )
                r.raise_for_status()
                st.success("Регистрация прошла успешно! Теперь можно войти.")
                st.page_link("pages/1_Login.py", label="→ Перейти ко входу", icon="🔑")
            except Exception as e:
                st.error(f"Ошибка регистрации: {r.text if 'r' in locals() else e}")