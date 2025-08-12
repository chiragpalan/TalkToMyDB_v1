import streamlit as st
from app.query_simple import run_nl_query
import os

# Page config
st.set_page_config(page_title="Talk to My DB", page_icon="💬", layout="wide")

st.title("💬 Talk to My Database")

# Instructions
st.markdown("""
**Welcome to the AI-powered Database Query App!**  
This application connects to the Sakila SQLite database and allows you to ask **questions in plain English**.  
The database schema is shown below in the ERD diagram for reference.  
You can type your own questions or try some of these examples:

- "Show me all actors in the database"
- "List the top 5 films by rental count"
- "Which customers live in California?"
- "Give me the total payments per customer"

💡 *Tip:* The AI will translate your question into SQL and fetch the results directly from the database.
""")

# Show ERD diagram
erd_path = os.path.join("data", "SQLite3 Sakila Sample Database ERD.png")
if os.path.exists(erd_path):
    st.subheader("📊 Database ERD Diagram")
    st.image(erd_path, caption="Sakila Database ERD", use_container_width=True)
else:
    st.warning(f"ERD diagram not found at {erd_path}")

# User question input
question = st.text_input("Enter your question:")
if st.button("Ask"):
    if question.strip():
        with st.spinner("Thinking..."):
            try:
                answer = run_nl_query(question)
                st.subheader("Answer:")
                st.write(answer)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a question.")
