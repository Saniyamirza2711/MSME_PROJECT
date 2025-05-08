import mysql.connector  
import random  
import sys
import os

# Ensure correct path resolution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db_connection import connect_db  
from automation.send_otp import send_otp  

def generate_otp():  
    """Generates a 6-digit OTP."""
    return str(random.randint(100000, 999999))  

def check_low_stock():  
    """Checks products with low stock and sends an OTP alert if needed."""
    conn = connect_db()  
    cursor = conn.cursor()  

    # Get products with stock below the reorder threshold  
    query = """
    SELECT p.product_id, p.name, p.stock, r.threshold 
    FROM products p  
    JOIN reorder_threshold r ON p.product_id = r.product_id  
    WHERE p.stock < r.threshold
    """
    cursor.execute(query)  
    low_stock_items = cursor.fetchall()  
    conn.close()  

    if low_stock_items:  
        for item in low_stock_items:  
            product_id, name, stock, threshold = item  
            print(f"Low stock alert: {name} (Stock: {stock}, Threshold: {threshold})")  
            
                       # Generate OTP and send alert  
            otp = generate_otp()  
            response = send_otp(otp)  

            if response.get("return") is False:
                print(f"⚠️ OTP sending failed for {name}: {response.get('message')}")

if __name__ == "__main__":  
    check_low_stock()
