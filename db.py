from cgitb import reset
from unittest import result
import mysql.connector

dbconfig = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "debt_database"
}


def addcustomer(cus_name: str):
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()

    _sql = """INSERT INTO 
    customer_table(customer_name, debt_total) 
    VALUES(?, ?)
    """

    cursor.execute(_sql, (cus_name, int(0)))
    conn.commit()

    cursor.close()
    conn.close()


def deleteAllRecords():
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()

    _sql = """DELETE FROM course"""

    cursor.execute(_sql)
    conn.commit()

    cursor.close()
    conn.close()


def show_transaction():
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()

    _sql = """SELECT * FROM transaction_table"""
    cursor.execute(_sql)

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result
