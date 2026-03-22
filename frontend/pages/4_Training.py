import streamlit as st
import requests
import random

API_BASE = "http://backend:8000"

st.title("Тренажёр")

if "selected_category" not in st.session_state:
    st.warning("Сначала выберите категорию")
    st.page_link("pages/3_Categories.py", label="← Вернуться к категориям")
    st.stop()

cat = st.session_state.selected_category
st.subheader(f"Категория: {cat['name']}")

if "questions" not in st.session_state or st.button("Обновить вопросы"):
    try:
        r = requests.get(
            f"{API_BASE}/questions/random",
            params={"category_id": cat["id"], "count": 10},
            headers={"Authorization": f"Bearer {st.session_state.token}"}
        )
        st.session_state.questions = r.json()
        st.session_state.current_idx = 0
        st.session_state.answers = {}
    except Exception as e:
        st.error(f"Ошибка загрузки вопросов: {e}")
        st.stop()

questions = st.session_state.questions
idx = st.session_state.current_idx

if idx >= len(questions):
    st.success("Тренировка завершена!")
    if st.button("Начать заново"):
        st.session_state.current_idx = 0
        st.rerun()
    st.page_link("pages/3_Categories.py", label="Выбрать другую категорию")
    st.stop()

q = questions[idx]
st.markdown(f"**Вопрос {idx+1}/{len(questions)}**")
st.write(q["text"])

options = ["A", "B", "C", "D"]
choices = [q["option_a"], q["option_b"], q["option_c"], q["option_d"]]

selected = st.radio(
    "Выберите вариант ответа",
    options=options,
    format_func=lambda x: f"{x}) {choices[options.index(x)]}",
    key=f"q_{q['id']}"
)

col1, col2 = st.columns([1,4])

with col1:
    if st.button("→ Следующий", disabled=idx >= len(questions)-1):
        # Отправляем ответ на бэкенд
        try:
            requests.post(
                f"{API_BASE}/progress/submit-answer",
                json={"question_id": q["id"], "selected_option": selected},
                headers={"Authorization": f"Bearer {st.session_state.token}"}
            )
        except:
            pass  # silent fail для прототипа
        
        st.session_state.current_idx += 1
        st.rerun()

with col2:
    if st.button("Завершить тренировку"):
        st.session_state.current_idx = len(questions)
        st.rerun()