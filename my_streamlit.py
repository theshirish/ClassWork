import my_streamlit as st

st.title("Radhasoami ji. Welcome to the Streamlit service!")

user_name = st.text_input("Enter your name : ")
if user_name:
    st.write(f"Hello, {user_name}! Welcome to the Streamlit service!")
user_age = st.slider("Select your age", 0, 100, 25)
if user_age:
    st.write(f"Your age is {user_age}.")

if st.button("Click me"):
    st.success("Button clicked! You can add more functionality here.")
# streamlit run streamlit.py
