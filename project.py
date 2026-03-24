import sys
import os

# Placeholder for core bank management logic
# You will need to refactor your existing 'bank-management-system/project.py'
# into a set of functions or a class here, or import it if it's already structured well.

# Example:
# from bank_management_system.project import BankManager # Assuming project.py contains a BankManager class
# or
# def create_account(name, initial_deposit):
#     # ... your existing logic ...
#     pass
# def deposit(account_id, amount):
#     # ... your existing logic ...
#     pass
# # etc.

class BankCore:
    def __init__(self):
        # A simple in-memory storage for demonstration. 
        # You should replace this with your actual data persistence logic (e.g., database, file system).
        self.accounts = {}

    def create_account(self, name, initial_deposit):
        if name in self.accounts:
            return False, "Account with this name already exists."
        if not isinstance(initial_deposit, (int, float)) or initial_deposit < 0:
            return False, "Initial deposit must be a non-negative number."
        self.accounts[name] = {"balance": initial_deposit, "transactions": [f"Initial deposit: {initial_deposit}"]}
        return True, f"Account '{name}' created with balance {initial_deposit}."

    def deposit(self, name, amount):
        if name not in self.accounts:
            return False, "Account not found."
        if not isinstance(amount, (int, float)) or amount <= 0:
            return False, "Deposit amount must be a positive number."
        self.accounts[name]["balance"] += amount
        self.accounts[name]["transactions"].append(f"Deposit: {amount}")
        return True, f"Deposited {amount} to '{name}'. New balance: {self.accounts[name]['balance']}."

    def withdraw(self, name, amount):
        if name not in self.accounts:
            return False, "Account not found."
        if not isinstance(amount, (int, float)) or amount <= 0:
            return False, "Withdrawal amount must be a positive number."
        if self.accounts[name]["balance"] < amount:
            return False, "Insufficient funds."
        self.accounts[name]["balance"] -= amount
        self.accounts[name]["transactions"].append(f"Withdrawal: {amount}")
        return True, f"Withdrew {amount} from '{name}'. New balance: {self.accounts[name]['balance']}."

    def check_balance(self, name):
        if name not in self.accounts:
            return False, "Account not found."
        return True, self.accounts[name]["balance"]

    def get_transactions(self, name):
        if name not in self.accounts:
            return False, "Account not found."
        return True, self.accounts[name]["transactions"]

# --- Command Line Interface (CLI) ---
def run_cli(bank_core):
    print("\nWelcome to the Bank Management System (CLI)")
    while True:
        print("\nOptions:")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. View Transactions")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter account name: ")
            try:
                initial_deposit = float(input("Enter initial deposit amount: "))
                success, message = bank_core.create_account(name, initial_deposit)
                print(message)
            except ValueError:
                print("Invalid amount. Please enter a number.")
        elif choice == '2':
            name = input("Enter account name: ")
            try:
                amount = float(input("Enter deposit amount: "))
                success, message = bank_core.deposit(name, amount)
                print(message)
            except ValueError:
                print("Invalid amount. Please enter a number.")
        elif choice == '3':
            name = input("Enter account name: ")
            try:
                amount = float(input("Enter withdrawal amount: "))
                success, message = bank_core.withdraw(name, amount)
                print(message)
            except ValueError:
                print("Invalid amount. Please enter a number.")
        elif choice == '4':
            name = input("Enter account name: ")
            success, result = bank_core.check_balance(name)
            if success:
                print(f"Account '{name}' balance: {result}")
            else:
                print(result)
        elif choice == '5':
            name = input("Enter account name: ")
            success, result = bank_core.get_transactions(name)
            if success:
                print(f"Transactions for '{name}':")
                for t in result:
                    print(f"- {t}")
            else:
                print(result)
        elif choice == '6':
            print("Exiting CLI. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# --- Graphical User Interface (GUI) ---
def run_gui(bank_core):
    try:
        import tkinter as tk
        from tkinter import messagebox, simpledialog
    except ImportError:
        print("tkinter is not installed or available. Please install it (e.g., `!apt-get install python3-tk`) or run in CLI mode.")
        return

    root = tk.Tk()
    root.title("Bank Management System (GUI)")
    root.geometry("400x300")

    # Helper function to get account name
    def get_account_name():
        return simpledialog.askstring("Account Name", "Enter account name:")

    # Helper function to get amount
    def get_amount_input(action):
        amount_str = simpledialog.askstring(f"{action} Amount", f"Enter {action.lower()} amount:")
        if amount_str:
            try:
                return float(amount_str)
            except ValueError:
                messagebox.showerror("Error", "Invalid amount. Please enter a number.")
        return None

    def create_account_gui():
        name = get_account_name()
        if name:
            initial_deposit = get_amount_input("Initial Deposit")
            if initial_deposit is not None:
                success, message = bank_core.create_account(name, initial_deposit)
                if success:
                    messagebox.showinfo("Create Account", message)
                else:
                    messagebox.showerror("Create Account Failed", message)

    def deposit_gui():
        name = get_account_name()
        if name:
            amount = get_amount_input("Deposit")
            if amount is not None:
                success, message = bank_core.deposit(name, amount)
                if success:
                    messagebox.showinfo("Deposit", message)
                else:
                    messagebox.showerror("Deposit Failed", message)

    def withdraw_gui():
        name = get_account_name()
        if name:
            amount = get_amount_input("Withdrawal")
            if amount is not None:
                success, message = bank_core.withdraw(name, amount)
                if success:
                    messagebox.showinfo("Withdraw", message)
                else:
                    messagebox.showerror("Withdraw Failed", message)

    def check_balance_gui():
        name = get_account_name()
        if name:
            success, result = bank_core.check_balance(name)
            if success:
                messagebox.showinfo("Check Balance", f"Account '{name}' balance: {result}")
            else:
                messagebox.showerror("Check Balance Failed", result)
                
    def view_transactions_gui():
        name = get_account_name()
        if name:
            success, result = bank_core.get_transactions(name)
            if success:
                transactions_str = "\n".join(result)
                messagebox.showinfo("Transactions", f"Transactions for '{name}':\n{transactions_str}")
            else:
                messagebox.showerror("View Transactions Failed", result)

    tk.Label(root, text="Bank Management System", font=("Arial", 16)).pack(pady=10)

    tk.Button(root, text="Create Account", command=create_account_gui).pack(pady=5, fill=tk.X, padx=20)
    tk.Button(root, text="Deposit", command=deposit_gui).pack(pady=5, fill=tk.X, padx=20)
    tk.Button(root, text="Withdraw", command=withdraw_gui).pack(pady=5, fill=tk.X, padx=20)
    tk.Button(root, text="Check Balance", command=check_balance_gui).pack(pady=5, fill=tk.X, padx=20)
    tk.Button(root, text="View Transactions", command=view_transactions_gui).pack(pady=5, fill=tk.X, padx=20)
    tk.Button(root, text="Exit", command=root.quit).pack(pady=10, fill=tk.X, padx=20)

    messagebox.showinfo("GUI Mode", "GUI is running. Please interact using the buttons and input dialogs.")
    root.mainloop()


# --- Main Application Logic ---
def main():
    bank_core = BankCore() # Initialize your core banking logic

    print("\nChoose interface:")
    print("1. Command Line Interface (CLI)")
    print("2. Graphical User Interface (GUI)")
    print("3. Exit")

    # interface_choice = input("Enter your choice (1/2/3): ")
    interface_choice = '1' # Auto-select CLI for Colab environment

    if interface_choice == '1':
        run_cli(bank_core)
    elif interface_choice == '2':
        run_gui(bank_core)
    elif interface_choice == '3':
        print("Exiting application. Goodbye!")
        sys.exit(0)
    else:
        print("Invalid choice. Please run the script again and choose 1, 2, or 3.")
        sys.exit(1)

if __name__ == "__main__":
    # Check if 'bank-management-system/project.py' exists
    project_path = "/content/bank-management-system/project.py"
    if os.path.exists(project_path):
        print(f"Detected '{project_path}'. You should integrate its core logic into the 'BankCore' class above.")
        print("If 'project.py' already defines functions like create_account, deposit, etc., you can replace the placeholder methods in BankCore.")
        print("Alternatively, you can import and use them directly within BankCore methods.")
    else:
        print("Could not find 'bank-management-system/project.py'. Using a basic BankCore implementation.")

    # To run the GUI in Colab, you might need to install tkinter first if it's not present.
    # For example, run: !apt-get install python3-tk

    main()
