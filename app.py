import streamlit as st
import pandas as pd
from openai import OpenAI

# Initialize OpenAI
client = OpenAI()

st.set_page_config(layout="wide")

# Layout
left_col, right_col = st.columns([3,1])

# ---------------------------
# MAIN APPLICATION
# ---------------------------

with left_col:

    st.title("SAP Table Assistant")

    tab1, tab2 = st.tabs(["Find Key Fields", "Find Table by Description"])

    # ----------------------------------
    # FEATURE 1
    # ENTER TABLE → GET KEY FIELDS
    # ----------------------------------

    with tab1:

        table_name = st.text_input("Enter SAP Table Name")

        if table_name:

            prompt = f"""
You are an SAP expert.

Return the PRIMARY KEY fields of SAP table {table_name}.

Return ONLY JSON in this format:

[
{{"Field_Name":"MANDT","Field_Label":"Client"}},
{{"Field_Name":"VEHICLE","Field_Label":"Vehicle"}}
]
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            result = response.choices[0].message.content

            try:
                df = pd.read_json(result)
                st.subheader("Primary Key Fields")
                st.dataframe(df)
            except:
                st.write(result)

    # ----------------------------------
    # FEATURE 2
    # NATURAL LANGUAGE → TABLE NAME
    # ----------------------------------

    with tab2:

        query = st.text_input("Describe the SAP table you are searching for")

        if query:

            prompt = f"""
You are an SAP consultant expert.

A user is searching for an SAP table.

User request:
{query}

Suggest the most likely SAP tables.

Return ONLY JSON in this format:

[
{{"Table_Name":"VLCVEHICLE","Description":"Vehicle Master"}},
{{"Table_Name":"VLCSTATUS","Description":"Vehicle Status"}},
{{"Table_Name":"VLCASSIGN","Description":"Vehicle Assignment"}}
]
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            result = response.choices[0].message.content

            try:
                df = pd.read_json(result)
                st.subheader("Suggested Tables")
                st.dataframe(df)
            except:
                st.write(result)


# ---------------------------
# COST DASHBOARD
# ---------------------------

with right_col:

    st.title("📊 Cost Dashboard")

    st.metric("Input Tokens", "Auto")
    st.metric("Output Tokens", "Auto")
    st.metric("Total Tokens", "Auto")

    st.metric("Cost (USD)", "Low")
    st.metric("Cost (INR)", "Low")
