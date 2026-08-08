import httpx
import streamlit as st

endpoint = "http://127.0.0.1:8000/first_endpoint"
params = {}
body = {
    "query": "What is the capital of France?",
    "temp": 0.1,
    "retries": 3
}

message_input = st.text_input("Enter your message:")
temperature = float(st.text_input(
    "Enter temperature (default 0.1):", value="0.1"))
retries = int(st.text_input("Enter number of retries (default 3):", value="3"))

try:
    with httpx.Client() as client:
        response = client.post(endpoint, json=body, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        st.write("Response from FastAPI service:", data)
        print("Response from FastAPI service:", data)
except httpx.RequestError as e:
    print(f"An error occurred while requesting {e.request.url!r}.")
