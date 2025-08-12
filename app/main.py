# app/main.py
import streamlit as st
from query_engine import get_results_for_question

st.set_page_config(page_title="TalkToMyDB — Sakila", layout="wide")
st.title("TalkToMyDB — Sakila (Groq LLM)")

q = st.text_input("Ask a question in plain English about the database:", value="")
if st.button("Ask") and q.strip():
    with st.spinner("Thinking..."):
        res = get_results_for_question(q)
    if res.get("error"):
        st.error(res["error"])
        st.code(res.get("sql", ""))
    else:
        st.subheader("Generated SQL")
        st.code(res["sql"])
        st.subheader("Results")
        import pandas as pd
        df = pd.DataFrame(res["rows"], columns=res["columns"])
        st.dataframe(df)
