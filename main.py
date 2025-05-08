import tkinter as tk  
from tkinter import ttk, messagebox
import sys
import os

# Ensure correct path resolution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_connection import connect_db
from GUI.stock_overview import fetch_stock_data
from GUI.sales_entry import record_sale

# Function to get product list from database
def fetch_products():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT product_id, name FROM products")
    products = cursor.fetchall()
    conn.close()
    return products  # ✅ Return (ID, Name) pairs

# Initialize Tkinter window
root = tk.Tk()
root.title("Supermarket Inventory Management")
root.geometry("1500x1600")

# Heading
tk.Label(root, text="Product Sales Entry", font=("Arial", 14, "bold")).pack(pady=10)

# Product Selection
products = fetch_products()
product_dict = {str(p[0]): p[1] for p in products}  # ✅ Store ID-Name mapping
product_var = tk.StringVar()
product_dropdown = ttk.Combobox(root, textvariable=product_var, values=[p[1] for p in products], state="readonly")
product_dropdown.pack()


# Quantity Entry
tk.Label(root, text="Enter Quantity:").pack()
quantity_entry = tk.Entry(root)
quantity_entry.pack()

# Submit Button
submit_btn = tk.Button(root, text="Record Sale", command=lambda: record_sale(product_var, quantity_entry, stock_table))
submit_btn.pack(pady=10)

# Stock Overview
tk.Label(root, text="Stock Overview", font=("Arial", 12, "bold")).pack(pady=5)

# Create Treeview table for stock
columns = ("Product", "Stock")
stock_table = ttk.Treeview(root, columns=columns, show="headings")
stock_table.heading("Product", text="Product")
stock_table.heading("Stock", text="Stock")
stock_table.pack(pady=5)

# Load stock data on startup
fetch_stock_data(stock_table)

# Run the Tkinter application
root.mainloop()
