from bank import Bank

bank = Bank()

while True:
    print("""
1. Create Account
2. Deposit
3. Withdraw
4. Transaction History
5. Exit
""")

    choice = input("Choice : ")

    if choice == "1":
        bank.create_account()
    elif choice == "2":
        bank.deposit()
    elif choice == "3":
        bank.withdraw()
    elif choice == "4":
        bank.history()
    elif choice == "5":
        break
    else:
        print("❌ Invalid choice")
