import requests
import streamlit as st
from typing import Any


def _base() -> str:
    if "api_url" not in st.session_state:
        st.session_state.api_url = "http://localhost:8000"
    return st.session_state.api_url


def get(path: str) -> Any | None:
    try:
        resp = requests.get(f"{_base()}{path}", timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"GET {path} failed: {e}")
        return None


def post(path: str, json: dict | None = None, params: dict | None = None) -> Any | None:
    try:
        resp = requests.post(f"{_base()}{path}", json=json, params=params, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"POST {path} failed: {e}")
        return None


def patch(path: str, json: dict | None = None) -> Any | None:
    try:
        resp = requests.patch(f"{_base()}{path}", json=json, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"PATCH {path} failed: {e}")
        return None
