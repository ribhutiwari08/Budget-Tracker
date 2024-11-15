import tkinter as tk
from tkinter import messagebox
import pandas as pd

class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker App")
        self.root.geometry("400x400")
        
        # Create an empty DataFrame to store expenses
        self.expenses_df = pd.DataFrame(columns=['Category', 'Amount', 'Date'])

        # Create widgets
        self.category_label = tk.Label(root, text="Category:")
        self.category_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.category_entry = tk.Entry(root)
        self.category_entry.grid(row=0, column=1, padx=10, pady=10)

        self.amount_label = tk.Label(root, text="Amount:")
        self.amount_label.grid(row=1, column=0, padx=10, pady=10)
        
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=10)

        self.date_label = tk.Label(root, text="Date (YYYY-MM-DD):")
        self.date_label.grid(row=2, column=0, padx=10, pady=10)
        
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=2, column=1, padx=10, pady=10)

        self.add_button = tk.Button(root, text="Add Expense", command=self.add_expense)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.view_button = tk.Button(root, text="View Summary", command=self.view_summary)
        self.view_button.grid(row=4, column=0, columnspan=2, pady=10)

    def add_expense(self):
        category = self.category_entry.get()
        amount = self.amount_entry.get()
        date = self.date_entry.get()

        if category and amount and date:
            try:
                amount = float(amount)
                # Create a new expense entry
                new_expense = pd.DataFrame({'Category': [category], 'Amount': [amount], 'Date': [date]})
                self.expenses_df = pd.concat([self.expenses_df, new_expense], ignore_index=True)

                # Clear the input fields
                self.category_entry.delete(0, tk.END)
                self.amount_entry.delete(0, tk.END)
                self.date_entry.delete(0, tk.END)

                messagebox.showinfo("Success", "Expense added successfully!")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount.")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def view_summary(self):
        if not self.expenses_df.empty:
            summary_window = tk.Toplevel(self.root)
            summary_window.title("Summary")
            summary_window.geometry("400x400")

            summary_label = tk.Label(summary_window, text="--- Budget Summary ---")
            summary_label.pack(pady=10)

            # Display expenses in a listbox
            listbox = tk.Listbox(summary_window, width=50, height=15)
            for index, row in self.expenses_df.iterrows():
                listbox.insert(tk.END, f"Category: {row['Category']}, Amount: ₹{row['Amount']}, Date: {row['Date']}")
            listbox.pack(pady=10)

            # Show total by category
            total_by_category = self.expenses_df.groupby('Category')['Amount'].sum()
            category_label = tk.Label(summary_window, text="--- Total by Category ---")
            category_label.pack(pady=5)

            for category, total in total_by_category.items():
                category_info = tk.Label(summary_window, text=f"{category}: ₹{total:.2f}")
                category_info.pack(pady=2)

            # Show the overall total
            total_expenses = self.expenses_df['Amount'].sum()
            total_label = tk.Label(summary_window, text=f"Total Expenses: ₹{total_expenses:.2f}")
            total_label.pack(pady=10)
        else:
            messagebox.showinfo("No Data", "No expenses have been added yet.")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()
