import streamlit as st
import requests

rasa_server_url = "http://localhost:5005/webhooks/rest/webhook"
payload = {"sender": "streamlit_user", "message": "Hello, Rasa!"}

response = requests.post(rasa_server_url, json=payload)

st.title("Rasa Connection Test")
st.write("Response from Rasa:", response.json())
