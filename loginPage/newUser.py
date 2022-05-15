from flask import Flask, render_template, request
from passlib.hash import sha256_crypt
import mysql.connector

app = Flask(__name__)
connection = mysql.connector.connect(host='localhost',user='root',password='24090110',database='Login')
@app.route('/')
def index():
    username = "admin"
    password = sha256_crypt.encrypt("admin123")
    email = "what@ever.com"

    cursor = connection.cursor()
    cursor.execute('INSERT INTO Login (username, password, email) VALUES (%s, %s, %s)', (username, password, email))
    connection.commit()
    cursor.close()

    return "New user added"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')
