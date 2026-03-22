import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.title("Админ-панель")

if not st.session_state.is_admin:
    st.error("Доступ запрещён. Только для администраторов.")
    st.stop()

tab1, tab2 = st.tabs(["Добавить вопрос", "Управление категориями"])

with tab1:
    with st.form("add_question"):
        category_id = st.number_input("ID категории", min_value=1, step=1)
        text = st.text_area("Текст вопроса")
        opt_a = st.text_input("Вариант A")
        opt_b = st.text_input("Вариант B")
        opt_c = st.text_input("Вариант C")
        opt_d = st.text_input("Вариант D")
        correct = st.selectbox("Правильный ответ", ["A", "B", "C", "D"])
        explanation = st.text_area("Пояснение (опционально)")
        
        submitted = st.form_submit_button("Добавить вопрос")
        
        if submitted:
            payload = {
                "category_id": category_id,
                "text": text,
                "option_a": opt_a,
                "option_b": opt_b,
                "option_c": opt_c,
                "option_d": opt_d,
                "correct_option": correct,
                "explanation": explanation or None
            }
            try:
                r = requests.post(
                    f"{API_BASE}/admin/questions",
                    json=payload,
                    headers={"Authorization": f"Bearer {st.session_state.token}"}
                )
                r.raise_for_status()
                st.success("Вопрос добавлен!")
            except Exception as e:
                st.error(f"Ошибка: {e}")

with tab2:
    st.info("Здесь можно добавить функционал создания/редактирования категорий (по аналогии)")