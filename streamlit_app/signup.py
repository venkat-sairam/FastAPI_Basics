import streamlit as st
import requests

st.title("Sign Up")
st.write("Create a new account")

message = st.empty()

with st.form("signup_form"):
    username = st.text_input("Username", key="signup_username")
    email    = st.text_input("Email",    key="signup_email")
    gender   = st.selectbox("Gender",    ["", "male", "female", "other"], key="signup_gender")
    role     = st.selectbox("Role",      ["", "user", "admin", "guest"],   key="signup_role")
    location = st.text_input("Location",  key="signup_location")
    submitted = st.form_submit_button("Sign Up")

if submitted:

    message.empty()
    if not username or not email or not gender or not role:
        message.warning("Username, Email, Gender, and Role are required.")
    else:
        payload = {
            "username": username,
            "email":    email,
            "gender":   gender,
            "location": location or None,
            "role":     role
        }

        try:
            resp = requests.post("http://api:8000/signup", json=payload)
        except Exception as e:
            message.error(f"Request failed: {e}")
        else:
            try:
                data = resp.json()
            except Exception:
                message.error("Invalid JSON in response")
            else:
                if resp.ok and "user_id" in data:
                    message.success(f"Account created! User ID: {data['user_id']}")
                    
                else:
 
                    message.error(data.get("detail", resp.text))

