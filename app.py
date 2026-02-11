import streamlit as st
import pandas as pd
import sqlite3
import tempfile

st.set_page_config(page_title="SmartSupply", page_icon="📦", layout="wide")
st.title("📦 SmartSupply - Inventory System")

db_path = tempfile.gettempdir() + "/inventory.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL, stock INTEGER)")
c.execute("CREATE TABLE IF NOT EXISTS sales (id INTEGER PRIMARY KEY, product_id INTEGER, quantity INTEGER, total REAL)")
conn.commit()

menu = st.sidebar.radio("Menu", ["Products", "Sales", "Reports"])

if menu == "Products":
    with st.form("add"):
        name = st.text_input("Product Name")
        price = st.number_input("Price", 0.0)
        stock = st.number_input("Stock", 0)
        if st.form_submit_button("Add"):
            c.execute("INSERT INTO products (name, price, stock) VALUES (?,?,?)", (name, price, stock))
            conn.commit()
    df = pd.read_sql("SELECT * FROM products", conn)
    st.dataframe(df)

elif menu == "Sales":
    df = pd.read_sql("SELECT * FROM products WHERE stock>0", conn)
    if len(df) > 0:
        prod = st.selectbox("Product", df["name"])
        p = df[df["name"]==prod].iloc[0]        P = DF[DF["name"]==provid].iLock[0]
        qty = st.number_input("Quantity", 1, int(p["stock"]))
        if st.button("Sell"):
            total = p["price"] * qty
            c.execute("INSERT INTO sales (product_id, quantity, total) VALUES (?,?,?)", (p["id"], qty, total))
            c.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (qty, p["id"]))
            conn.commit()

elif menu == "Reports":
    df = pd.read_sql("SELECT SUM(total) as total FROM sales", conn)
    st.metric("Total Revenue", f"₹{df['total'].iloc[0] if not df.empty else 0:.2f}")
    df2 = pd.read_sql("SELECT p.name, SUM(s.quantity) as qty, SUM(s.total) as revenue FROM sales s JOIN products p ON s.product_id=p.id GROUP BY p.name", conn)
    if len(df2) > 0:
        st.dataframe(df2)
        st.bar_chart(df2.set_index("name")["revenue"])

conn.close()
