import streamlit as st

st.title("SAP Key Fields Finder")

table = st.text_input("Enter SAP Table Name")

if table:
    st.write(f"You entered table: {table}")
