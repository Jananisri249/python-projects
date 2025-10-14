import streamlit as st
import json
import os

DATA_FILE = "bank_data.json"

# ---------- Save data to JSON ----------
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------- Load existing data ----------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                st.warning("JSON file was empty or corrupted. Starting fresh.")
                return {}
    else:
        return {}

# ---------- Create account ----------
def create_account(data):
    st.subheader("Create New Account")
    name = st.text_input("Enter account holder name:")
    pin = st.text_input("Enter 4-digit PIN:", type="password", max_chars=4)
    balance = st.number_input("Enter initial balance:", min_value=0.0, step=0.1)

    if st.button("Create Account"):
        if name == "" or pin == "":
            st.warning("Please fill all fields.")
        elif name in data:
            st.error(f"Account for '{name}' already exists!")
        else:
            data[name] = {"account_holder": name, "pin": pin, "balance": balance}
            save_data(data)
            st.success(f"Account for {name} added successfully!")

# ---------- Display accounts ----------
def display_accounts(data):
    st.subheader("All Bank Accounts")
    if not data:
        st.info("No accounts found.")
    else:
        for account in data.values():
            st.write(f"**Name:** {account['account_holder']} | **Balance:** ₹{account['balance']} | **PIN:** {account['pin']}")

# ---------- Update account ----------
def update_account(data):
    st.subheader("Update Account")
    name = st.text_input("Enter account holder name to update:")
    if name in data:
        choice = st.radio("Select detail to update:", ["PIN", "Balance"])
        if choice == "PIN":
            new_pin = st.text_input("Enter new 4-digit PIN:", type="password", max_chars=4)
            if st.button("Update PIN"):
                data[name]['pin'] = new_pin
                save_data(data)
                st.success(f"PIN updated for {name}")
        else:
            new_balance = st.number_input("Enter new balance:", min_value=0.0, step=0.1)
            if st.button("Update Balance"):
                data[name]['balance'] = new_balance
                save_data(data)
                st.success(f"Balance updated for {name}")
    else:
        if name:
            st.error(f"Account for '{name}' not found.")

# ---------- Delete account ----------
def delete_account(data):
    st.subheader("Delete Account")
    name = st.text_input("Enter account holder name to delete:")
    if name in data:
        if st.button(f"Delete '{name}'"):
            del data[name]
            save_data(data)
            st.success(f"Account '{name}' deleted successfully!")
    else:
        if name:
            st.error(f"Account for '{name}' not found.")

# ---------- Streamlit App ----------
def main():
    st.title("🏦 Bank Account Manager")

    data = load_data()

    menu = ["Create Account", "Display Accounts", "Update Account", "Delete Account"]
    choice = st.sidebar.radio("Menu", menu)

    if choice == "Create Account":
        create_account(data)
    elif choice == "Display Accounts":
        display_accounts(data)
    elif choice == "Update Account":
        update_account(data)
    elif choice == "Delete Account":
        delete_account(data)

if __name__ == "__main__":
    main()
