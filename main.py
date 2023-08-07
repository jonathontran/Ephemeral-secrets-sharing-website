from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

def create_connection():
    connection = mysql.connector.connect(
        host="localhost",       
        user="",    
        password="",
        database="" 
    )
    return connection

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/<code>')
def code(code):
    return f'{code}'

if __name__ == '__main__':
    app.run()
