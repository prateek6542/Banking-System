# 💻 DigiBank - Console-Based Banking System 🏦

A simple yet fully functional console-based banking system written in Python. DigiBank allows users to create accounts, deposit and withdraw money, view transaction history, and download transaction history as a PDF — all from the terminal.

---

## 📜 Project Description

DigiBank is a text-based banking system developed using core Python. It simulates the basic functionalities of a bank such as account creation, secure login, deposits, withdrawals, transaction logs, and exporting history to PDF. It uses local JSON files to store account and transaction data persistently.

---

## ✨ Features Implemented

- 🔐 **User Authentication** with password hashing (SHA256)
- 🆕 **Create Account** with unique account number generation
- 💰 **Deposit and Withdraw Money**
- 📜 **View Transaction History** with date and type
- 💾 **Data Persistence** using `accounts.json` and `transactions.json`
- 🎨 **Color-coded UI** using `colorama` for better CLI experience

---

## 🚀 How to Run the Project

### 🔧 Run from Terminal

1. Open terminal or command prompt.
2. Navigate to the project directory.
3. Run the main file:

```bash
python banking_system.py
```
## 🛠️ Installation Instructions

### 🐍 Prerequisites

Python 3.x

colorama (for colored CLI)


### 📦 Install Required Packages

Run the following command in your terminal:

```bash
pip install colorama
```

## 🧪 Sample Menu (User Console)

### 🏦  Welcome to DigiBank – Your Console. Your Control. 🏦
------------------------------------------------------------
1. 🆕 Create New Account
2. 🔐 Login to Existing Account
3. ❌ Exit

### 🧠 Inspired By
This project was built to demonstrate how core concepts like file handling, and password hashing can be used to create real-world applications in Python.
