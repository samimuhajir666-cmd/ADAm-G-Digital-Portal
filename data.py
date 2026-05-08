import streamlit as st
import datetime
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText

# --- 1. EMAIL LOGIC ---
def send_email(target_email, subject, body):
    sender_email = "samimuhajir666@gmail.com"
    app_password = "iuig kkpr ajhg jbiw" 
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = target_email
    try:
        with smtplib.SMTP('://gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.send_message(msg)
            return True 
    except Exception:
        return False

# --- 2. PAGE SETUP ---
st.set_page_config(page_title="ADAm G Portal", layout="centered")

st.title("🏫 ADAm G Digital Portal")

# --- 3. FORM SECTION ---
with st.form("admission_form", clear_on_submit=True):
    name = st.text_input("Full Name")
    email_input = st.text_input("Email")
    course = st.selectbox("Course", ["Web Dev", "Python AI", "Graphic Design"])
    cnic_val = st.text_input("CNIC Number")
    submitted = st.form_submit_button("Submit Admission Request")

    if submitted:
        if name and email_input:
            # --- CARD DISPLAY (This will now show on screen!) ---
            st.markdown(f"""
            <div style="border: 3px solid #007bff; padding: 20px; border-radius: 10px; background-color: white; text-align: center; color: black;">
                <h2 style="color: #007bff;">ADAm G Admission Card</h2>
                <hr>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Course:</strong> {course}</p>
                <p><strong>Status:</strong> Received</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.balloons()
            st.success(f"Mubarak ho {name}!")
            send_email("samimuhajir666@gmail.com", "New Student", f"Name: {name}, Course: {course}")
        else:
            st.error("Please fill all fields")
