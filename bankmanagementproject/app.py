import streamlit as st
import json
import random
import string
import hashlib
import re
from pathlib import Path

# ===================== DATABASE LAYER =====================
class BankDB:
    def __init__(self, filename="data.json"):
        self.filename = filename
        self.data = self.load()

    def load(self):
        if Path(self.filename).exists():
            with open(self.filename, "r") as f:
                return json.load(f)
        return []

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=4)

    def generate_account(self):
        while True:
            acc = "".join(random.choices(string.digits, k=12))
            if not any(i["account_number"] == acc for i in self.data):
                return acc

    def hash_pin(self, pin):
        return hashlib.sha256(pin.encode()).hexdigest()

    def find_user(self, acc, pin):
        hashed = self.hash_pin(pin)
        for user in self.data:
            if user["account_number"] == acc and user["pin"] == hashed:
                return user
        return None


# ===================== APPLICATION LAYER =====================
class BankApp:
    def __init__(self):
        st.set_page_config("Bank Management System", "🏦")
        st.title("🏦 Bank Management System")
        self.db = BankDB()
        self.menu()

    # ---------- VALIDATIONS ----------
    @staticmethod
    def valid_email(email):
        return bool(re.fullmatch(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", email))

    @staticmethod
    def valid_phone(ph):
        return bool(re.fullmatch(r"^[6-9]\d{9}$", ph))

    # ---------- MENU ----------
    def menu(self):
        choice = st.sidebar.radio(
            "Menu",
            [
                "Create Account",
                "Deposit Money",
                "Withdraw Money",
                "Account Details",
                "Update Account",
                "Delete Account",
            ],
        )

        if choice == "Create Account":
            self.create_account()
        elif choice == "Deposit Money":
            self.deposit()
        elif choice == "Withdraw Money":
            self.withdraw()
        elif choice == "Account Details":
            self.details()
        elif choice == "Update Account":
            self.update_account()
        elif choice == "Delete Account":
            self.delete_account()

    # ---------- FEATURES ----------
    def create_account(self):
        st.header("🆕 Create New Account")

        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, step=1)
        pin = st.text_input("4 Digit PIN", type="password")
        phone = st.text_input("Mobile Number")
        email = st.text_input("Email")
        ifsc = st.text_input("IFSC Code")

        if st.button("Create Account"):
            if age < 18:
                st.error("You must be 18+")
            elif len(pin) != 4 or not pin.isdigit():
                st.error("PIN must be exactly 4 digits")
            elif not self.valid_phone(phone):
                st.error("Invalid phone number")
            elif not self.valid_email(email):
                st.error("Invalid email")
            else:
                acc = self.db.generate_account()
                user = {
                    "name": name,
                    "age": age,
                    "phno": phone,
                    "email": email.lower(),
                    "pin": self.db.hash_pin(pin),
                    "account_number": acc,
                    "ifsc": ifsc.upper(),
                    "balance": 0,
                }
                self.db.data.append(user)
                self.db.save()

                st.success("🎉 Account Created Successfully!")
                st.info(f"Account Number: {acc}")

    def deposit(self):
        st.header("💰 Deposit Money")

        acc = st.text_input("Account Number")
        ifsc = st.text_input("IFSC Code")
        pin = st.text_input("PIN", type="password")
        amount = st.number_input("Amount", min_value=1, max_value=50000)

        if st.button("Deposit"):
            user = self.db.find_user(acc, pin)
            if not user or user["ifsc"] != ifsc.upper():
                st.error("Invalid account / PIN / IFSC")
            else:
                user["balance"] += amount
                self.db.save()
                st.success(f"₹{amount} deposited successfully")
                st.info(f"Balance: ₹{user['balance']:,}")

    def withdraw(self):
        st.header("💸 Withdraw Money")

        acc = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password")
        amount = st.number_input("Amount", min_value=1, max_value=50000)

        if st.button("Withdraw"):
            user = self.db.find_user(acc, pin)
            if not user:
                st.error("Invalid account or PIN")
            elif amount > user["balance"]:
                st.error("Insufficient balance")
            else:
                user["balance"] -= amount
                self.db.save()
                st.success("Withdrawal successful")
                st.info(f"Balance: ₹{user['balance']:,}")

    def details(self):
        st.header("📄 Account Details")

        acc = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password")

        if st.button("View Details"):
            user = self.db.find_user(acc, pin)
            if not user:
                st.error("Invalid credentials")
            else:
                st.json(
                    {
                        "Name": user["name"],
                        "Account": f"XXXX-XXXX-{user['account_number'][-4:]}",
                        "Balance": f"₹{user['balance']:,}",
                    }
                )

    def update_account(self):
        st.header("⚙️ Update Account")

        acc = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password")

        user = self.db.find_user(acc, pin)
        if user:
            phone = st.text_input("New Mobile Number", user["phno"])
            email = st.text_input("New Email", user["email"])

            if st.button("Update"):
                user["phno"] = phone
                user["email"] = email
                self.db.save()
                st.success("Account updated successfully")

    def delete_account(self):
        st.header("❌ Delete Account")

        acc = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password")

        if st.button("Delete Account"):
            user = self.db.find_user(acc, pin)
            if not user:
                st.error("Invalid credentials")
            else:
                self.db.data.remove(user)
                self.db.save()
                st.success("Account deleted successfully")


# ===================== RUN APP =====================
if __name__ == "__main__":
    BankApp()
