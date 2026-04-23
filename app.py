"""
app.py
======
Entry point chạy Streamlit dashboard (nếu nhóm làm phần demo interactive).

Cách chạy:
    streamlit run app.py

Dashboard bao gồm:
    - Tab 1: EDA & Visualizations (Phần 2)
    - Tab 2: Revenue Forecast (Phần 3)

Yêu cầu: cài đặt môi trường từ requirements.txt hoặc environment.yml trước.
"""

import streamlit as st
from src.ui_builder.dashboard import build_dashboard

st.set_page_config(page_title="Datathon 2026 — The Gridbreakers", layout="wide")

if __name__ == "__main__":
    build_dashboard()
