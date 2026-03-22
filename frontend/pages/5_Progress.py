import streamlit as st
import requests
import pandas as pd

API_BASE = "http://localhost:8000"

st.title("Мой прогресс")

headers = {"Authorization": f"Bearer {st.session_state.token}"}

try:
    r = requests.get(f"{API_BASE}/progress/me", headers=headers)
    progress = r.json()
    
    if not progress:
        st.info("У вас пока нет прогресса. Начните тренировку!")
    else:
        df = pd.DataFrame(progress)
        df["accuracy"] = (df["score"] / df["total_questions"] * 100).round(1).astype(str) + " %"
        # df = df[["category_id", "score", "total_questions", "accuracy", "last_updated"]]
        df = df[["category_id", "score", "total_questions", "accuracy"]]
        st.dataframe(df.style.format(precision=1), use_container_width=True)
except Exception as e:
    st.error(f"Не удалось загрузить прогресс: {e}")