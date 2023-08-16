from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import random
import string
import hashlib

app = Flask(__name__)

#Establish DB connection
def create_connection():
    connection = mysql.connector.connect(
        host="localhost",       
        user="",    
        password="",
        database="" 
    )
    return connection

#Utility functions
def create_code():
    characters = string.ascii_uppercase + string.digits
    code = ''.join(random.choice(characters) for i in range(6))
    return code

def create_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation # All upper and lowercase letters, digits, and punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def encrypt(input):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input.encode('utf-8'))
    return sha256_hash.hexdigest()

#Web interface
@app.route('/submit', methods=['POST'])
def submit():
    secret = request.form['secretForm']
    code = create_code()
    pw = create_password()

    #do DB stuff

    return redirect(url_for('home', url=f"localhost:5000/{code}"))

@app.route('/submitCode', methods=['POST'])
def submitCode():
    code = request.form['secretCode']

    return redirect(code,code=code)

@app.route('/')
def home():
    url = request.args.get('url')
    return render_template("index.html", url=url)

@app.route('/<code>')
def code(code):
    #validate code to prevent SQL injection
    return f'{code}'

if __name__ == '__main__':
    app.run()
