import streamlit as st
import requests

API_BASE = st.sidebar.text_input("API URL", "http://localhost:8000")

st.set_page_config(page_title="MSME Supply Chain", layout="wide")
st.title("📦 MSME Inventory Dashboard")


def api(path: str) -> dict | list | None:
    try:
        resp = requests.get(f"{API_BASE}{path}", timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"API error: {e}")
        return None
