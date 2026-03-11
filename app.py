import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI

st.title("Talking Rabbit MVP")
st.write("Conversational insights from your CSV data.")


uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Dataset Preview")
    st.dataframe(df)

    question = st.text_input("Ask a question about your data")

    if question:

        
        csv_text = df.to_csv(index=False)

        prompt = f"""
You are a data analysis assistant.  
The user has uploaded this dataset:

{csv_text}

User question: {question}

1. Interpret the question.
2. Convert it to a Pandas operation.
3. Compute the answer.
4. Respond in clean English.
5. Suggest what chart should be shown (bar, line, pie, etc.).
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        answer = response.choices[0].message.content
        st.write("### Answer")
        st.write(answer)

       
        if "revenue" in question.lower() or "units" in question.lower():
            if "Quarter" in df.columns:
                fig, ax = plt.subplots()
                df.groupby("Quarter")["Revenue"].sum().plot(kind="bar", ax=ax)
                ax.set_title("Revenue by Quarter")
                st.pyplot(fig)