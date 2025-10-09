import streamlit as st
class Vehicle:
    def __init__(self,brand,model):
        self.brand=brand
        self.model=model
    def start(self):
        return f"{self.brand} is starting"

class Car(Vehicle):
    def __init__(self,brand,model):
        super().__init__(brand,model)
    def play_music(self):
        return "Playing music"
class ElectricCar(Car):
    def __init__(self, brand, model):
        super().__init__(brand, model)
    def charge(self):
        return "Charging..."
class SmartDeivce:
    def connect_wifi(self):
        return "Connecting to wifi"
class SmartCar(Car,SmartDeivce):
    def __init__(self,brand,model):
        super().__init__(brand,model)
    def autopilot(self):
        return "AutoPilot mode Activated"
class Bike(Vehicle):
    def __init__(self,brand,model):
        super().__init__(brand,model)
    def kick_start(self):
        return "Bike kick started"
class ElectricSmartCar(SmartCar,ElectricCar):
    def __init__(self, brand, model):
        super().__init__(brand, model)
    

st.title("Vehicle Management System")
brand=st.text_input("Enter Vehicle Brand")
model=st.text_input("Enter Vehicle Model")

vehicle_type=st.selectbox("Select Vehicle Type",["Car","Bike","Electric Car","Smart Car","Electric Smart Car"])
if st.button("Create Vehicle"):
    if vehicle_type=="Car":
        vehicle=Car(brand,model)
        st.success(f"Car: {vehicle.brand} {vehicle.model}")
        features={}

        features['Feature']=[vehicle.start()]
        features['Feature'].append(vehicle.play_music())
        st.table(features)
    elif vehicle_type=="Bike":
        vehicle=Bike(brand,model)
        features={}
        st.success(f"Bike: {vehicle.brand} {vehicle.model}")
        features['Feature']=[vehicle.start()]
        features['Feature'].append(vehicle.kick_start())
        st.table(features)

    elif vehicle_type=="Electric Car":
        vehicle=ElectricCar(brand,model)
        features={}
        st.success(f" Electric Car: {vehicle.brand} {vehicle.model}")
        features['Feature']=[vehicle.start()]
        features['Feature'].append(vehicle.play_music())
        features['Feature'].append(vehicle.charge())
        st.table(features)

    elif vehicle_type=="Smart Car":
        vehicle=SmartCar(brand,model)
        features={}
        st.success(f"Smart Car: {vehicle.brand} {vehicle.model}")
        features['Feature']=[vehicle.start()]
        features['Feature'].append(vehicle.play_music())
        features['Feature'].append(vehicle.connect_wifi())
        features['Feature'].append(vehicle.autopilot())
        st.table(features)

    elif vehicle_type=="Electric Smart Car":
        vehicle=ElectricSmartCar(brand,model)
        features={}
        st.success(f"Electric Smart Car: {vehicle.brand} {vehicle.model}")
        features['Feature']=[vehicle.start()] 
        features['Feature'].append(vehicle.play_music())
        features['Feature'].append(vehicle.connect_wifi())
        features['Feature'].append(vehicle.autopilot())
        features['Feature'].append(vehicle.charge())
        st.table(features)


