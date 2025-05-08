from tkinter import simpledialog, messagebox
from database.db_connection import connect_db
from automation.send_email_otp import otp_storage
from GUI.stock_overview import fetch_stock_data
from logs.logger import log_info, log_error  # ✅ Logging

def verify_otp(email, user_otp, product_id, stock_table):
    """Verify OTP and update stock if valid."""

    if email in otp_storage and otp_storage[email] == user_otp:
        messagebox.showinfo("Success", "✅ OTP verified successfully!")
        log_info(f"OTP verified for {email} on product {product_id}")

        conn = connect_db()
        cursor = conn.cursor()

        # Check current stock
        cursor.execute("SELECT stock FROM products WHERE product_id = %s", (product_id,))
        stock = cursor.fetchone()

        if stock is None:
            messagebox.showerror("Error", "⚠️ Product not found in the database.")
            log_error(f"Product {product_id} not found in database.")
            conn.close()
            return False

        if stock[0] == 0:
            messagebox.showwarning("Out of Stock", "⚠️ Product is out of stock. Adding new stock!")

        # Prompt for reorder quantity
        reorder_qty = simpledialog.askinteger("Reorder", "Enter reorder quantity:")
        if reorder_qty and reorder_qty > 0:
            cursor.execute("UPDATE products SET stock = stock + %s WHERE product_id = %s", (reorder_qty, product_id))
            conn.commit()
            messagebox.showinfo("Success", f"✅ Stock updated! Added {reorder_qty} units.")
            fetch_stock_data(stock_table)  # ✅ Refresh UI
            log_info(f"Reordered {reorder_qty} units for product {product_id}.")
        else:
            messagebox.showwarning("Invalid", "⚠️ Please enter a valid reorder quantity!")

        conn.close()
        return True
    else:
        messagebox.showerror("Error", "❌ Invalid OTP!")
        log_error(f"Invalid OTP attempt for {email}.")
        return False  # ✅ Caller should handle retries
