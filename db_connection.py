import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # ✅ Use your actual MySQL username
        password="Eshwar@9347",  # ✅ Use your actual MySQL password
        database="inventory_db"  # ✅ Use the correct database name
    )
