import mysql.connector
import random
import time
import sys
import msvcrt

# Connect to MySQL server (without specifying a database)
try:
    db = mysql.connector.connect(
        host="localhost",       
        user="root",            
        password="Agrim@2003"             
    )
    cursor = db.cursor()

    # Create the database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS icici_bank")

    # Connect to the newly created database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="IVY@rkj12",
        database="icici_bank"
    )
    cursor = db.cursor()

except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit()

# Creating the accounts table if it doesn't already exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    account_number VARCHAR(16) PRIMARY KEY,
    pin INT(4),
    balance FLOAT
)
""")

# A function to insert initial data
def initialize_data():
    initial_data = [
        ("1234567890123456", 1234, 10000),
        ("1234567898765432", 2345, 12000),
        ("1234567890987654", 3456, 17000),
        ("1234567890876543", 4567, 16000),
        ("1234567899876543", 5678, 130000),
        ("1234567887654321", 6789, 10100),
        ("1234567876543219", 7890, 109800),
        ("9876543219876543", 9987, 10760),
        ("9319517847658719", 7777, 15400),
        ("9811292778479258", 2007, 18200)
    ]
    cursor.executemany("INSERT IGNORE INTO accounts (account_number, pin, balance) VALUES (%s, %s, %s)", initial_data)
    db.commit()

initialize_data()

# Function to retrieve account details from the database
def get_account(account_number):
    cursor.execute("SELECT pin, balance FROM accounts WHERE account_number = %s", (account_number,))
    return cursor.fetchone()

# Function to update the balance in the database
def update_balance(account_number, new_balance):
    cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s", (new_balance, account_number))
    db.commit()

# Function to update the PIN in the database
def update_pin(account_number, new_pin):
    cursor.execute("UPDATE accounts SET pin = %s WHERE account_number = %s", (new_pin, account_number))
    db.commit()

# Password masking function (****)
def get_pass(prompt):
    print(prompt, end='', flush=True)
    password = ""
    while True:
        ch = msvcrt.getch()
        if ch in {b'\r', b'\n'}:   # Enter key
            print('')
            break
        elif ch == b'\x08':  # Backspace
            if len(password) > 0:
                password = password[:-1]
                sys.stdout.write('\b \b')
                sys.stdout.flush()
        elif ch == b'\x03':  # Ctrl+C
            raise KeyboardInterrupt
        else:
            try:
                c = ch.decode("utf-8")
            except:
                continue
            password += c
            sys.stdout.write('*')
            sys.stdout.flush()
    return password

# Rest of your code
j = 0
em = {}  # Counting the number of incorrect attempts

def ica(a):
    if a in em:
        em[a] += 1
        if em[a] == 2:
            print("Too many incorrect attempts. Please wait for 10 seconds.")
            time.sleep(10)
            em[a] = 0
    else:
        em[a] = 1

admin_username = "admin"
admin_password = "adminpass"

message = "Welcome to ICICI Bank"
box_width = len(message) + 4
print("*" * box_width)
print("|", message, "|")
print("*" * box_width)

while True:
    print("Choose 1 for user actions")
    print("Choose 2 for admin login")
    print("Choose 3 for exit")
    choice = input()

    try:
        choice_int = int(choice)
        if choice_int == 3:
            print("Terminating the program. Goodbye!")
            break
        elif choice_int == 1:
            message = "Welcome to ICICI Bank User Menu"
            box_width = len(message) + 4
            print("*" * box_width)
            print("|", message, "|")
            print("*" * box_width)
            print("Choose 1 for details")
            print("Choose 2 for making an account")
            print("Choose 3 to go back to the main menu")
            user_choice = input()

            try:
                user_choice_int = int(user_choice)
                if user_choice_int == 3:
                    print("Returning to the main menu.")
                elif user_choice_int == 1:
                    a = input("Please Enter your 16-digit credit/debit card number:\n")
                    account_details = get_account(a)

                    if account_details is None:
                        print("Invalid Card Number. Please enter a valid 16-digit card number.")
                        continue

                    while True:
                        b = get_pass("Please enter your 4-digit ATM PIN:\n")
                        try:
                            b_int = int(b)
                            if b_int == account_details[0]:
                                print("Login successful!")
                                break
                            else:
                                ica(a)
                                print("Login failed. Incorrect PIN.")
                        except ValueError:
                            print("Please enter numeric values only")

                    while True:
                        print("**" * 20)
                        print("|" + " " * 36 + "|")
                        print("|" + " " * 9 + "ICICI Bank User Menu" + " " * 9 + "|")
                        print("|" + " " * 36 + "|")
                        print("**" * 20)
                        print("Choose 1 for changing the ATM PIN")
                        print("Choose 2 for withdrawing money")
                        print("Choose 3 for checking the balance in the account")
                        print("Choose 4 for checking the last five transactions")
                        print("Choose 5 for transferring money")
                        print("Choose 6 to exit the program")

                        z = input()
                        try:
                            z_int = int(z)
                            if 1 <= z_int <= 6:
                                if z_int == 1:
                                    while True:
                                        x = get_pass("Enter your current 4-digit ATM PIN:")
                                        if len(x) == 4 and x == str(account_details[0]):
                                            break
                                        else:
                                            print("Invalid PIN. Please enter the correct current PIN.")

                                    while True:
                                        y = get_pass("Enter your new 4-digit ATM PIN:")
                                        if len(y) == 4:
                                            break
                                        else:
                                            print("Invalid PIN. Please enter a 4-digit PIN.")
                                    while True:
                                        co = get_pass("Enter your new 4-digit ATM PIN again:")
                                        if len(co) == 4:
                                            break
                                        else:
                                            print("Invalid PIN. Please enter a 4-digit PIN.")

                                    if x != y and y == co:
                                        update_pin(a, int(y))
                                        print("Your ATM PIN has been changed successfully.")
                                    else:
                                        print("New PIN is the same as the current PIN or you entered your new PIN wrong the second time.")
                                elif z_int == 2:
                                    while True:
                                        b = input("Enter the amount of money you want to withdraw:\n")
                                        try:
                                            b_int = int(b)
                                            if b_int <= 20000:
                                                new_balance = account_details[1] - b_int
                                                update_balance(a, new_balance)
                                                print("Withdrawal successful. Remaining balance:", new_balance)
                                                break
                                            else:
                                                print("Amount entered is more than 20,000 INR. Enter an amount less than 20,000.")
                                        except ValueError:
                                            print("Please enter a numeric value.")
                                elif z_int == 3:
                                    print("Account Number:", a, "Balance:", account_details[1])
                                elif z_int == 4:
                                    print("Transaction history:")
                                    print("Your debit card transaction:", random.randint(10, 100000000))
                                    print("Your credit card transaction:", random.randint(100, 100000000))
                                    print("Your debit card transaction:", random.randint(10, 100000000))
                                    print("Your credit card transaction:", random.randint(100, 100000000))
                                    print("Your debit card transaction:", random.randint(10, 100000000))
                                    print("Thank You!\nCome Again")
                                elif z_int == 5:
                                    while True:
                                        f = input("Enter the 16-digit ATM card number to which you want to send the money:\n")
                                        recipient_details = get_account(f)

                                        if recipient_details is None:
                                            print("Invalid recipient account number.")
                                            break

                                        while True:
                                            try:
                                                amount = int(input("Enter the amount of money you want to transfer:\n"))
                                                if amount > account_details[1]:
                                                    print("Insufficient funds for the transfer.")
                                                    break
                                                else:
                                                    new_sender_balance = account_details[1] - amount
                                                    new_recipient_balance = recipient_details[1] + amount

                                                    update_balance(a, new_sender_balance)
                                                    update_balance(f, new_recipient_balance)

                                                    print(amount, "transferred successfully from", a, "to", f)
                                                    print("Remaining balance:", new_sender_balance)
                                                    break
                                            except ValueError:
                                                print("Please enter a numeric value.")
                                        break
                                elif z_int == 6:
                                    print("Thank you for using our ATM!!")
                                    break
                            else:
                                print("Please enter a valid number (1 to 6).")
                        except ValueError:
                            print("Please enter a numeric value.")
                elif user_choice_int == 2:
                    na = input("Please Enter your 16-digit credit/debit card number:\n")
                    try:
                        na_int = int(na)
                        if len(na) == 16 and get_account(na) is None:
                            np = get_pass("Enter a 4-digit PIN for the new account: ")
                            np_int = int(np)

                            initial_balance = float(input("Enter the initial balance for the new account: "))
                            cursor.execute("INSERT INTO accounts (account_number, pin, balance) VALUES (%s, %s, %s)", (na, np_int, initial_balance))
                            db.commit()

                            print("Account", na, "created successfully.")
                        else:
                            print("Invalid Card Number or Account already exists. Please enter a unique 16-digit number.")
                    except ValueError:
                        print("Please enter numeric values only")
                else:
                    print("Please enter a valid number (1, 2, or 3).")
            except ValueError:
                print("Please enter a numeric value.")

        elif choice_int == 2:
            admin_user = input("Enter admin username: ")
            admin_pass = get_pass("Enter admin password: ")

            if admin_user == admin_username and admin_pass == admin_password:
                message = "Welcome to ICICI Bank Admin Menu"
                box_width = len(message) + 4
                print("*" * box_width)
                print("|", message, "|")
                print("*" * box_width)
                print("Admin login successful!")

                while True:
                    print("Choose 1 for sorting accounts")
                    print("Choose 2 for viewing all accounts")
                    print("Choose 3 for searching an account")
                    print("Choose 4 for changing admin password")
                    print("Choose 5 to go back to the main menu")

                    admin_choice = input()

                    try:
                        admin_choice_int = int(admin_choice)
                        if admin_choice_int == 5:
                            print("Returning to the main menu.")
                            break
                        elif admin_choice_int == 1:
                            cursor.execute("SELECT account_number, balance FROM accounts ORDER BY account_number")
                            sorted_accounts = cursor.fetchall()
                            print("Sorted Accounts:")
                            for account, balance in sorted_accounts:
                                print("Account:", account, "Balance:", balance)
                        elif admin_choice_int == 2:
                            cursor.execute("SELECT account_number, balance FROM accounts")
                            all_accounts = cursor.fetchall()
                            print("All Accounts:")
                            for account, balance in all_accounts:
                                print("Account:", account, "Balance:", balance)
                        elif admin_choice_int == 3:
                            search_account = input("Enter the account number to search: ")
                            account_details = get_account(search_account)
                            if account_details:
                                print("Account", search_account, "found. Balance:", account_details[1])
                            else:
                                print("Account", search_account, "not found.")
                        elif admin_choice_int == 4:
                            new_admin_pass = get_pass("Enter the new admin password: ")
                            admin_password = new_admin_pass
                            print("Admin password changed successfully.")
                        else:
                            print("Please enter a valid number (1, 2, 3, 4, or 5).")
                    except ValueError:
                        print("Please enter a numeric value.")
            else:
                print("Admin login failed. Incorrect username or password.")
        else:
            print("Please enter a valid number (1, 2, or 3).")
    except ValueError:
        print("Please enter a numeric value.")

input()
