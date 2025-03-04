import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class FinanceTracker:
    def __init__(self, master):
        self.master = master
        master.title("Personal Finance Tracker")
        master.geometry("800x600")  # Increased window size
        master.configure(bg="#f0f0f0")  # Light background

        self.transactions = []

        # --- Styling ---
        self.font_title = ("Helvetica", 16, "bold")
        self.font_label = ("Arial", 12)
        self.font_entry = ("Arial", 12)
        self.button_style = "Accent.TButton"  # Use ttk themed button

        # --- Variables ---
        self.category_options = ["Food", "Transport", "Rent", "Salary", "Other"]
        self.type_options = ["Income", "Expense"]  # Added Income/Expense type
        self.date_format = "%Y-%m-%d"
        self.amount_var = tk.StringVar()
        self.date_var = tk.StringVar(value=datetime.now().strftime(self.date_format))
        self.category_var = tk.StringVar(value=self.category_options[0])
        self.type_var = tk.StringVar(value=self.type_options[0])  # Default to Income
        self.description_var = tk.StringVar()

        # --- UI Elements ---
        self.create_header()
        self.create_input_fields()
        self.create_transaction_list()
        self.create_summary()

        # --- Initialize ttk style ---
        self.style = ttk.Style()
        self.style.configure(self.button_style, background="#4CAF50", foreground="black", font=("Arial", 10, "bold"))
        self.style.map(self.button_style, background=[("active", "#388E3C")])  # Darken on hover

    def create_header(self):
        # Header Frame
        header_frame = tk.Frame(self.master, bg="#3498db")  # Blue header
        header_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

        self.header_label = tk.Label(header_frame, text="💰 Personal Finance Tracker 💰", font=self.font_title, bg="#3498db", fg="white")
        self.header_label.pack(pady=10)

    def create_input_fields(self):
        # Input Frame
        input_frame = tk.Frame(self.master, bg="#f0f0f0")
        input_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=5)

        # Amount
        amount_label = tk.Label(input_frame, text="Amount:", font=self.font_label, bg="#f0f0f0")
        amount_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.amount_entry = tk.Entry(input_frame, textvariable=self.amount_var, font=self.font_entry)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Date
        date_label = tk.Label(input_frame, text="Date (YYYY-MM-DD):", font=self.font_label, bg="#f0f0f0")
        date_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.date_entry = tk.Entry(input_frame, textvariable=self.date_var, font=self.font_entry)
        self.date_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Category
        category_label = tk.Label(input_frame, text="Category:", font=self.font_label, bg="#f0f0f0")
        category_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.category_dropdown = ttk.Combobox(input_frame, textvariable=self.category_var, values=self.category_options, font=self.font_entry, state="readonly")
        self.category_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Type (Income/Expense)
        type_label = tk.Label(input_frame, text="Type:", font=self.font_label, bg="#f0f0f0")
        type_label.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.type_dropdown = ttk.Combobox(input_frame, textvariable=self.type_var, values=self.type_options, font=self.font_entry, state="readonly")
        self.type_dropdown.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        # Description
        description_label = tk.Label(input_frame, text="Description:", font=self.font_label, bg="#f0f0f0")
        description_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.description_entry = tk.Entry(input_frame, textvariable=self.description_var, font=self.font_entry)
        self.description_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Add Button
        self.add_button = ttk.Button(input_frame, text="Add Transaction", command=self.add_transaction, style=self.button_style)
        self.add_button.grid(row=2, column=4, pady=5, padx=5, sticky="ew") # Adjusted padding and sticky

        # Configure column weights to make the input fields expand
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(3, weight=1)
        input_frame.columnconfigure(4, weight=0)  # Button column does not expand

    def create_transaction_list(self):
        # Treeview Frame
        tree_frame = tk.Frame(self.master)
        tree_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=10, pady=5)

        # Treeview widget
        self.tree = ttk.Treeview(tree_frame, columns=("Amount", "Date", "Category", "Type", "Description"), show="headings") # Added Type column
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Type", text="Type")  # Type heading
        self.tree.heading("Description", text="Description")

        # Column widths and resizability
        self.tree.column("Amount", width=100, stretch=False)
        self.tree.column("Date", width=100, stretch=False)
        self.tree.column("Category", width=100, stretch=False)
        self.tree.column("Type", width=80, stretch=False)  # Type column width
        self.tree.column("Description", width=200, stretch=True)

        self.tree.pack(expand=True, fill="both")

        # Edit and Delete buttons
        button_frame = tk.Frame(self.master, bg="#f0f0f0")
        button_frame.grid(row=3, column=0, columnspan=3, pady=5)

        self.edit_button = ttk.Button(button_frame, text="Edit", command=self.edit_transaction, style=self.button_style)
        self.edit_button.grid(row=0, column=0, padx=10)

        self.delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_transaction, style=self.button_style)
        self.delete_button.grid(row=0, column=1, padx=10)

        # Category Filter
        filter_label = tk.Label(button_frame, text="Filter by Category:", font=self.font_label, bg="#f0f0f0")
        filter_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.filter_var = tk.StringVar(value="All")
        self.filter_dropdown = ttk.Combobox(button_frame, textvariable=self.filter_var, values=["All"] + self.category_options, font=self.font_entry, state="readonly", width=12)
        self.filter_dropdown.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.filter_dropdown.bind("<<ComboboxSelected>>", self.update_transaction_list)  # Update on selection

        # Configure row and column weights for resizing
        self.master.rowconfigure(2, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=1)

    def create_summary(self):
        # Summary Frame
        summary_frame = tk.Frame(self.master, bg="#e0e0e0")
        summary_frame.grid(row=4, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

        self.total_income_label = tk.Label(summary_frame, text="Total Income: $0", font=self.font_label, bg="#e0e0e0")
        self.total_income_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.total_expenses_label = tk.Label(summary_frame, text="Total Expenses: $0", font=self.font_label, bg="#e0e0e0")
        self.total_expenses_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        self.balance_label = tk.Label(summary_frame, text="Balance: $0", font=self.font_label, bg="#e0e0e0")
        self.balance_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        for i in range(3):
            summary_frame.columnconfigure(i, weight=1)

        self.update_summary()

    def update_summary(self):
        total_income = sum(t["amount"] for t in self.transactions if t["amount"] > 0)
        total_expenses = abs(sum(t["amount"] for t in self.transactions if t["amount"] < 0))
        balance = total_income - total_expenses

        self.total_income_label.config(text=f"Total Income: ${total_income:.2f}")
        self.total_expenses_label.config(text=f"Total Expenses: ${total_expenses:.2f}")
        self.balance_label.config(text=f"Balance: ${balance:.2f}")

    def add_transaction(self):
        amount = self.amount_var.get()
        date_str = self.date_var.get()
        category = self.category_var.get()
        type = self.type_var.get()  # Get the selected type (Income/Expense)
        description = self.description_var.get()

        # Input Validation
        if not amount or not date_str or not category or not type:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            amount = float(amount)
            datetime.strptime(date_str, self.date_format)  # Validate date format
        except ValueError:
            messagebox.showerror("Error", "Invalid amount or date format.")
            return

        # Determine the sign based on the selected type
        if type == "Income":
            amount = abs(amount)  # Ensure income is positive
        else:
            amount = -abs(amount)  # Ensure expenses are negative

        transaction = {"amount": amount, "date": date_str, "category": category, "type": type, "description": description}  # Added type
        self.transactions.append(transaction)
        self.update_transaction_list()
        self.update_summary()

        # Clear input fields
        self.amount_var.set("")
        self.description_var.set("")
        self.date_var.set(datetime.now().strftime(self.date_format))

    def edit_transaction(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select a transaction to edit.")
            return

        selected_index = self.tree.index(selected_item[0])
        transaction = self.transactions[selected_index]

        # Populate input fields with selected transaction's data
        self.amount_var.set(abs(transaction["amount"]))  # Show amount as positive for editing
        self.date_var.set(transaction["date"])
        self.category_var.set(transaction["category"])
        self.type_var.set(transaction["type"])  # Set the transaction type in the dropdown
        self.description_var.set(transaction["description"])

        # Create a function to save the edited transaction
        def save_edit():
            amount = self.amount_var.get()
            date_str = self.date_var.get()
            category = self.category_var.get()
            type = self.type_var.get()  # Get type from edit window
            description = self.description_var.get()

            if not amount or not date_str or not category or not type:
                messagebox.showerror("Error", "Please fill in all fields.")
                return

            try:
                amount = float(amount)
                datetime.strptime(date_str, self.date_format)
            except ValueError:
                messagebox.showerror("Error", "Invalid amount or date format.")
                return

            # Determine the sign based on the selected type
            if type == "Income":
                amount = abs(amount)  # Ensure income is positive
            else:
                amount = -abs(amount)  # Ensure expenses are negative

            # Update the transaction
            transaction["amount"] = amount
            transaction["date"] = date_str
            transaction["category"] = category
            transaction["type"] = type  # Update the transaction type
            transaction["description"] = description

            self.transactions[selected_index] = transaction
            self.update_transaction_list()
            self.update_summary()

            # Clear input fields and destroy the edit window
            self.amount_var.set("")
            self.date_var.set(datetime.now().strftime(self.date_format))
            self.description_var.set("")
            edit_window.destroy()

        # Create a new window for editing
        edit_window = tk.Toplevel(self.master)
        edit_window.title("Edit Transaction")
        edit_window.geometry("400x250")
        edit_window.configure(bg="#f0f0f0")

        # UI elements for the edit window
        amount_label = tk.Label(edit_window, text="Amount:", font=self.font_label, bg="#f0f0f0")
        amount_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        amount_entry = tk.Entry(edit_window, textvariable=self.amount_var, font=self.font_entry)
        amount_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        date_label = tk.Label(edit_window, text="Date (YYYY-MM-DD):", font=self.font_label, bg="#f0f0f0")
        date_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        date_entry = tk.Entry(edit_window, textvariable=self.date_var, font=self.font_entry)
        date_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        category_label = tk.Label(edit_window, text="Category:", font=self.font_label, bg="#f0f0f0")
        category_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        category_dropdown = ttk.Combobox(edit_window, textvariable=self.category_var, values=self.category_options, font=self.font_entry, state="readonly")
        category_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Type dropdown in Edit Window
        type_label = tk.Label(edit_window, text="Type:", font=self.font_label, bg="#f0f0f0")
        type_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        type_dropdown = ttk.Combobox(edit_window, textvariable=self.type_var, values=self.type_options, font=self.font_entry, state="readonly")
        type_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        description_label = tk.Label(edit_window, text="Description:", font=self.font_label, bg="#f0f0f0")
        description_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        description_entry = tk.Entry(edit_window, textvariable=self.description_var, font=self.font_entry)
        description_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        save_button = ttk.Button(edit_window, text="Save", command=save_edit, style=self.button_style)
        save_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def delete_transaction(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select a transaction to delete.")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this transaction?"):
            selected_index = self.tree.index(selected_item[0])
            del self.transactions[selected_index]
            self.update_transaction_list()
            self.update_summary()

    def update_transaction_list(self):
        # Clear existing items in the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get the selected category filter
        selected_category = self.filter_var.get()

        # Insert transactions into the treeview based on the filter
        for transaction in self.transactions:
            if selected_category == "All" or transaction["category"] == selected_category:
                self.tree.insert("", "end", values=(
                    transaction["amount"],
                    transaction["date"],
                    transaction["category"],
                    transaction["type"],  # Include type
                    transaction["description"]
                ))

# Main application setup
if __name__ == "__main__":
    root = tk.Tk()
    finance_tracker = FinanceTracker(root)
    root.mainloop()
