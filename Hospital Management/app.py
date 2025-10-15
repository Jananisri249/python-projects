import streamlit as st 
from models import Doctor, Patient, Appointment 
from database import read_db, write_db 
from datetime import datetime 
 
st.set_page_config(page_title="Hospital Management System", layout="wide") 
# Load DB 
db = read_db() 
 
# Initialize session 
if "user" not in st.session_state: 
    st.session_state["user"] = None 
 
# ---------------------- LOGIN ---------------------- 
def login(): 
    st.title("Hospital Management System") 
    username = st.text_input("Username") 
    password = st.text_input("Password", type="password") 
    role = st.selectbox("Role", ["admin", "doctor", "patient"]) 
 
    if st.button("Login"): 
        users = db[role + "s"] 
        for user in users: 
            if user["name"] == username and user["password"] == password: 
                st.session_state["user"] = { 
                    "name": username, 
                    "role": role, 
                    "id": user["user_id"], 
                } 
                st.success(f"Logged in as {username} ({role})") 
                st.rerun() 
        st.error("Invalid login credentials") 
 
# ---------------------- ADMIN ---------------------- 
def admin_dashboard(): 
    st.header("Admin Dashboard") 
    st.write("**Total Doctors:**", len(db["doctors"])) 
    st.write("**Total Patients:**", len(db["patients"])) 
 
    # --- Add Doctor --- 
    st.subheader("Add Doctor") 
    with st.form("add_doc"): 
        name = st.text_input("Doctor Name") 
        spec = st.text_input("Specialization") 
        password = st.text_input("Password") 
        submit = st.form_submit_button("Add Doctor") 
        if submit: 
            if name and spec and password: 
                doc_id = db["next_ids"]["doctor"] + 1 
                db["next_ids"]["doctor"] = doc_id 
                new_doc = Doctor(doc_id, name, spec, password) 
                db["doctors"].append(new_doc.to_dict()) 
                write_db(db) 
                st.success("Doctor added successfully!") 
                st.rerun() 
            else: 
                st.warning("Please fill all fields") 
 
    # --- Add Patient --- 
    st.subheader("Add Patient") 
    with st.form("add_pat"): 
        pname = st.text_input("Patient Name") 
        age = st.number_input("Age", min_value=0, max_value=120, step=1) 
        contact = st.text_input("Contact") 
        ppassword = st.text_input("Password") 
        submit_p = st.form_submit_button("Add Patient") 
        if submit_p: 
            if pname and contact and ppassword: 
                pat_id = db["next_ids"]["patient"] + 1 
                db["next_ids"]["patient"] = pat_id 
                new_pat = Patient(pat_id, pname, age, contact, ppassword) 
                db["patients"].append(new_pat.to_dict()) 
                write_db(db) 
                st.success("Patient added successfully!") 
                st.rerun() 
            else: 
                st.warning("Please fill all fields") 
 
    st.subheader("View Doctors") 
    for d in db["doctors"]: 
        st.write(f"{d['name']} ({d['specialization']})") 
 
    st.subheader("View Patients") 
    for p in db["patients"]: 
        st.write(f"{p['name']} (Age: {p['age']}, Contact: {p['contact']})") 
 
# ---------------------- DOCTOR ---------------------- 
def doctor_dashboard(): 
    st.header("Doctor Dashboard") 
    doctor_id = st.session_state["user"]["id"] 
 
    st.subheader("My Appointments") 
    doctor_appts = [a for a in db["appointments"] if a["doctor_id"] == doctor_id] 
 
    if not doctor_appts: 
        st.info("No appointments yet.") 
    else: 
        for appt in doctor_appts: 
            st.write( 
                f"Patient ID: {appt['patient_id']} | Date: {appt['date']} | Status: {appt['status']}" 
            ) 
 
    st.subheader("Patient Notes") 
    st.info("Feature placeholder – doctors can add/view patient records here.") 
 
# ---------------------- PATIENT ---------------------- 
def patient_dashboard(): 
    st.header("Patient Dashboard") 
    patient_id = st.session_state["user"]["id"] 
 
    st.subheader("Book Appointment") 
    if not db["doctors"]: 
        st.warning("No doctors available. Please contact admin.") 
        return 
 
    doctor_names = [d["name"] for d in db["doctors"]] 
    doc_choice = st.selectbox("Choose Doctor", doctor_names) 
    appt_date = st.date_input("Select Date") 
 
    if st.button("Book Appointment"): 
        doctor = next(d for d in db["doctors"] if d["name"] == doc_choice) 
        appt_id = db["next_ids"]["appointment"] + 1 
        db["next_ids"]["appointment"] = appt_id 
        new_appt = Appointment(appt_id, patient_id, doctor["user_id"], str(appt_date)) 
        db["appointments"].append(new_appt.to_dict()) 
        write_db(db) 
        st.success(f"Appointment booked with Dr. {doc_choice} on {appt_date}") 
        st.rerun() 
 
    st.subheader("My Appointments") 
    my_appts = [a for a in db["appointments"] if a["patient_id"] == patient_id] 
    if not my_appts: 
        st.info("No appointments booked yet.") 
    else: 
        for appt in my_appts: 
            st.write( 
                f"Doctor ID: {appt['doctor_id']} | Date: {appt['date']} | Status: {appt['status']}" 
            ) 
 
# ---------------------- MAIN ---------------------- 
def main(): 
    user = st.session_state["user"] 
    if not user: 
        login() 
    else: 
        st.sidebar.success(f"Logged in as {user['name']} ({user['role']})") 
 
        if user["role"] == "admin": 
            admin_dashboard() 
        elif user["role"] == "doctor": 
            doctor_dashboard() 
        elif user["role"] == "patient": 
            patient_dashboard() 
 
        if st.sidebar.button("Logout"): 
            st.session_state["user"] = None 
            st.rerun() 
 
if __name__ == "__main__": 
    main() 
 
 
