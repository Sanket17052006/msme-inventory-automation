import streamlit as st
import pandas as pd
import plotly.express as px
from api import get

st.set_page_config(page_title="Analytics", layout="wide")
st.title("Analytics")

summary = get("/analytics/summary")
if summary:
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Products", summary.get("total_products", 0))
    c2.metric("Total Stock", summary.get("total_stock", 0))
    c3.metric("Low Stock Items", summary.get("low_stock_count", 0))
    c4.metric("Total Orders", summary.get("total_orders", 0))
    c5.metric("Pending Orders", summary.get("pending_orders", 0))

st.subheader("Sales Trends")
sales = get("/sales-log")
if sales:
    df = pd.DataFrame(sales)

    products = get("/products")
    prod_map = {}
    if products:
        prod_map = {p["id"]: p["name"] for p in products}
        df["product_name"] = df["product_id"].map(prod_map)

    fig = px.line(df, x="sale_date", y="qty_sold", color="product_name",
                  title="Daily Sales by Product")
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Raw Sales Log"):
        st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No sales data. Use 'Simulate Sale' on the Inventory page to generate sales.")

st.subheader("Suppliers")
suppliers = get("/suppliers")
if suppliers:
    sdf = pd.DataFrame(suppliers)
    st.dataframe(sdf, use_container_width=True, hide_index=True)
else:
    st.info("No suppliers found.")

st.subheader("Product Performance")
products = get("/products")
if products:
    pdf = pd.DataFrame(products)
    if "price" in pdf.columns and "stock" in pdf.columns:
        pdf["stock_value"] = pdf["price"] * pdf["stock"]
        pdf = pdf.sort_values("stock_value", ascending=False)
        fig2 = px.bar(pdf, x="name", y="stock_value", title="Stock Value by Product (₹)")
        st.plotly_chart(fig2, use_container_width=True)
