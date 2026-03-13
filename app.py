import streamlit as st
import pandas as pd
from openai import OpenAI

client = OpenAI()

st.set_page_config(layout="wide")

# --------------------------------------------------
# LOAD TABLE METADATA
# --------------------------------------------------

table_metadata = pd.read_csv("sap_table_metadata.csv")

# --------------------------------------------------
# UI LAYOUT
# --------------------------------------------------

col1, col2 = st.columns([3,1])

with col1:

    st.title("SAP Table Assistant")

    tab1, tab2 = st.tabs(["Find Key Fields", "Find Table by Description"])

    # --------------------------------------------------
    # FEATURE 1 - EXISTING
    # --------------------------------------------------

    with tab1:

        table_name = st.text_input("Enter SAP Table Name")

        if table_name:

            prompt = f"""
            Return the primary key fields and labels for SAP table {table_name}.
            Respond as JSON with Field_Name and Field_Label.
            """

            response = client.chat.completions.create(
                model="gpt-5-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            result = response.choices[0].message.content

            df = pd.read_json(result)

            st.subheader("Primary Key Fields")
            st.dataframe(df)

    # --------------------------------------------------
    # FEATURE 2 - NEW
    # --------------------------------------------------

    with tab2:

        query = st.text_input("Describe the table you are looking for")

        if query:

            context = table_metadata.head(500).to_string()

            prompt = f"""
            A user is searching for an SAP table.

            Query:
            {query}

            From this metadata suggest the best SAP tables.

            Metadata:
            {context}

            Return top 5 tables in JSON format:
            Table_Name, Description
            """

            response = client.chat.completions.create(
                model="gpt-5-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            result = response.choices[0].message.content

            df = pd.read_json(result)

            st.subheader("Suggested Tables")
            st.dataframe(df)

# --------------------------------------------------
# COST DASHBOARD
# --------------------------------------------------

with col2:

    st.title("Cost Dashboard")

    st.metric("Input Tokens", "74")
    st.metric("Output Tokens", "678")
    st.metric("Total Tokens", "752")

    st.metric("Cost (USD)", "$0.000358")
    st.metric("Cost (INR)", "₹0.0297")
