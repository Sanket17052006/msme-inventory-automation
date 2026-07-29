import streamlit as st

st.set_page_config(page_title="MSME Supply Chain", layout="wide")

api_url = st.sidebar.text_input("API URL", "http://localhost:8000", key="api_url_input")
st.session_state.api_url = api_url

st.sidebar.success("Select a page above.")

st.title("MSME Inventory Dashboard")

st.markdown("""
### Welcome to the MSME Inventory Dashboard

Monitor your inventory, track orders, and view analytics in real time.

**Quick actions:**
- **Inventory** — View all products with color-coded stock levels, simulate sales
- **Orders** — Track order status, confirm/reject pending orders, create new orders
- **Analytics** — Summary metrics, sales trends chart, supplier comparison, stock valuation

**Setup:** Make sure the backend API is running and enter its URL in the sidebar.
""")
