import streamlit as st
import pandas as pd
from api import get, post, patch

st.set_page_config(page_title="Orders", layout="wide")
st.title("Orders")

analytics = get("/analytics/summary")
if analytics:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Orders", analytics.get("total_orders", 0))
    c2.metric("Pending", analytics.get("pending_orders", 0))
    c3.metric("Confirmed", analytics.get("confirmed_orders", 0))
    c4.metric("Fulfilled", analytics.get("fulfilled_orders", 0))

status_filter = st.selectbox("Filter by status", ["all", "pending", "confirmed", "rejected", "fulfilled"])
orders_data = get(f"/orders{'?status=' + status_filter if status_filter != 'all' else ''}")

if orders_data:
    df = pd.DataFrame(orders_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

    for _, row in df.iterrows():
        if row["status"] == "pending":
            cols = st.columns([6, 1, 1])
            cols[0].write(f"**#{row['id']}** — Product #{row['product_id']}, Qty: {row['qty']}")
            if cols[1].button("Confirm", key=f"confirm_{row['id']}"):
                result = patch(f"/orders/{row['id']}/status", json={"status": "confirmed"})
                if result:
                    st.success(f"Order #{row['id']} confirmed!")
                    st.rerun()
            if cols[2].button("Reject", key=f"reject_{row['id']}"):
                result = patch(f"/orders/{row['id']}/status", json={"status": "rejected"})
                if result:
                    st.success(f"Order #{row['id']} rejected.")
                    st.rerun()
else:
    st.info("No orders found.")

st.divider()
st.subheader("Create New Order")
products = get("/products")
suppliers = get("/suppliers")

if products and suppliers:
    prod_map = {p["name"]: p["id"] for p in products}
    supp_map = {s["name"]: s["id"] for s in suppliers}

    with st.form("create_order"):
        prod_name = st.selectbox("Product", list(prod_map.keys()))
        qty = st.number_input("Quantity", min_value=1, value=1)
        supp_name = st.selectbox("Supplier", list(supp_map.keys()))
        submitted = st.form_submit_button("Create Order")
        if submitted:
            result = post("/orders", json={
                "product_id": prod_map[prod_name],
                "qty": qty,
                "supplier_id": supp_map[supp_name],
            })
            if result:
                st.success(f"Order #{result['id']} created!")
                st.rerun()
