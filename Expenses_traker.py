import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import pandas as pd

# Initialize the DataFrame
columns = ["Date", "Category", "Amount", "Description"]
data = pd.DataFrame(columns=columns)


def add_expense():
    """Add expense to the DataFrame."""
    global data
    date = date_entry.get()
    category = category_var.get()
    amount = amount_entry.get()
    description = description_entry.get()

    # Validate input
    if not date or not category or not amount:
        messagebox.showerror("Input Error", "Date, Category, and Amount are required.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Input Error", "Amount must be a number.")
        return

    # Append to DataFrame
    new_row = pd.DataFrame([[date, category, amount, description]], columns=columns)
    data = pd.concat([data, new_row], ignore_index=True)

    # Update table
    update_table()

    # Clear inputs
    date_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    category_var.set(categories[0])


def update_table():
    """Refresh the table with current DataFrame."""
    for row in tree.get_children():
        tree.delete(row)
    for index, row in data.iterrows():
        tree.insert("", tk.END, values=row.tolist())


def save_to_csv():
    """Save DataFrame to a CSV file."""
    global data
    filepath = filedialog.asksaveasfilename(
        defaultextension=".csv", filetypes=[("CSV files", "*.csv")]
    )
    if filepath:
        data.to_csv(filepath, index=False)
        messagebox.showinfo("Save Successful", "Data saved successfully!")


def load_from_csv():
    """Load DataFrame from a CSV file."""
    global data
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filepath:
        data = pd.read_csv(filepath)
        update_table()


# Main Window
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("800x500")

# Header
header_label = tk.Label(root, text="Expense Tracker", font=("Helvetica", 18, "bold"))
header_label.pack(pady=10)

# Input Frame
input_frame = tk.Frame(root)
input_frame.pack(pady=10, fill="x", padx=10)

tk.Label(input_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
date_entry = tk.Entry(input_frame)
date_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Category:").grid(row=0, column=2, padx=5, pady=5)
categories = ["Food", "Transport", "Shopping", "Utilities", "Others"]
category_var = tk.StringVar(value=categories[0])
category_menu = ttk.Combobox(input_frame, textvariable=category_var, values=categories)
category_menu.grid(row=0, column=3, padx=5, pady=5)

tk.Label(input_frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
amount_entry = tk.Entry(input_frame)
amount_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Description:").grid(row=1, column=2, padx=5, pady=5)
description_entry = tk.Entry(input_frame)
description_entry.grid(row=1, column=3, padx=5, pady=5)

add_button = tk.Button(
    input_frame, text="Add Expense", command=add_expense, bg="#4CAF50", fg="white"
)
add_button.grid(row=2, column=0, columnspan=4, pady=10)

# Table Frame
table_frame = tk.Frame(root)
table_frame.pack(pady=10, fill="both", expand=True, padx=10)

tree = ttk.Treeview(table_frame, columns=columns, show="headings")
tree.pack(side="left", fill="both", expand=True)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.config(yscrollcommand=scrollbar.set)

# Footer
footer_frame = tk.Frame(root)
footer_frame.pack(pady=10, fill="x", padx=10)

save_button = tk.Button(
    footer_frame, text="Save to CSV", command=save_to_csv, bg="#007BFF", fg="white"
)
save_button.pack(side="left", padx=5)

load_button = tk.Button(
    footer_frame, text="Load from CSV", command=load_from_csv, bg="#FF5722", fg="white"
)
load_button.pack(side="left", padx=5)

exit_button = tk.Button(
    footer_frame, text="Exit", command=root.quit, bg="#f44336", fg="white"
)
exit_button.pack(side="right", padx=5)

# Start the application
root.mainloop()
