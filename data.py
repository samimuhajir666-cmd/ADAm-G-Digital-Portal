import streamlit as st
import datetime
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText

# --- 1. EMAIL FUNCTION ---
def send_admission_email(student_name, student_course, student_email):
    sender_email = "samimuhajir666@gmail.com"
    app_password = "iuig kkpr ajhg jbiw" 
    receiver_email = "samimuhajir666@gmail.com"
    
    subject = f"New Admission: {student_name}"
    body = f"Assalamu Alaikum,\n\nNew admission request received:\n\nName: {student_name}\nCourse: {student_course}\nEmail: {student_email}\nDate: {datetime.date.today()}\n\nPlease check the admissions.csv file for full details."
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        with smtplib.SMTP('://gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.send_message(msg)
            return True 
    except Exception as e:
        return False

# 1. Page Configuration
st.set_page_config(page_title="ADAm G Portal", layout="centered")

# 2. Professional CSS
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { 
        width: 100%; border-radius: 5px; height: 3em; 
        background-color: #007bff; color: white; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏫 ADAm G Digital Portal")

# --- TASK 1: THE AI CHATBOT ---
st.subheader("💬 ADAm G Admission Help")

if "history" not in st.session_state:
    st.session_state.history = []

for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Admissions ke bare mein puchein..."):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    query = prompt.lower()
    if "fee" in query or "paisa" in query:
        answer = "ADAm G ki monthly fee sirf 1500 PKR hai."
    elif "location" in query or "kahan" in query:
        answer = "Hum Shah Faisal Colony, Karachi mein waqay hain."
    elif "course" in query or "parhai" in query:
        answer = "Hum Web Development, Python AI, Graphic Design aur Hifz karwate hain."
    elif "admission" in query or "form" in query:
        answer = "Admission lene ke liye niche diya gaya form fill karein."
    else:
        answer = "Maazrat! Main sirf admissions ke sawaloon ke jawab de sakta hun."

    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.history.append({"role": "assistant", "content": answer})

st.divider()

# --- TASK 2: ADMISSION FORM ---
st.subheader("📝 Online Admission Form")

with st.form("admission_form_main", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Student Full Name")
        f_name = st.text_input("Father's Name")
        dob = st.date_input("Date of Birth", value=datetime.date(2010, 1, 1))
    with col2:
        age = st.number_input("Age", min_value=5, max_value=25)
        contact = st.text_input("Contact Number")
        course = st.selectbox("Select Course", ["Web Dev", "Python AI", "Graphic Design", "Hifz"])

    address = st.text_area("Home Address")
    submitted = st.form_submit_button("Submit Application")

    if submitted:
        if name and contact:
            # 1. Save to CSV
            data = {"Name": [name], "Contact": [contact], "Course": [course], "Date": [str(datetime.date.today())]}
            df = pd.DataFrame(data)
            file = "admissions.csv"
            if not os.path.isfile(file):
                df.to_csv(file, index=False)
            else:
                df.to_csv(file, mode='a', header=False, index=False)
            
            # 2. Send Email Notification
            email_status = send_admission_email(name, course, "samimuhajir666@gmail.com")
            
            if email_status:
                st.balloons()
                st.snow()     
                st.toast('Admission Form Successfully Received!', icon='✅')
                st.success(f"Mubarak ho {name}! Aapka data save ho gaya aur Admin ko email bhej di gayi hai.")
            else:
                st.warning(f"Data save ho gaya hai, lekin email bhejney mein masla hua.")
        else:
            st.error("Meherbani karke Name aur Contact number lazmi likhein.")
