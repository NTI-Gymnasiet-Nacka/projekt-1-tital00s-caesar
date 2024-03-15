import csv
from tkinter import *
import time

user_choice =""

filepath1 = "./Knas/böcker.csv"
filepath2 = "./Knas/accounts.txt"
purchase_history_file = "purchase_history.txt" 

number_of_articles = 0

File = open(filepath1)
Reader = csv.reader(File)
Data = list(Reader)
del(Data[0])
Shopping_cart = []

list_of_entries = []
for x in list(range(0, len(Data))):
    list_of_entries.append(Data[x][0])       


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
        with open(filepath1, "r") as file:
            lines = file.readlines()

        with open(filepath1, "w") as file:
            for line in lines:
                values = line.strip().split(',')
                if values[0] == str(self.account_username):
                    file.write(f"{self.account_username},{self.account_password},{self.owner},{self.loans}\n")
                else:
                    file.write(line)
    

# Read Function
def read_accounts():
    accounts = {}
    with open(filepath2, "r") as file:
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

            with open(filepath2, "a") as file:
                file.write(f"{new_account_username},{new_password},{new_owner},{new_loans}\{new_loans}\n")

            print("Account created successfully!")
            return new_account

#  Button Functions
def update():
    index = listbox1.curselection()[0]
    namelabel2.config(text=Data[index][0], font=("Arial", 14))
    yearlabel2.config(text=Data[index][1], font=("Arial", 14))
    authorlabel2.config(text=Data[index][2], font=("Arial", 14))

def add_to_shopping_cart():
    global number_of_articles
    selected_index = listbox1.curselection()

    if selected_index:
        selected_row_index = selected_index[0]
        selected_item = list_of_entries[selected_row_index]
        Shopping_cart_listbox.insert(END, f"{Data[selected_row_index][0]} - {Data[selected_row_index][1]} - {Data[selected_row_index][2]}")

        number_of_articles += 1

        numberofbookslabel.config(text=f"Articles : {number_of_articles}")


def delete():
    global number_of_articles
    for index in reversed(Shopping_cart_listbox.curselection()):
        deleted_item_info = Shopping_cart_listbox.get(index)
        deleted_price = float(deleted_item_info.split(' - ')[-1])

        
        number_of_articles -= 1

        Shopping_cart_listbox.delete(index)

        numberofbookslabel.config(text=f"Articles : {number_of_articles}")

def loan():
    global number_of_articles, Shopping_cart

    if number_of_articles == 0:
        print("Your shopping cart is empty. Please add items before loaning.")
        return

    confirmation_message = f"Thank you for loaning books from us!"


    thank_you_label = Label(root, text=confirmation_message, font=("Arial", 14))
    thank_you_label.grid(row=9, column=0, columnspan=3)


    with open(purchase_history_file, 'a') as history_file:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        history_file.write(f"{timestamp} - You loaned: ")       #Lägg till här en funktion call för vad man lånade
        for item in Shopping_cart:
            history_file.write(f"{item}\n")

    Shopping_cart = []
    Shopping_cart_listbox.delete(0, END)

    root.after(5000, thank_you_label.destroy)

def start_window(update, add_to_shopping_cart, delete, loan):
    global listbox1, Shopping_cart_listbox, root, numberofbookslabel, yearlabel2, authorlabel2, namelabel2
    
    #  Tk window creation
    root = Tk()
    root.geometry("800x600")
    root.title("Book Loaning System")

    books = Label(text="Books", font=("Arial", 14))
    books.grid(row=0, column=0)

    loanlist_label = Label(text="Loanlist", font=("Arial", 14))
    loanlist_label.grid(row=0, column=2)

    #  listboxes
    var = StringVar(value=list_of_entries)
    listbox1 = Listbox(root, listvariable=var, bg="#f7ffde", font=("Arial", 14))
    listbox1.grid(row=1, column=0)

    Shopping_cart_listbox = Listbox(root, bg="#f7ffde", font=("Arial", 14))               
    Shopping_cart_listbox.grid(row=1, column=2)
    
    #  Buttons
    button1 = Button(root, text="Info", command=update)
    button1.grid(row=5, column=0)

    addButton = Button(root, text="Add", command=add_to_shopping_cart)
    addButton.grid(row=6, column=0)

    deleteButton = Button(root,text="Delete",command=delete)
    deleteButton.grid(row=7,column=0)

    loanbutton = Button(root, text="Loan", command=loan)
    loanbutton.grid(row=8,column=0)

    #  Meta Labels
    namelabel = Label(root, text="Name : ", font=("Arial", 14)).grid(row=2, column=0, sticky="w")
    yearlabel = Label(root, text="Year : ", font=("Arial", 14)).grid(row=3, column=0, sticky="w")
    authorlabel = Label(root, text="Author : ", font=("Arial", 14)).grid(row=4, column=0, sticky="w")

    numberofbookslabel = Label(root, text=f"Articles : {number_of_articles}", font=("Arial", 14))
    numberofbookslabel.grid(row=2, column=2, sticky="w")


    #  info labels
    namelabel2 = Label(root, text=" - ")
    namelabel2.grid(row=2, column=1, sticky="w")

    yearlabel2 = Label(root, text=" - ")
    yearlabel2.grid(row=3, column=1, sticky="w")

    authorlabel2 = Label(root, text=" - ")
    authorlabel2.grid(row=4, column=1, sticky="w")
    
    root.mainloop()

    #   Menu
if __name__ == "__main__":
    while user_choice != 0:
        print("Welcome to the library ! \n1 : Log in \n2 : Create account \n9 : Quit ")
        user_choice = int(input("Your choice: "))

        if user_choice == 1:
            logged_in_account = login()
            while user_choice != 0:    
                print(f"Account menu for number {logged_in_account.account_username} \n1 : You're Information \n2 : loan books\n4 : Log out")
                user_choice = int(input("Your choice: "))
                if user_choice == 1:
                    logged_in_account.show_details()
                elif user_choice == 2 :
                    start_window(update, add_to_shopping_cart, delete, loan)
                    pass
                elif user_choice == 4:
                    print("Log out")
                    continue

        elif user_choice == 2:
            create_account()

        elif user_choice == 9:
            break