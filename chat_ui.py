import streamlit as st

prompt = st.chat_input("Enter your prompt here:")
if prompt:
    st.write(f"You entered: {prompt}")
