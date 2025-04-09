import json
import hashlib
import os
from datetime import datetime
from getpass import getpass
from colorama import init, Fore

# Initialize Colorama for colored text in terminal
init(autoreset=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ACCOUNTS_FILE = os.path.join(BASE_DIR, "accounts.json")
TRANSACTIONS_FILE = os.path.join(BASE_DIR, "transactions.json")

# Clear screen function
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
# Pause until the user presses enter
def pause():
    input("\n🔄 Press Enter to continue...")
    
# Convert password to hashed value for secure storage
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load JSON data from the file
def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Save JSON data to file with  formatting
def save_data(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f,ensure_ascii=False, indent=4)

# Auto-generate unique account number
def generate_account_number():
    accounts = load_data(ACCOUNTS_FILE)
    if not accounts:
        return "100001"
    last_account = accounts[-1]
    return str(int(last_account['account_number']) + 1)

# Function to create a new account
def create_account():
    clear_screen()
    print(Fore.CYAN + "\n🔹 Create a New Bank Account 🔹")
    name = input("👤 Enter your name: ")
    initial_deposit = input("💵 Enter your initial deposit: ")

    try:
        initial_deposit = float(initial_deposit)
        if initial_deposit < 0:
            print(Fore.RED + "❌ Initial deposit must be non-negative.")
            pause()
            return
    except ValueError:
        print(Fore.RED + "❌ Invalid amount.")
        pause()
        return

    password = getpass("🔑 Enter your password: ")
    hashed_password = hash_password(password)
    account_number = generate_account_number()

    # Load existing accounts and append a new one
    accounts = load_data(ACCOUNTS_FILE)
    accounts.append({
        "account_number": account_number,
        "name": name,
        "password": hashed_password,
        "balance": initial_deposit
    })
    save_data(ACCOUNTS_FILE, accounts)

    record_transaction(account_number, "CREATED", initial_deposit)

    print(Fore.GREEN + f"\n✅ Account created successfully! Your account number is {account_number}")
    pause()

# Login logic with password validation
def login():
    clear_screen()
    print("🔐 Login to Your Account")
    account_number = input("Enter your account number: ").strip()
    password = getpass("Enter your password: ").strip()

    hashed_input_password = hash_password(password)
    accounts = load_data(ACCOUNTS_FILE)

    for acc in accounts:
        if acc["account_number"] == account_number:
            if acc["password"] == hashed_input_password:
                print("✅ Login successful!")
                pause()
                return acc["account_number"], acc["name"], acc["balance"]
            else:
                print("❌ Wrong password.")
                pause()
                return None, None, None

    print("❌ User does not exist.")
    pause()
    return None, None, None

# Save transaction to file with timestamp
def record_transaction(account_number, transaction_type, amount):
    transactions = load_data(TRANSACTIONS_FILE)
    transactions.append({
        "account_number": account_number,
        "type": transaction_type,
        "amount": f"₹{amount}",
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    save_data(TRANSACTIONS_FILE, transactions)

# Deposit logic with balance update
def deposit(account_number):
    clear_screen()
    print(Fore.YELLOW + "\n💰 Deposit Money")
    accounts = load_data(ACCOUNTS_FILE)

    for acc in accounts:
        if acc["account_number"] == account_number:
            try:
                amount = float(input("➕ Enter amount to deposit: "))
                if amount <= 0:
                    print(Fore.RED + "❌ Invalid amount. Enter a positive number.")
                    pause()
                    return
            except ValueError:
                print(Fore.RED + "❌ Invalid input. Please enter a valid number.")
                pause()
                return

            acc["balance"] += amount
            save_data(ACCOUNTS_FILE, accounts)
            record_transaction(account_number, "DEPOSIT", amount)
            print(Fore.GREEN + f"✅ Deposit successful! New balance: ₹{acc['balance']}")
            pause()
            return

    print(Fore.RED + "❌ Account not found.")
    pause()

# Withdrawal logic with validation for sufficient balance
def withdrawal(account_number):
    clear_screen()
    print(Fore.YELLOW + "\n💸 Withdraw Money")
    accounts = load_data(ACCOUNTS_FILE)

    for acc in accounts:
        if acc["account_number"] == account_number:
            try:
                amount = float(input("➖ Enter amount to withdraw: "))
                if amount <= 0:
                    print(Fore.RED + "❌ Invalid amount. Enter a positive number.")
                    pause()
                    return
            except ValueError:
                print(Fore.RED + "❌ Invalid input. Please enter a valid number.")
                pause()
                return

            if amount > acc["balance"]:
                print(Fore.RED + "❌ Insufficient funds!")
                pause()
                return

            acc["balance"] -= amount
            save_data(ACCOUNTS_FILE, accounts)
            record_transaction(account_number, "WITHDRAWAL", amount)
            print(Fore.GREEN + f"✅ Withdrawal successful! New balance: ₹{acc['balance']}")
            pause()
            return

    print(Fore.RED + "❌ Account not found.")
    pause()

# Display all transactions for a given account
def display_transaction_summary(account_number):
    clear_screen()
    print(Fore.CYAN + "\n📜 Transaction History")
    print(Fore.BLUE + "─" * 60)

    transactions = load_data(TRANSACTIONS_FILE)
    accounts = load_data(ACCOUNTS_FILE)

    found = False
    for txn in transactions:
        if txn["account_number"] == account_number:
            found = True
            date = txn["timestamp"].split()[0]
            print(f"📅 {date}  |  🔁 {txn['type'].ljust(11)} | 💵 {txn['amount']}")

    balance = next((acc["balance"] for acc in accounts if acc["account_number"] == account_number), 0)

    if not found:
        print(Fore.RED + "❌ No transaction history found.")

    print(Fore.BLUE + "─" * 60)
    print(Fore.GREEN + f"{'':>30}💰 Current Balance: ₹{balance:.2f}")
    print(Fore.BLUE + "─" * 60)
    pause()

# Main menu 
def main():
    while True:
        clear_screen()
        print(Fore.MAGENTA + "\n" + "═" * 60)
        print(Fore.CYAN + "🏦  Welcome to DigiBank – Your Console. Your Control. 🏦".center(60))
        print(Fore.MAGENTA + "═" * 60)
        print(Fore.YELLOW + "1. 🆕 Create New Account")
        print("2. 🔐 Login to Existing Account")
        print("3. ❌ Exit")
        print(Fore.MAGENTA + "─" * 60)

        choice = input(Fore.BLUE + "📥 Enter your choice (1-3): ")

        if choice == "1":
            create_account()
        elif choice == "2":
            account_number, name, balance = login()
            if account_number:
                while True:
                    clear_screen()
                    print(Fore.MAGENTA + "\n" + "═" * 60)
                    print(Fore.CYAN + f"🔓 Logged in as: {name}  |  Account No: {account_number}".center(60))
                    print(Fore.MAGENTA + "═" * 60)
                    print(Fore.YELLOW + "1. 💰 Deposit Money")
                    print("2. 💸 Withdraw Money")
                    print("3. 📜 View Transaction History")
                    print("4. 🔒 Logout")
                    print(Fore.MAGENTA + "─" * 60)

                    action = input(Fore.BLUE + "📥 Choose an option (1-4): ")

                    if action == "1":
                        deposit(account_number)
                    elif action == "2":
                        withdrawal(account_number)
                    elif action == "3":
                        display_transaction_summary(account_number)
                    elif action == "4":
                        print(Fore.CYAN + "🔒 Logging out....")
                        pause()
                        break
        elif choice == "3":
            clear_screen()
            print(Fore.CYAN + "👋 Thank you for using DigiBank. Goodbye!")
            pause()
            break

if __name__ == "__main__":
    main()
