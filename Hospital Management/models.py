import json 
from datetime import datetime 
from typing import List, Dict 
 
class User: 
    def __init__(self, user_id, name, role, password): 
        self.user_id = user_id 
        self.name = name 
        self.role = role  # 'admin', 'doctor', or 'patient' 
        self.password = password 
 
    def to_dict(self): 
        return self. __dict__ 
 
class Doctor(User): 
    def __init__(self, user_id, name, specialization, password): 
        super().__init__(user_id, name, 'doctor', password) 
        self.specialization = specialization 
        self.patients: List[int] = []  # store patient IDs 
 
    def add_patient(self, patient_id): 
        if patient_id not in self.patients: 
            self.patients.append(patient_id) 
 
class Patient(User): 
    def __init__(self, user_id, name, age, contact, password): 
        super().__init__(user_id, name, 'patient', password) 
        self.age = age 
        self.contact = contact 
        self.appointments: List[int] = [] 
 
    def book_appointment(self, appointment_id): 
        self.appointments.append(appointment_id) 
 
class Appointment: 
    def __init__(self, appointment_id, patient_id, doctor_id, date, status='Pending'): 
        self.appointment_id = appointment_id 
        self.patient_id = patient_id 
        self.doctor_id = doctor_id 
        self.date = date 
        self.status = status 
 
    def to_dict(self): 
        return self.__dict__