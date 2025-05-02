import streamlit as st
import requests

st.title("Sign Up")
st.write("Create a new account")

username = st.text_input("Username")
email = st.text_input("Email")
gender = st.selectbox("Gender", ["", "male", "female", "other"])
location = st.text_input("Location")
role = st.selectbox("Role", ["", "user", "admin", "guest"])

if st.button("Sign Up"):
    if not username or not email or not role:
        st.warning("Username, Email, and Role are required.")
    else:
        payload = {
            "username": username,
            "email": email,
            "gender": gender or None,
            "location": location or None,
            "role": role
        }

        try:
            response = requests.post("http://api:8000/signup", json=payload)
        except Exception as e:
            st.error(f"Request failed: {e}")
            st.stop()

        try:
            response_json = response.json()
            st.write("Status Code:", response.status_code)
            st.write("Raw Text:", response.text)
        except Exception as e:
            st.error(f"Failed to decode JSON: {e}")
            st.error(f"Raw response: {response.text}")
            response_json = {}

        if response.ok and "user_id" in response_json:
            st.success("Account created successfully!")
            st.success("User ID: {}".format(response_json.get("user_id")))
        else:
            st.error(f"Error: {response_json.get('detail') or response.text}")

