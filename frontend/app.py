import streamlit as st
import requests

st.set_page_config(
    page_title="NoMoreJunior — тренажёр для джунов",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Инициализация сессии
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# Боковая панель
st.sidebar.title("NoMoreJunior")

if st.session_state.token:
    st.sidebar.success(f"Привет, {st.session_state.user.get('username', 'Пользователь')}")
    
    st.sidebar.page_link("pages/3_Categories.py", label="Категории", icon="📚")
    st.sidebar.page_link("pages/4_Training.py", label="Тренажёр", icon="⚡")
    st.sidebar.page_link("pages/5_Progress.py", label="Мой прогресс", icon="📊")
    
    if st.session_state.is_admin:
        st.sidebar.page_link("pages/6_Admin.py", label="Админ-панель", icon="🔧")
    
    if st.sidebar.button("Выйти", type="primary"):
        st.session_state.token = None
        st.session_state.user = None
        st.session_state.is_admin = False
        st.rerun()
else:
    st.sidebar.page_link("pages/1_Login.py", label="Вход", icon="🔑")
    st.sidebar.page_link("pages/2_Register.py", label="Регистрация", icon="✍️")

# Главный контент на главной странице
if not st.session_state.token:
    st.title("🚀 NoMoreJunior")
    st.markdown("""
    Тренажёр для junior-разработчиков и студентов IT-направлений  
    Практикуйся в реальных задачах, получай обратную связь и отслеживай прогресс.
    
    **Войди или зарегистрируйся**, чтобы начать!
    """)
else:
    st.title(f"Добро пожаловать, {st.session_state.user['username']}! 👋")
    st.markdown("Выбери раздел в боковом меню чтобы начать тренировку.")