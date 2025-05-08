import logging
from tkinter import messagebox, simpledialog
from database.db_connection import connect_db
from GUI.stock_overview import fetch_stock_data
from automation.send_email_otp import send_otp_via_email, generate_otp
from automation.verify_otp import verify_otp
from logs.logger import log_info, log_error  # ✅ Correct import

def record_sale(product_var, quantity_entry, stock_table):
    """Handles the sales entry process with logging and OTP verification for low stock."""
    
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch product names & IDs into a dictionary
    cursor.execute("SELECT product_id, name FROM products")
    product_dict = {pid: name for pid, name in cursor.fetchall()}

    # Convert selected product name to product ID
    product_name = product_var.get()
    product_id = next((pid for pid, name in product_dict.items() if name == product_name), None)

    if not product_id:
        messagebox.showerror("Error", "Invalid product selected!")
        log_error(f"Invalid product selected: {product_name}")  # ✅ Log error
        conn.close()
        return

    quantity = quantity_entry.get()
    if not quantity.isdigit():
        messagebox.showerror("Error", "Please enter a valid quantity!")
        log_error(f"Invalid quantity input: {quantity}")  # ✅ Log error
        conn.close()
        return

    quantity = int(quantity)

    # Check stock availability
    cursor.execute("SELECT stock FROM products WHERE product_id = %s", (product_id,))
    stock = cursor.fetchone()[0]

    if stock < quantity:
        messagebox.showerror("Error", "Not enough stock available!")
        log_error(f"Stock too low: Product ID {product_id}, Available {stock}, Requested {quantity}")  # ✅ Log warning
        conn.close()
        return

    # Deduct stock and insert sale record
    cursor.execute("INSERT INTO sales (product_id, quantity) VALUES (%s, %s)", (product_id, quantity))
    cursor.execute("UPDATE products SET stock = stock - %s WHERE product_id = %s", (quantity, product_id))
    conn.commit()

    messagebox.showinfo("Success", "Sale recorded successfully!")
    log_info(f"Sale recorded: Product ID {product_id}, Quantity {quantity}")  # ✅ Log sale

    quantity_entry.delete(0, "end")

    # Refresh stock table (🔴 Low-stock items turn red)
    fetch_stock_data(stock_table)

    # Check for low stock and send OTP
    cursor.execute("SELECT threshold FROM reorder_threshold WHERE product_id = %s", (product_id,))
    threshold = cursor.fetchone()

    if threshold and stock - quantity <= threshold[0]:  
        log_error(f"Low stock alert: Product ID {product_id}, Remaining {stock - quantity}, Threshold {threshold[0]}")  # ✅ Log low stock
        
        otp = generate_otp()
        admin_email = "eshwarsaikuntala@gmail.com"
        send_otp_via_email(admin_email)  # ✅ Corrected OTP function call

        # OTP Verification with retries
        max_attempts = 3
        attempts = 0
        verified = False

        while attempts < max_attempts:
            user_otp = simpledialog.askstring("OTP Verification", f"Enter the OTP received (Attempt {attempts + 1}/{max_attempts}):")
            
            if user_otp and verify_otp(admin_email, user_otp, product_id, stock_table):
                verified = True
                break  # ✅ Exit loop if OTP is correct
            else:
                attempts += 1
                messagebox.showerror("Error", f"❌ Invalid OTP. Attempts left: {max_attempts - attempts}")

        if not verified:
            messagebox.showerror("Error", "❌ Maximum OTP attempts reached! Reorder canceled.")
            conn.close()
            return  # ❌ Stop further execution

        # Prompt for reorder quantity after successful OTP verification
        reorder_qty = simpledialog.askinteger("Reorder", "Enter reorder quantity:")
        
        if reorder_qty and reorder_qty > 0:
            cursor.execute("UPDATE products SET stock = stock + %s WHERE product_id = %s", (reorder_qty, product_id))
            conn.commit()
            messagebox.showinfo("Reorder", f"✅ Stock updated! Added {reorder_qty} units.")
            log_info(f"Stock replenished: Product ID {product_id}, Added {reorder_qty} units")  # ✅ Log reorder
            
            fetch_stock_data(stock_table)  # ✅ Refresh stock table after reorder
        else:
            messagebox.showwarning("Invalid", "⚠️ Please enter a valid reorder quantity!")

    conn.close()
