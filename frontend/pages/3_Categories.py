import streamlit as st
import requests

API_BASE = "http://backend:8000"

st.title("Категории")

headers = {"Authorization": f"Bearer {st.session_state.token}"}

try:
    r = requests.get(f"{API_BASE}/categories", headers=headers)
    categories = r.json()
    
    cols = st.columns(2)
    for i, cat in enumerate(categories):
        with cols[i % 2]:
            with st.container(border=True):
                st.subheader(cat["name"])
                st.caption(cat.get("description", ""))
                if st.button("Начать тренировку", key=f"start_{cat['id']}"):
                    st.session_state.selected_category = cat
                    st.switch_page("pages/4_Training.py")
except Exception as e:
    st.error(f"Не удалось загрузить категории: {e}")