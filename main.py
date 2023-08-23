from flask import Flask, render_template, request, redirect, url_for, session
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import mysql.connector
import random
import string
import hashlib
import base64

app = Flask(__name__)

SALT = base64.b64encode(b'GUDNQ5O70A0NQSXW')

#DB functions - todo: error handling
def create_connection():
    connection = mysql.connector.connect(
        host="localhost",       
        user="root",    
        password="ephemeral",
        database="ephemeralSecrets" 
    )
    return connection

def close_connection(connection):
    connection.close()

def insert_row(connection,url,expiry,password,secret,active):
    cursor = connection.cursor()
    sql = f"insert into secret (url,expiry,password,secret,active) values ('{url}','{expiry}','{password}','{secret}',{active})"
    cursor.execute(sql)
    connection.commit()
    cursor.close()

def select_row(connection,code):
    cursor = connection.cursor()
    sql = f"select * from secret where url = '{code}' order by ID desc"
    cursor.execute(sql)
    row = cursor.fetchone()
    cursor.close()
    return row

def delete_row(connection,url,password):
    cursor = connection.cursor()
    sql = f"delete from secret where url='{url}' and password='{password}'"
    cursor.execute(sql)
    connection.commit()
    cursor.close()

#Utility functions
def create_code():
    characters = string.ascii_uppercase + string.digits
    code = ''.join(random.choice(characters) for i in range(6))
    return code

def create_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation # All upper and lowercase letters, digits, and punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def hash(input):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input.encode('utf-8'))
    return sha256_hash.hexdigest()





#Secret Submission
@app.route('/submit', methods=['POST'])
def submit():
    code = create_code() #generate random 6 character code
    pw = create_password() #todo
    print(pw)
    pwhash = hash(pw) #SHA256 hash to store

    secret = request.form['secretForm'] #get user input
    #key derivation function
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(str.encode(pw))) #convert pw to bytes, then derive a key and encode
    fernet = Fernet(key)
    secret = fernet.encrypt(secret.encode()) #convert secret to bytes and encrypt

    #do DB stuff
    connection = create_connection()
    insert_row(connection,code,'2023-08-25',pwhash,secret.decode('utf-8'),1)
    close_connection(connection)

    return redirect(url_for("submitConfirmation",code=code))

@app.route('/submitConfirmation', methods=['GET','POST'])
def submitConfirmation():
    code = request.args.get('code')

    return render_template("submitConfirmation.html", code=code)







#Secret Retreival
@app.route('/submitCode', methods=['GET','POST'])
def submitCode():
    code = request.form['secretCode']

    return redirect(code)

@app.route('/<code>', methods=['GET','POST'])
def retrieveSecret(code):
    #todo: validate code to prevent SQL injection

    return render_template("retrieveSecret.html", code=code)

@app.route('/submitPassword', methods=['GET','POST'])
def viewSecret():
    code = request.args.get('code')
    #todo: validate code to prevent SQL injection
    pw = request.form['password']

    connection = create_connection()
    row = select_row(connection,code)
    close_connection(connection)

    secret = ''
    if row is not None:
        secret = row[4]
    
    #now decrypt
    #key derivation function
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(str.encode(pw))) #convert pw to bytes, then derive a key and encode
    fernet = Fernet(key)
    secret = fernet.decrypt(secret) 
    secret = secret.decode('utf-8') #back to string

    #delete secret after retrieval
    connection = create_connection()
    row = delete_row(connection,code,hash(pw))
    close_connection(connection)

    return render_template("viewSecret.html", secret=secret,code=code)




#Home Page
@app.route('/')
def home():
    url = request.args.get('url')
    return render_template("index.html", url=url)

if __name__ == '__main__':
    app.run()
