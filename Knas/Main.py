import csv
from tkinter import Tk

user_choice =""

#Error messages
class AccountNotFoundError(Exception):
    pass

class GeneralError(Exception):
    pass

#Parent Class
class Account:  
    def __init__(self, account_username, owner, account_password, loans):
        self.account_username = account_username
        self.owner = owner
        self.account_password = account_password
        self.loans = loans

    def show_details(self):
        print("Account Details \n")
        print(f"Account Number: {self.account_username} \nOwner: {self.owner} \nLoans: {self.loans}")

#Child class
class ClientAccount(Account):
    def __init__(self, account_username, owner, account_password, loans, transaction_history=None):
        super().__init__(account_username, owner, account_password, loans)
        self.transaction_history = transaction_history or []

    def show_details(self):
        super().show_details()
        print(f"Transaction History: {self.transaction_history}")

    def update_file(self):
        with open("./Knas/accounts.txt", "r") as file:
            lines = file.readlines()

        with open("./Knas/accounts.txt", "w") as file:
            for line in lines:
                values = line.strip().split(',')
                if values[0] == str(self.account_username):
                    file.write(f"{self.account_username},{self.account_password},{self.owner},{self.loans}\n")
                else:
                    file.write(line)
    

# Read Function
def read_accounts():
    accounts = {}
    with open("./Knas/accounts.txt", "r") as file:
        for line in file:
            values = line.strip().split(',')
            if len(values) == 4:            #kollar på längden i txtfilen så att allt finns med
                account_username, password, owner, loans = values
                accounts[account_username] = ClientAccount(account_username, owner, password, (loans))
    return accounts

# Login Function
def login():
    accounts = read_accounts()

    while True:
        account_username = input("Enter your account number: ")
        password = input("Enter your password: ")

        if account_username in accounts and accounts[account_username].account_password == password:
            print("Login successful!")
            return accounts[account_username]
        else:
            print("Invalid account number or password. Please try again.")

# Create account function
def create_account():
    accounts = read_accounts()

    while True:
        new_account_username = input("Enter a new account number: ")

        if new_account_username in accounts:
            print("Account number already exists. Please choose a different one.")
        else:
            new_password = input("Set a password for the new account: ")
            new_owner = input("Set an owner for the new account: ")
            new_loans = 0
            new_account = ClientAccount(new_account_username, new_owner, new_password, new_loans)
            accounts[new_account_username] = new_account

            with open("./Knas/accounts.txt", "a") as file:
                file.write(f"{new_account_username},{new_password},{new_owner},{new_loans}\{new_loans}\n")

            print("Account created successfully!")
            return new_account


if __name__ == "__main__":
    while user_choice != 0:
        print("Welcome to the library ! \n1 : Log in \n2 : Create account \n9 : Quit ")
        user_choice = int(input("Your choice: "))

        if user_choice == 1:
            logged_in_account = login()
            print(f"Account menu for number {logged_in_account.account_username} \n1 : Check value \n2 : Withdraw \n3 : Deposit \n4 : Transaction history \n5 : Log out")
            user_choice = int(input("Your choice: "))

            if user_choice == 1:
                logged_in_account.show_details()
            elif user_choice == 2:
                withdraw_amount = float(input("Enter the amount to withdraw: "))
                logged_in_account.withdraw(withdraw_amount)
            elif user_choice == 3:
                deposit_amount = float(input("Enter the amount to deposit: "))
                logged_in_account.deposit(deposit_amount)
            elif user_choice == 4:
                print(f"Transaction history: {logged_in_account.transaction_history}")
            elif user_choice == 5:
                print("Log out")
                continue

        elif user_choice == 2:
            create_account()

        elif user_choice == 9:
            break