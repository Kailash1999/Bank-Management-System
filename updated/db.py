import mysql.connector

def get_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Karan@2000",
            database="bank_system"
        )
    except mysql.connector.Error as err:
        print("❌ Database Error:", err)
        return None
