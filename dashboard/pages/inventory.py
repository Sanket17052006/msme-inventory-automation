import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st
import pandas as pd
from api import get, post
from components.color_codes import stock_color

st.set_page_config(page_title="Inventory", layout="wide")
st.title("Inventory")

summary = get("/products/summary")
if summary:
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Products", summary.get("total_products", 0))
    c2.metric("Low Stock Items", summary.get("low_stock_count", 0))
    c3.metric("Total Stock (units)", summary.get("total_stock", 0))

tab1, tab2 = st.tabs(["All Products", "Low Stock"])

products_data = get("/products")
if not products_data:
    st.warning("No products found. Seed the database first.")
    st.stop()

df = pd.DataFrame(products_data)
df["status"] = df.apply(lambda r: stock_color(r["stock"], r["reorder_point"]), axis=1)

with tab1:
    col_order = ["id", "name", "sku", "stock", "reorder_point", "avg_daily_sales", "price", "status"]
    display = df[[c for c in col_order if c in df.columns]]
    st.dataframe(display, width="stretch", hide_index=True)

    st.subheader("Simulate Sale")
    col1, col2 = st.columns([3, 1])
    with col1:
        prod_name = st.selectbox("Product", df["name"].unique(), key="inv_sale_prod")
    with col2:
        sale_qty = st.number_input("Qty", min_value=1, value=1, key="inv_sale_qty")

    if st.button("Run Simulate Sale"):
        prod = df[df["name"] == prod_name].iloc[0]
        result = post(f"/products/{prod['id']}/simulate-sale", params={"qty": sale_qty})
        if result:
            st.success(f"Sold {sale_qty} × {prod_name}. New stock: {result['stock']}")
            st.rerun()

with tab2:
    low = df[df["stock"] < df["reorder_point"]]
    if low.empty:
        st.success("No low stock products!")
    else:
        low_display = low[[c for c in col_order if c in df.columns]]
        st.dataframe(low_display, width="stretch", hide_index=True)
