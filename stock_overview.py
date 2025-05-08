import tkinter as tk
from tkinter import ttk
from database.db_connection import connect_db

def fetch_stock_data(stock_table):
    """Fetch stock data and update the table with color formatting for low-stock items."""
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch product stock and threshold values
    cursor.execute("""
        SELECT p.product_id, p.name, p.stock, COALESCE(r.threshold, 0)
        FROM products p
        LEFT JOIN reorder_threshold r ON p.product_id = r.product_id
    """)
    stock_data = cursor.fetchall()
    conn.close()

    # Clear existing table data
    stock_table.delete(*stock_table.get_children())

    # Insert stock data into the table with conditional coloring
    for product_id, name, stock, threshold in stock_data:
        color_tag = "red" if stock <= threshold else "black"
        stock_table.insert("", "end", values=(name, stock), tags=(color_tag,))

    # Configure tag colors
    stock_table.tag_configure("red", foreground="red")
    stock_table.tag_configure("black", foreground="black")
