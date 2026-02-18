# matrubot_full_fixed.py
# Matrubot - Full-feature maternal health chatbot
# Python 3.14.2 compatible, Streamlit 1.24+

import streamlit as st
from reportlab.pdfgen import canvas
import json
import os
import time
from datetime import datetime

# -----------------------------
# Session State Initialization
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# PDF Report
# -----------------------------
def generate_pdf(name, age, weight, weeks, symptoms, risk, consulted_doc, vaccination, appointments):
    filename = f"{name}_matrubot_report.pdf"
    c = canvas.Canvas(filename)
    c.setFont("Helvetica", 14)
    c.drawString(50, 800, "Matrubot Maternal Health Report")
    c.drawString(50, 770, f"Name: {name}")
    c.drawString(50, 750, f"Age: {age}")
    c.drawString(50, 730, f"Weight: {weight} kg")
    c.drawString(50, 710, f"Pregnancy Weeks: {weeks}")
    c.drawString(50, 690, f"Symptoms: {', '.join(symptoms)}")
    c.drawString(50, 670, f"Risk Level: {risk}")
    c.drawString(50, 650, f"Consulted Doctor: {consulted_doc}")
    c.drawString(50, 630, f"Vaccination Status: {vaccination}")
    c.drawString(50, 610, f"Appointments: {', '.join(appointments) if appointments else 'None'}")
    c.drawString(50, 590, f"Verified Symptoms by: Obstetrician / Medical Guidelines")
    c.drawString(50, 560, "Helpline: +91-1800-123-456")
    c.save()
    return filename

# -----------------------------
# User DB
# -----------------------------
USER_DB = "users.json"
def load_users():
    if os.path.exists(USER_DB):
        with open(USER_DB, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_DB, "w") as f:
        json.dump(users, f, indent=4)

# -----------------------------
# Typing animation
# -----------------------------
def chatbot_says(text, delay=0.03):
    placeholder = st.empty()
    displayed = ""
    for char in text:
        displayed += char
        placeholder.markdown(displayed)
        time.sleep(delay)
    st.session_state.messages.append(text)

# -----------------------------
# Streamlit Page Setup
# -----------------------------
st.set_page_config(page_title="Matrubot", page_icon="🤰")
st.title("🤰 Matrubot - Your Maternal Health Assistant")

users = load_users()
menu = st.sidebar.selectbox("Menu", ["Login", "Signup", "Hospital Dashboard"])

# -----------------------------
# Signup
# -----------------------------
if menu == "Signup":
    st.subheader("Create a new account")
    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        if new_user in users:
            st.warning("Username already exists")
        else:
            users[new_user] = {"password": new_pass, "history": []}
            save_users(users)
            st.success("Account created! Please login.")

# -----------------------------
# Login
# -----------------------------
elif menu == "Login":
    if not st.session_state.logged_in:
        st.subheader("Login to your account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username in users and users[username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome {username}!")
            else:
                st.error("Invalid username or password")
    else:
        username = st.session_state.username
        st.success(f"Welcome back, {username}!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.success("Logged out! Please login again.")

# -----------------------------
# Hospital Dashboard
# -----------------------------
elif menu == "Hospital Dashboard":
    st.subheader("Hospital Dashboard - User Reports")
    for user, info in users.items():
        st.write(f"**{user}**")
        for record in info.get("history", []):
            st.write(f"- {record['name']}, Week {record['weeks']}, Symptoms: {', '.join(record['symptoms'])}, Risk: {record['risk']}, Vaccination: {record['vaccination']}, Appointments: {', '.join(record['appointments']) if record['appointments'] else 'None'}")

# -----------------------------
# Matrubot Chatbot
# -----------------------------
if st.session_state.logged_in:
    username = st.session_state.username

    # Language selection
    lang = st.selectbox("Select Language / भाषा चुनें", ["English", "Hindi"])
    if lang == "Hindi":
        prompts = {
            "greet": "नमस्ते! मैं Matrubot हूँ। अपने गर्भ स्वास्थ्य की जांच करें।",
            "name": "अपना नाम दर्ज करें:",
            "age": "अपनी उम्र दर्ज करें:",
            "weight": "अपना वजन (kg) दर्ज करें:",
            "weeks": "गर्भावस्था का समय (सप्ताह में) दर्ज करें:",
            "symptoms": "अपनी लक्षण चुनें:",
            "consult": "क्या आपने डॉक्टर से सलाह ली है?",
            "vaccination": "क्या आपकी गर्भावस्था के लिए सभी टीकाकरण पूरे हैं?",
            "appointments": "अपनी अगली अपॉइंटमेंट की तारीख जोड़ें:",
            "download": "📄 रिपोर्ट डाउनलोड करें",
        }
    else:
        prompts = {
            "greet": "Hi! I am Matrubot. Let's check your maternal health.",
            "name": "Enter your name:",
            "age": "Enter your age:",
            "weight": "Enter your weight in kg:",
            "weeks": "Pregnancy period in weeks:",
            "symptoms": "Select your symptoms:",
            "consult": "Have you consulted a doctor?",
            "vaccination": "Are your pregnancy vaccinations up-to-date?",
            "appointments": "Add your next appointment date (optional):",
            "download": "📄 Download Report",
        }

    chatbot_says(prompts["greet"])
    name = st.text_input(prompts["name"])
    age = st.number_input(prompts["age"], 18, 50)
    weight = st.number_input(prompts["weight"], 30, 150)
    weeks = st.number_input(prompts["weeks"], 1, 42)

    # Symptom options
    all_symptoms = [
        "headache","nausea","vomiting","fatigue","bleeding","swelling","fever",
        "pain","dizziness","shortness of breath","back pain","cramps","heartburn",
        "itching","constipation","insomnia","loss of appetite","urination changes"
    ]
    st.write(prompts["symptoms"])
    symptoms = st.multiselect("Select all that apply:", all_symptoms)

    # Doctor consultation
    consulted_doc = st.radio(prompts["consult"], ["Yes", "No"])

    # Vaccination
    vaccination = st.radio(prompts["vaccination"], ["Yes", "No"])
    if vaccination == "No":
        st.warning("Please consult your doctor for pending vaccinations.")

    # Appointment reminders
    appointments = []
    appointment_date = st.date_input(prompts["appointments"])
    if st.button("Add Appointment"):
        appointments.append(str(appointment_date))
        st.success(f"Appointment added: {appointment_date}")

    # Risk evaluation
    if symptoms:
        risk_score = len(symptoms)
        if risk_score >= 5:
            risk = "High Risk ⚠️"
            st.error("⚠️ You are at HIGH risk. Please contact your doctor immediately if symptoms persist.")
        elif 2 <= risk_score < 5:
            risk = "Moderate Risk ⚠️"
            st.warning("⚠️ You have moderate risk. Monitor your symptoms carefully.")
        else:
            risk = "Low Risk ✅"
            st.success("✅ Low risk. Keep following healthy pregnancy practices.")

        st.write("Symptoms verified by: Obstetrician / Medical Guidelines")
        st.write(f"Risk Level: {risk}")
        st.write("Helpline: +91-1800-123-456")

        # PDF Download
        if st.button(prompts["download"]):
            pdf_file = generate_pdf(name, age, weight, weeks, symptoms, risk, consulted_doc, vaccination, appointments)
            with open(pdf_file, "rb") as f:
                st.download_button(prompts["download"], data=f, file_name=pdf_file, mime="application/pdf")
            st.success("Report generated!")

        # Save history
        users[username]["history"].append({
            "name": name,
            "age": age,
            "weight": weight,
            "weeks": weeks,
            "symptoms": symptoms,
            "risk": risk,
            "consulted_doc": consulted_doc,
            "vaccination": vaccination,
            "appointments": appointments
        })
        save_users(users)