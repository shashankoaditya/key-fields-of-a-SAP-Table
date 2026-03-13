import streamlit as st
import pandas as pd
from openai import OpenAI

client = OpenAI()

st.set_page_config(layout="wide")

st.title("SAP Table Key Fields Finder")

col1, col2 = st.columns([3,1])

with col1:
    table_name = st.text_input("Enter SAP Table Name")

    if table_name:

        prompt = f"""
        Return the PRIMARY KEY fields of SAP table {table_name}.
        Provide output in JSON format with two columns:
        Field_Name
        Field_Label
        """

        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role":"system","content":"You are an SAP data dictionary expert"},
                {"role":"user","content":prompt}
            ]
        )

        output = response.choices[0].message.content
        st.write(output)

with col2:
    if table_name:

        usage = response.usage

        input_tokens = usage.prompt_tokens
        output_tokens = usage.completion_tokens
        total_tokens = usage.total_tokens

        # pricing example
        input_cost = input_tokens * 0.00000025
        output_cost = output_tokens * 0.0000005
        total_cost = input_cost + output_cost

        usd = round(total_cost,6)
        inr = round(total_cost * 83,4)

        st.subheader("Token Usage")
        st.write("Input Tokens:", input_tokens)
        st.write("Output Tokens:", output_tokens)
        st.write("Total Tokens:", total_tokens)

        st.subheader("Cost")
        st.write("USD:", usd)
        st.write("INR:", inr)
