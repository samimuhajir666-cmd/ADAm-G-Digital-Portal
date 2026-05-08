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

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏫 ADAm G Digital Portal")

# --- 3. THE AI CHATBOT ---
if "history" not in st.session_state:
    st.session_state.history = []

for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("ADAM G Chatbot - Ask me anything"):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    query = prompt.lower()
    if any(word in query for word in ["hi", "hello", "assalamu alaikum"]):
        answer = "Wa Alaikum Assalam! I am the ADAm G Virtual Assistant. How can I help you?"
    elif "fee" in query:
        answer = "Our monthly fee is 1,500 PKR."
    elif "location" in query:
        answer = "We are located in Shah Faisal Colony, Karachi."
    else:
        answer = "I am ADAM G Bot. Please use the form below for admissions."

    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.history.append({"role": "assistant", "content": answer})

st.divider()

# --- 4. ADMISSION FORM SECTION ---
st.subheader("📝 ADAm G Admission Form")

with st.form("admission_form_main", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=1, max_value=100, value=18)
        email_input = st.text_input("Student Email")
        cnic_val = st.text_input("CNIC / B-Form Number")

    with col2:
        contact = st.text_input("Contact Number")
        dob = st.date_input("Date of Birth", value=datetime.date(2010, 1, 1), min_value=datetime.date(1900, 1, 1))
        course = st.selectbox("Course", ["Web Dev", "Python AI", "Graphic Design", "Hifz"])
        cast = st.selectbox("Background", ["Muhajir", "Sindhi", "Punjabi", "Balochi", "Pashtun"])
        hafiz_status = st.selectbox("Hafiz-e-Quran?", ["Yes", "No"])
    
    address_val = st.text_area("Residential Address") 
    
    # --- HERE IS THE SUBMIT BUTTON ---
    submitted = st.form_submit_button("Submit Admission Request")

    if submitted:
        if name and email_input and contact:
            # SAVE TO CSV (All fields included)
            new_entry = {
                "Date": [str(datetime.date.today())],
                "Name": [name],
                "Email": [email_input],
                "CNIC": [cnic_val],
                "Course": [course],
                "Age": [age],
                "DOB": [str(dob)],
                "Cast": [cast],
                "Hafiz": [hafiz_status],
                "Address": [address_val]
            }
            df = pd.DataFrame(new_entry)
            file_path = "admission_data.csv"
            df.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)
            
            # --- THE DIGITAL CARD ---
            st.markdown(f"""
            <div style="border: 3px solid #007bff; padding: 25px; border-radius: 15px; background-color: #ffffff; text-align: center; box-shadow: 10px 10px 5px #eeeeee; margin-top: 20px;">
                <h1 style="color: #007bff; margin-bottom: 5px;">ADAm G Portal</h1>
                <p style="font-size: 14px; color: gray; font-style: italic;">Official Admission Receipt</p>
                <hr style="border: 1px solid #007bff; width: 80%; margin: auto;">
                <div style="text-align: left; padding: 20px; font-family: sans-serif;">
                    <p><strong>Student Name:</strong> {name}</p>
                    <p><strong>Course:</strong> {course}</p>
                    <p><strong>CNIC / ID:</strong> {cnic_val}</p>
                    <p><strong>Date:</strong> {datetime.date.today()}</p>
                </div>
                <hr style="border: 1px solid #eeeeee;">
                <p style="color: #28a745; font-weight: bold; font-size: 18px;">✅ APPLICATION RECEIVED</p>
                <p style="font-size: 10px; color: gray;">Ref ID: {datetime.datetime.now().strftime('%Y%H%M%S')}</p>
            </div>
            <p style="text-align: center; color: gray; font-size: 12px; margin-top: 10px;">Please take a screenshot of this card for your records.</p>
            """, unsafe_allow_html=True)
            
            # --- NOTIFICATIONS ---
            admin_msg = f"New Student: {name}\nCNIC: {cnic_val}\nCourse: {course}\nContact: {contact}"
            send_email("samimuhajir666@gmail.com", "ADMIN: New Admission", admin_msg)

            student_msg = f"Assalamu Alaikum {name},\n\nForm received for {course}. Our team will contact you soon.\n\nJazakAllah."
            email_status = send_email(email_input, "Form Received - ADAm G", student_msg)
            
            if email_status:
                st.balloons()
                st.success(f"Mubarak ho {name}! Form submit ho gaya.")
            else:
                st.warning("Data save ho gaya, magar email bhejney mein masla hua.")
        else:
            st.error("Meherbani karke saari malomat (Name, Email, Contact) lazmi likhein.")
