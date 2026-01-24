import random, string, hashlib, re, msvcrt
from datetime import datetime
from db import get_connection

class Bank:

    # ---------------- PIN HASH ----------------
    @staticmethod
    def hash_pin(pin):
        return hashlib.sha256(pin.encode()).hexdigest()

    # ---------------- MASKED PIN ----------------
    @staticmethod
    def masked_input(prompt):
        print(prompt, end="", flush=True)
        pin = ""
        while True:
            ch = msvcrt.getch()
            if ch == b'\r':
                if len(pin) != 4:
                    print("\n❌ PIN must be exactly 4 digits")
                    pin = ""
                    print(prompt, end="", flush=True)
                    continue
                print()
                return pin
            elif ch == b'\x08' and pin:
                pin = pin[:-1]
                print("\b \b", end="", flush=True)
            elif ch.isdigit() and len(pin) < 4:
                pin += ch.decode()
                print("*", end="", flush=True)

    # ---------------- ACCOUNT NUMBER ----------------
    @staticmethod
    def generate_account():
        return ''.join(random.choices(string.digits, k=12))

    # ---------------- CREATE ACCOUNT ----------------
    def create_account(self):
        name = input("Name : ")
        age = int(input("Age : "))
        phno = input("Phone : ")
        email = input("Email : ").lower()
        ifsc = input("IFSC : ").upper()
        pin = Bank.masked_input("4 Digit PIN : ")

        conn = get_connection()
        cur = conn.cursor()

        acc = Bank.generate_account()
        pin_hash = Bank.hash_pin(pin)

        cur.execute("""
            INSERT INTO users (name, age, phno, email, pin_hash, account_number, ifsc)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (name, age, phno, email, pin_hash, acc, ifsc))

        conn.commit()
        cur.close()
        conn.close()

        print("\n🎉 Account Created")
        print("💳 Account Number:", acc)

    # ---------------- AUTH ----------------
    def authenticate(self, acc, pin):
        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT * FROM users
            WHERE account_number=%s AND pin_hash=%s
        """, (acc, Bank.hash_pin(pin)))

        user = cur.fetchone()
        cur.close()
        conn.close()
        return user

    # ---------------- DEPOSIT ----------------
    def deposit(self):
        acc = input("Account Number : ")
        pin = Bank.masked_input("PIN : ")
        user = self.authenticate(acc, pin)

        if not user:
            print("❌ Invalid details")
            return

        amount = int(input("Amount : "))
        new_balance = user["balance"] + amount

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("UPDATE users SET balance=%s WHERE id=%s",
                    (new_balance, user["id"]))

        cur.execute("""
            INSERT INTO transactions (user_id,type,amount,balance_after,time)
            VALUES (%s,%s,%s,%s,%s)
        """, (user["id"], "Deposit", amount, new_balance, datetime.now()))

        conn.commit()
        cur.close()
        conn.close()

        print("✅ Deposited ₹", amount)

    # ---------------- WITHDRAW ----------------
    def withdraw(self):
        acc = input("Account Number : ")
        pin = Bank.masked_input("PIN : ")
        user = self.authenticate(acc, pin)

        if not user:
            print("❌ Invalid details")
            return

        amount = int(input("Amount : "))
        if amount > user["balance"]:
            print("❌ Insufficient balance")
            return

        new_balance = user["balance"] - amount

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("UPDATE users SET balance=%s WHERE id=%s",
                    (new_balance, user["id"]))

        cur.execute("""
            INSERT INTO transactions (user_id,type,amount,balance_after,time)
            VALUES (%s,%s,%s,%s,%s)
        """, (user["id"], "Withdraw", amount, new_balance, datetime.now()))

        conn.commit()
        cur.close()
        conn.close()

        print("💸 Withdrawn ₹", amount)

    # ---------------- TRANSACTIONS ----------------
    def history(self):
        acc = input("Account Number : ")
        pin = Bank.masked_input("PIN : ")
        user = self.authenticate(acc, pin)

        conn = get_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute("""
            SELECT * FROM transactions
            WHERE user_id=%s ORDER BY time DESC
        """, (user["id"],))

        for t in cur.fetchall():
            print(t["type"], t["amount"], t["time"])

        cur.close()
        conn.close()
