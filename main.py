import json
import random
import string
import hashlib
from pathlib import Path
import msvcrt #intract with keyboard on in windows
import sys
import time
from datetime import datetime
import re


class Bank:

        database='data.json' 
        data=[]
        #-----------------LOAD DATA---------------------------
        try:
            if Path(database).exists():
                with open(database,'r') as f:
                    data=json.load(f)
            else:
                print("No Such File Exists..")
        except Exception as e:
            print(f"Exception Occured as {e}")

            #------------------SAVE DATA-------------------------

        @staticmethod
        def update():
             with open(Bank.database,'w') as f:
                  json.dump(Bank.data, f, indent=4)

     #--------------------------------GENERATE ACCOUNT NUMBER----------------------------

        @staticmethod
        def accountgenerate()->str:
              while True:
                    acc="".join(random.choices(string.digits,k=12))
                    if not any(i.get("account_number") == acc for i in Bank.data):
                       return acc
        
     #------------------------------------PIN HASH--------------------------------
        
        @staticmethod
        def hash_pin(pin: str) -> str:
              return hashlib.sha256(pin.encode()).hexdigest()
        
        
        #-------------------------------MASKED PIN INPUT-----------------------------
        
        @staticmethod
        def masked_input(prompt:str) -> str:
             print(prompt,end="",flush=True)
             pin="" #empty pin len =0
             while True:
                  ch=msvcrt.getch()
                  if ch==b'\r': #Enter
                       if len(pin)!=4:
                            print("\n❌ PIN must be exactly 4 digits")
                            pin=""
                            print(prompt,end="",flush=True)
                            continue
                       print()
                       break
                  elif ch==b'\x08': #Backspace
                       if pin:
                            pin=pin[:-1]
                            print("\b \b",end="",flush=True) #dlt one star
                  elif ch.isdigit() and len(pin)<4:
                       pin +=ch.decode()
                       print("*",end="",flush=True)
             return pin
        
        #-------------------------------VALIDATIONS--------------------------
        @staticmethod
        def is_valid_email(email:str) -> bool:
             email_regex=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
             return bool(re.fullmatch(email_regex,email))
        
        @staticmethod
        def is_valid_phno(phno:str) -> bool:
             ph_regex=r"^[6-9]\d{9}$"
             return bool(re.fullmatch(ph_regex,phno))
        
        #[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[AUTHENTICATION]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]
        @staticmethod
        def authenticate(accnum: str,pin:str,ifsc: str=None):
              hashed_pin = Bank.hash_pin(pin)
              for user in Bank.data:
                   if user.get("account_number")==accnum and user.get('pin')==hashed_pin:
                        if ifsc:
                             if user.get('ifsc')==ifsc.upper():
                                  return user
                             else:
                                  return None
                        return user
              return None
             
        
        #==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=CREATE ACCOUNT=-=-=-=-=-=-=-=-=-=-=-=-==

        def Create_account(self):
                name=input("Enter Your Name :")
                try:
                 age=int(input("Enter Your Age :"))
                except ValueError:
                     print("❌Enter a valid Age")
                     return
                pin=Bank.masked_input("Enter Your 4 digit PIN :") 
                phno=input("Enter Your Mobile Number :").strip()
                email=input("Enter Your Email :").strip().lower()
                ifsc=input("Enter Your IFSC CODE :")

                
                #--------------Validation on raw input-----------------------------
                if  age < 18:
                      print("🛑Sorry!You Can Not Create An Account,You Are Underage")
                      return
                if len(pin) !=4 or not pin.isdigit():
                     print("🛑Sorry!You Can Not Create An Account,Pleaase Enter A Valid Pin Number")
                     return
                if not Bank.is_valid_phno(phno):
                     print("🛑Sorry!You Can Not Create An Account,Please Enter a Valid Mobile Number")
                     return
                if not Bank.is_valid_email(email):
                     print("🛑Sorry!You Can Not Create An Account,Please Enter a Valid Email Id")
                     return
                
                info = {
                        "name": name,
                        "age": age,
                        "phno": phno,
                        "email": email,
                        "pin": Bank.hash_pin(pin),   # ✅ hashed PIN
                        "account_number": Bank.accountgenerate(),
                        "ifsc":ifsc.upper(),
                        "balance": 0,
                        "transactions":[] #TRANSITION HISTORY
                         }

                
                print(f"""
════════════════════════════════════════════════
🎉        ACCOUNT CREATED SUCCESSFULLY        🎉
════════════════════════════════════════════════

👤 Account Holder : {info['name']}
💳 Account Number : {info['account_number']}
🏦 IFSC Code      : {info['ifsc']}
📞 Mobile Number  : {info['phno']}

════════════════════════════════════════════════
✒️  Please remember your Account Number safely
🔐  Never share your PIN with anyone
🙏  Thank you for choosing Our Bank
════════════════════════════════════════════════
""")
                
                Bank.data.append(info)
                    
                Bank.update()

     #================================DEPOSIT MONEY=======================================
        def depositmoney(self) :
              accnum=input("Please Enter Your Account Number :")
              ifsc=input("Please Enter YOUR IFSC CODE :")
              pin=Bank.masked_input("Please Enter Your 4 digit PIN :")

              userdata=Bank.authenticate(accnum,pin,ifsc)

              if not userdata:
                    print("❌Sorry!This Account is Not Exist❌")
                    return
              
              try:

                 amount=int(input("How Much Money You Want To Deposit :"))
              except ValueError:
                 print("❌ Please enter a valid number ❌")
                 return
        
              if amount <= 0 or amount > 50000:
                        print("❌ Sorry! You Can't Deposit More Than 50000 or Below 1 ❌")
                        return

              userdata['balance'] +=amount

              if "transactions" not in userdata:
                 userdata["transactions"] = []

              userdata["transactions"].append({
                   "type":"Deposit",
                   "amount":amount,
                   "balance_after":userdata['balance'],
                   "time":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
              })

              Bank.update()
              print(f"✨✨Amount ₹{amount} Deposit Successfully✨✨")
              print(f"💰Your Current Balance is ₹{userdata['balance']:,}")
     
     #++++++++++++++++++++++++++++++++ WITHDRAW +++++++++++++++++++++++++++++

        def withdraw_money(self):
             accnum=input("Enter Your Account Number :")
             pin=Bank.masked_input("Enter Your 4 digit PIN :")

             userdata=Bank.authenticate(accnum,pin)
             if not userdata:
                    print("❌Sorry!This Account is Not Exist❌")
                    return
              
             try:
                  amount=int(input("How Much Money You Want To Withdraw :"))
             except ValueError:
                  print("❌ Please enter a valid number ❌")
                  return
             if amount>userdata.get("balance",0):
                  print("❌Insufficient Balance!Try Again❌")
                  return
             if amount>50000 or amount<=0:
                  print("❌Invalid Amount❌")
                  return
             userdata["balance"]=userdata["balance"]-amount

             if "transactions" not in userdata:
                 userdata["transactions"] = []
             
             userdata["transactions"].append({
                   "type":"Withdraw",
                   "amount":amount,
                   "balance_after":userdata['balance'],
                   "time":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
              })
             
             Bank.update()
             print(f"💸{amount} Withdrawn successfully💸")
             print(f"💰Your Current Balance is ₹{userdata['balance']:,}")

     
     #:::::::::::::::::::::::::::::::::::TRANSACTIONS::::::::::::::::::::::::::::::::::::::::::::::

        def transaction_history(self):
               accnum=input("Enter Your Account Number :")
               pin=Bank.masked_input("Enter Your 4 digit PIN :")
               

               userdata=Bank.authenticate(accnum,pin)

               if not userdata:
                    print("❌ Invalid Details")
                    return
               
               if not userdata["transactions"]:
                    print("ℹ️ No transactions found")
                    return
               
               print("\n╔════════════════════════════════════════════════════╗")
               print("║               🧾 TRANSACTION HISTORY               ║")
               print("╠════════════════════════════════════════════════════╣")

               for idx,t in enumerate(userdata["transactions"][::-1],start=1):
                    icon = "➕" if t["type"] == "Deposit" else "➖"
                    print(f"""║ {idx:02d}. {icon} {t['type']:<10} | ₹{t['amount']:<8} | {t['time']} ║
║     🏦 Balance After : ₹{t['balance_after']:<12}           ║
╠════════════════════════════════════════════════════╣""")

               print("║          ✅ End of Transaction History             ║")
               print("╚════════════════════════════════════════════════════╝")



     
     #||||||||||||||||||||||||||||||DEATAILS||||||||||||||||||||||||||||||||||||||||

        def acc_details(self):
             acc=input("Enter Your Account Number :")
             pin=Bank.masked_input("Enter Your 4 Digit PIN :")

             userdata=Bank.authenticate(acc,pin)
             if not userdata:
                  print("❌ Invalid Account Number or PIN ❌")
                  return
             
             print(f"""
                   =======================================
                   🏦       BANK ACCOUNT DETAILS      🏦
                   =======================================
                   👤Account Holder : {userdata['name']}
                   💳Account Number : XXXX-XXXX-{userdata["account_number"][-4:]}
                   💰Balance        : ₹{userdata["balance"]:,}
                   =======================================
                   🙏 Thank you for banking with us
                   =======================================              
""")
             
     #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\UPDATE ACCOUNT DETAILS\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

        def update_acc(self):
             acc=input("Enter Your Account Number :")
             pin=Bank.masked_input("Enter Your 4 digit PIN :")

             userdata=Bank.authenticate(acc,pin)

             if not userdata:
                  print("❌ Invalid Account Number or PIN ❌")
                  return
             
             while True:
                    print("""
════════════════════════════════════════════════
⚙️        UPDATE ACCOUNT INFORMATION MENU       ⚙️
════════════════════════════════════════════════

🔐  1️⃣  Update PIN
📱  2️⃣  Update Mobile Number
📧  3️⃣  Update Email ID
❌  4️⃣  Exit

════════════════════════════════════════════════
""")
                    #-------------update pin--------
                    try:
                         choice=int(input("👉  Please enter your choice :"))
                    except ValueError:
                         print("❌ Invalid input! Enter a number.")
                         continue
                    if choice==1:
                              old=Bank.hash_pin(Bank.masked_input("🔑Enter Your Old PIN :"))

                              if old==userdata["pin"]:
                                   new=Bank.masked_input("🆕Enter Your New PIN :")
                                   confirm=Bank.masked_input("🔁Confirm New PIN :")
                                   if Bank.hash_pin(new)==userdata["pin"]:
                                        print("❌ New PIN cannot be the same as old PIN")
                                        continue
                                   if new==confirm:
                                        if len(new)==4 and new.isdigit():
                                             userdata["pin"]=Bank.hash_pin(new)
                                             Bank.update()
                                             print("✅ Your PIN has been updated successfully!")
                                             continue
                                        else:
                                             print("❌PIN Must Be Exacly 4 Digits")
                                             continue
                                   
                                   else:
                                        print("❌ PINs do not match!")
                                        continue
                              else:
                                   print("You Entered Wrong Old PIN!")
                                   continue
                    #------------------update phone number----------------
                    elif choice==2:
                             old=input("📱 Enter Old Mobile Number : ")
                             if old==userdata["phno"]:
                                  userdata["phno"]=input("📱 Enter New Mobile Number : ")
                                  Bank.update()
                                  print("✅ Mobile number updated successfully!")
                             else:
                                  print("❌Wrong Mobile Number!")
                                  continue
                    #--------------------------UPDATE EMAIL----------------------
                    elif choice==3:
                             old=input("📧 Enter Old Email ID : ")
                             if old==userdata["email"]:
                                  userdata["email"]=input("📧 Enter New Email ID : ")
                                  Bank.update()
                                  print("✅ Email ID updated successfully!")

                    elif choice==4:
                          print("""
════════════════════════════════════════════════
🙏 Thank you! Update process completed.
════════════════════════════════════════════════
""")
                          break
                    else:
                         print("❌ Invalid choice! Please select between 1–4.")


     #'''''''''''''''''''''''''''''''''''DELETE''''''''''''''''''''''''''''''''''''''''''''''''

        def delete_acc(self):
             acc=input("Enter Your Account Number :")
             pin=Bank.masked_input("Enter Your 4 digit PIN :")
             
             userdata=Bank.authenticate(acc,pin)
             if not userdata:
                  print("❌ Invalid Account Number or PIN ❌")
                  return
             #warning
             print(f"\n⚠ Account Number: {acc}")
             print("⚠ This action cannot be undone.")
             #confirmation
             confirm=input("⚠ Are you sure you want to delete your account? (Y/N) :").strip().lower()
             if confirm!="y":
                  print("❎ Account deletion cancelled")
                  return

             Bank.data.remove(userdata) #deleted 
             Bank.update()
             print("✅Your Account Deleted Succesfully")


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>EXIT<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        def exit_system(self):
             print("\nExiting Bank Management System",end="",flush=True)

             for i in range(5):
                  print(".",end="",flush=True) #flush=True forces Python to show output immediately
                  time.sleep(0.4) #Pauses program for 0.4 seconds
             print("""
╔══════════════════════════════════════════╗
║        👋 THANK YOU FOR USING            ║
║        🏦 BANK MANAGEMENT SYSTEM 🏦       ║
╠══════════════════════════════════════════╣
║        Have a great day! 😊               ║
╚══════════════════════════════════════════╝
""")
             sys.exit()

        #----------------------------MAIN MENU---------------------------------------
        def run(self):
          while True:
                         
                         print("""
          ╔══════════════════════════════════════════╗
          ║        🏦 BANK MANAGEMENT SYSTEM 🏦       ║
          ╠══════════════════════════════════════════╣
          ║  1️⃣  Create New Bank Account              ║
          ║  2️⃣  Deposit Money                        ║
          ║  3️⃣  Withdraw Money                       ║
          ║  4️⃣  Transaction History                 ║
          ║  5️⃣  View Account Details                 ║
          ║  6️⃣  Update Account Information           ║
          ║  7️⃣  Delete Account                       ║
          ║  8️⃣  Exit                                ║
          ╚══════════════════════════════════════════╝
          """)

                         try:
                           choice=int(input("Enter Your Choice :"))
                         except ValueError:
                              print("Please Choose A Valid Key")
                              continue

                         if choice==1:
                              self.Create_account()
                              continue
                         elif choice==2:
                              self.depositmoney()
                              continue
                         elif choice==3:
                              self.withdraw_money()
                              continue
                         elif choice==4:
                              self.transaction_history()
                              continue
                         elif choice==5:
                              self.acc_details()
                              continue
                         elif choice==6:
                              self.update_acc()
                              continue
                         elif choice==7:
                              self.delete_acc()
                              continue
                         elif choice==8:
                              self.exit_system()
                         else:
                              print("❌Invalid Choice...")

#======================================RUN SYSTEM==================================
if __name__=="__main__":
     bank=Bank()
     bank.run()
