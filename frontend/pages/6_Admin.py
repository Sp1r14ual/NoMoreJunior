import streamlit as st
import requests
import pandas as pd

# ────────────────────────────────────────────────
# Конфигурация
# ────────────────────────────────────────────────
API_BASE = "http://backend:8000"  # ← поменяй на реальный адрес

if "token" not in st.session_state or st.session_state.token is None:
    st.error("Необходим вход в систему")
    st.stop()

if not st.session_state.get("is_admin", False):
    st.error("Доступ разрешён только администраторам")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state.token}"}

st.title("Админ-панель")
st.markdown("Управление контентом тренажёра")

# ────────────────────────────────────────────────
# Вкладки
# ────────────────────────────────────────────────
tab_categories, tab_questions, tab_users = st.tabs(
    ["Категории", "Вопросы", "Пользователи"]
)

# ────────────────────────────────────────────────
# Вкладка 1: Категории
# ────────────────────────────────────────────────
with tab_categories:
    st.subheader("Список категорий")

    # Загрузка категорий
    try:
        r = requests.get(f"{API_BASE}/categories", headers=headers)
        r.raise_for_status()
        categories = r.json()

        if categories:
            df_cat = pd.DataFrame(categories)
            df_cat = df_cat.rename(columns={
                "id": "ID",
                "name": "Название",
                "description": "Описание"
            })
            st.dataframe(
                df_cat[["ID", "Название", "Описание"]],
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("Пока нет категорий")
    except Exception as e:
        st.error(f"Не удалось загрузить категории: {e}")

    # Форма добавления категории
    st.subheader("Добавить новую категорию")

    with st.form("add_category_form"):
        name = st.text_input("Название категории", key="cat_name")
        description = st.text_area("Описание (необязательно)", key="cat_desc")

        submitted = st.form_submit_button("Создать категорию", type="primary")

        if submitted:
            if not name.strip():
                st.error("Название категории обязательно")
            else:
                payload = {"name": name.strip(), "description": description.strip() or None}
                try:
                    r = requests.post(
                        f"{API_BASE}/admin/categories",
                        json=payload,
                        headers=headers
                    )
                    r.raise_for_status()
                    st.success(f"Категория «{name}» успешно добавлена!")
                    st.rerun()  # обновляем список
                except Exception as e:
                    st.error(f"Ошибка при создании категории: {r.text if 'r' in locals() else str(e)}")

# ────────────────────────────────────────────────
# Вкладка 2: Вопросы
# ────────────────────────────────────────────────
with tab_questions:
    st.subheader("Управление вопросами")

    # Выбор категории
    try:
        r_cat = requests.get(f"{API_BASE}/categories", headers=headers)
        categories_list = r_cat.json()
        category_options = {c["name"]: c["id"] for c in categories_list}
        
        selected_cat_name = st.selectbox(
            "Выберите категорию",
            options=["Все категории"] + list(category_options.keys()),
            index=0
        )
        
        cat_id = None if selected_cat_name == "Все категории" else category_options.get(selected_cat_name)
    except:
        st.error("Не удалось загрузить список категорий")
        cat_id = None

    # Загрузка вопросов
    params = {}
    if cat_id:
        params["category_id"] = cat_id

    try:
        r_q = requests.get(f"{API_BASE}/questions", params=params, headers=headers)
        questions = r_q.json()

        if questions:
            df_q = pd.DataFrame(questions)
            df_q = df_q.rename(columns={
                "id": "ID",
                "text": "Текст вопроса",
                "difficulty": "Сложность",
                "correct_option": "Правильный ответ"
            })
            
            # показываем только важные колонки
            display_cols = ["ID", "Текст вопроса", "Сложность", "Правильный ответ"]
            if "category_id" in df_q.columns:
                display_cols.append("category_id")
                
            st.dataframe(
                df_q[display_cols],
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Текст вопроса": st.column_config.TextColumn(width="large")
                }
            )
        else:
            st.info("В выбранной категории пока нет вопросов")
    except Exception as e:
        st.error(f"Ошибка загрузки вопросов: {e}")

    # Форма добавления вопроса
    st.subheader("Добавить новый вопрос")

    with st.form("add_question_form"):
        col1, col2 = st.columns([3, 1])
        with col1:
            q_text = st.text_area("Текст вопроса *", height=120)
        with col2:
            q_cat = st.selectbox("Категория *", options=list(category_options.keys()))
            q_diff = st.selectbox("Сложность", ["easy", "medium", "hard"], index=1)

        col_a, col_b = st.columns(2)
        with col_a:
            opt_a = st.text_input("Вариант A *")
            opt_c = st.text_input("Вариант C")
        with col_b:
            opt_b = st.text_input("Вариант B *")
            opt_d = st.text_input("Вариант D")

        correct_opt = st.radio("Правильный ответ *", ["A", "B", "C", "D"], horizontal=True)

        explanation = st.text_area("Пояснение / правильный ответ (необязательно)", height=100)

        submitted_q = st.form_submit_button("Добавить вопрос", type="primary")

        if submitted_q:
            if not all([q_text.strip(), opt_a.strip(), opt_b.strip(), q_cat]):
                st.error("Заполните обязательные поля")
            else:
                cat_id_selected = category_options[q_cat]
                payload = {
                    "category_id": cat_id_selected,
                    "text": q_text.strip(),
                    "option_a": opt_a.strip(),
                    "option_b": opt_b.strip(),
                    "option_c": opt_c.strip() or "",
                    "option_d": opt_d.strip() or "",
                    "correct_option": correct_opt,
                    "explanation": explanation.strip() or None,
                    "difficulty": q_diff
                }
                try:
                    r = requests.post(
                        f"{API_BASE}/admin/questions",
                        json=payload,
                        headers=headers
                    )
                    r.raise_for_status()
                    st.success("Вопрос успешно добавлен!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Ошибка: {r.text if 'r' in locals() else str(e)}")

# ────────────────────────────────────────────────
# Вкладка 3: Пользователи (просмотр)
# ────────────────────────────────────────────────
with tab_users:
    st.subheader("Список пользователей")

    try:
        # Предполагаем эндпоинт /admin/users
        r_users = requests.get(f"{API_BASE}/admin/users", headers=headers)
        users = r_users.json()

        if users:
            df_users = pd.DataFrame(users)
            df_users = df_users.rename(columns={
                "id": "ID",
                "username": "Имя пользователя",
                "email": "Email",
                "is_active": "Активен",
                "is_admin": "Админ",
                "created_at": "Создан"
            })
            st.dataframe(
                df_users[["ID", "Имя пользователя", "Email", "Активен", "Админ", "Создан"]],
                hide_index=True,
                use_container_width=True
            )
        else:
            st.info("Пользователи не найдены")
    except Exception as e:
        st.error(f"Не удалось загрузить список пользователей: {e}")
        st.info("Эндпоинт /admin/users пока не реализован на бэкенде?")