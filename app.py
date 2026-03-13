import streamlit as st
import pandas as pd
from openai import OpenAI
import json

client = OpenAI()

st.set_page_config(page_title="SAP Key Field Assistant", layout="wide")

st.title("🔑 SAP Key Field Assistant")

left, right = st.columns([3,1])

with left:

    st.subheader("Enter SAP Table Name")

    table = st.text_input("Table Name")

    if table:

        prompt = f"""
        Return the PRIMARY KEY fields of SAP table {table}.
        Respond ONLY in JSON format like:

        [
        {{"Field_Name":"MANDT","Field_Label":"Client"}},
        {{"Field_Name":"VBELN","Field_Label":"Sales Document"}}
        ]
        """

        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {"role":"system","content":"You are an SAP Data Dictionary expert."},
                {"role":"user","content":prompt}
            ]
        )

        result = response.choices[0].message.content

        try:
            data = json.loads(result)
            df = pd.DataFrame(data)

            st.subheader("Primary Key Fields")
            st.dataframe(df, use_container_width=True)

        except:
            st.write(result)

with right:

    st.subheader("📊 Cost Dashboard")

    if table:

        usage = response.usage

        input_tokens = usage.prompt_tokens
        output_tokens = usage.completion_tokens
        total_tokens = usage.total_tokens

        st.metric("Input Tokens", input_tokens)
        st.metric("Output Tokens", output_tokens)
        st.metric("Total Tokens", total_tokens)

        # GPT-5 mini pricing example
        input_cost = input_tokens * 0.00000025
        output_cost = output_tokens * 0.0000005
        total_cost = input_cost + output_cost

        usd = round(total_cost,6)
        inr = round(total_cost * 83,4)

        st.divider()

        st.metric("Cost (USD)", f"${usd}")
        st.metric("Cost (INR)", f"₹{inr}")
