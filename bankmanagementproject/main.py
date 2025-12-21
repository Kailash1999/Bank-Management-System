import json
import random
import string
from pathlib import Path


class Bank:
        database='data.json'
        data=[]
        try:
            if Path(database).exists():
                with open(database,'r') as f:
                    data=json.load(f)
            else:
                print("No Such File Exists..")
        except Exception as e:
            print("Exception Occured as {e}")

        @staticmethod
        def update():
             with open(Bank.database,'w') as f:
                  f.write(json.dump(Bank.data))

        def Create_account(self):
                
                info={
                    "name":input("Enter Your Name :"),
                    "age":int(input("Enter Your Age")),
                    "phno":int(input("Enter Your Mobile Number")),
                    "email":input("Enter Your Email"),
                    "pin":int(input("Enter Your 4 Number Pin :")),
                    "account number":112345,
                    "balance" :0
                }
                if (info["age"]<18 
                        or len(str(info["pin"]))!=4
                        or not info["phno"].isdigit() 
                        or len(str(info["phno"]))!=10 
                        or not info["email"].endswith("@gmail.com")
                        ):
                    
                    print("🛑Sorry You Can Not Create An Account!")
                    
                else:
                    print("✨Your Account Created Successfully✨")
                    for i in info:
                        print(f"{i} :{info[i]} ")
                    print("✒️Please!Remember Your Account Number✒️")
                    Bank.data.append(info)
                  
                  

user=Bank()

print("""
╔══════════════════════════════════════════╗
║        🏦 BANK MANAGEMENT SYSTEM 🏦       ║
╠══════════════════════════════════════════╣
║  1️⃣  Create New Bank Account              ║
║  2️⃣  Deposit Money                        ║
║  3️⃣  Withdraw Money                       ║
║  4️⃣  View Account Details                 ║
║  5️⃣  Update Account Information           ║
║  6️⃣  Delete Account                       ║
╚══════════════════════════════════════════╝
""")

choice=int(input("Enter Your Choice :"))

if choice==1:
    user.Create_account()

