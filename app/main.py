from flask import Flask, render_template, request, redirect, url_for, session
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import mysql.connector
import random
import string
import hashlib
import base64
import secrets
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(app=app, key_func=get_remote_address)

#SALT = base64.b64encode(b'GUDNQ5O70A0NQSXW')


#DB functions - todo: error handling
def create_connection():
    connection = mysql.connector.connect(       
        user="root",    
        password="root",
        host="db",
        #host="localhost",
        port="3306",
        database="ephemeralSecrets" 
    )
    return connection

def close_connection(connection):
    connection.close()

def insert_row(connection, url, expiry, password, SALT, secret, active):
    cursor = connection.cursor()
    sql = "INSERT INTO user_secret (url, expiry, password, SALT, secret, active) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (url, expiry, password, SALT, secret, active)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


def select_row(connection, code):
    cursor = connection.cursor()
    sql = "SELECT * FROM user_secret WHERE url = %s ORDER BY ID DESC"
    values = (code,) #tuple with single element
    cursor.execute(sql, values)
    row = cursor.fetchone()
    cursor.close()
    return row

def delete_row(connection, url, password):
    cursor = connection.cursor()
    sql = "DELETE FROM user_secret WHERE url = %s AND password = %s"
    values = (url, password)
    cursor.execute(sql, values)
    connection.commit()
    cursor.close()


#Utility functions
def create_code():
    characters = string.ascii_uppercase + string.digits
    code = ''.join(random.choice(characters) for i in range(6))
    return code

def create_password(length=8): #UNUSED
    characters = string.ascii_letters + string.digits + string.punctuation # All upper and lowercase letters, digits, and punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def hash(input):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input.encode('utf-8'))
    return sha256_hash.hexdigest()

def generate_SALT():
    salt = secrets.token_bytes(16)
    return salt

def derive_key_from(input,salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(str.encode(input))) #convert input string to bytes, then derive a key and encode
    return key



#Secret Submission
@app.route('/submit', methods=['POST'])
def submit():
    #Create unique code
    connection = create_connection()
    while True:
        code = create_code() #generate random 6 character code
        if select_row(connection,code) is None:
            break
    close_connection(connection)

    pw = request.form['password']
    expiryDate = request.form['expiryDate']
    pwhash = hash(pw) #SHA256 hash to store

    secret = request.form['secretForm'] #get user input
    salt = generate_SALT()
    plaintextSalt = base64.b64encode(salt).decode('utf-8')
    key = derive_key_from(pw,salt)
    fernet = Fernet(key)
    secret = fernet.encrypt(str.encode(secret)) #convert secret to bytes and encrypt

    #do DB stuff
    connection = create_connection()
    insert_row(connection,code,expiryDate,pwhash,plaintextSalt,secret.decode('utf-8'),1)
    close_connection(connection)

    return redirect(url_for("submitConfirmation",code=code))

@app.route('/submitConfirmation', methods=['GET','POST'])
def submitConfirmation():
    code = request.args.get('code')

    connection = create_connection()
    row = select_row(connection,code)
    close_connection(connection)

    #validate code to be exactly 6 characters, and exists in the database
    if len(code) == 6 and row is not None:
        return render_template("submitConfirmation.html", code=code)
    else:
        return redirect(url_for("home"))
    







#Secret Retreival
@app.route('/submitCode', methods=['POST'])
def submitCode():
    code = request.form['secretCode']

    return redirect(code)

@app.route('/<code>', methods=['GET','POST'])
def retrieveSecret(code):
    connection = create_connection()
    row = select_row(connection,code)
    close_connection(connection)

    #validate code to be exactly 6 characters, and exists in the database
    if len(code) == 6 and row is not None:
        return render_template("retrieveSecret.html", code=code)
    elif row[6] != '1':
        return render_template("retrieveSecret.html", code=code, invalidCode="Code has expired")
    else:
        return render_template("retrieveSecret.html", code=code, invalidCode="Invalid Code - please try again")
    
    

@app.route('/submitPassword', methods=['GET','POST'])
@limiter.limit("3/minute")
def viewSecret():
    code = request.args.get('code')
    pw = request.form.get('password')

    connection = create_connection()
    row = select_row(connection,code)
    close_connection(connection)

    #validate code to be exactly 6 characters, and exists in the database
    if not (len(code) == 6 and row is not None):
        return redirect(url_for("retrieveSecret",code=code))

    secret = ''
    salt = ''
    if row is not None:
        secret = row[5]
        salt = row[4]
    salt = base64.b64decode(salt.encode("utf-8")) #back to bytestring

    #key derivation function
    key = derive_key_from(pw,salt)
    fernet = Fernet(key)
    try:
        secret = fernet.decrypt(secret) 
        secret = secret.decode('utf-8') #back to string
    except (InvalidToken, Exception):
        return render_template("retrieveSecret.html", code=code, error="Incorrect password.")

    #delete secret after retrieval
    #connection = create_connection()
    #delete_row(connection,code,hash(pw))
    #close_connection(connection)

    return render_template("viewSecret.html", secret=secret,code=code)

@app.errorhandler(429)
def ratelimit_handler(e):
    code = request.referrer.split('/')[-1].split('=')[-1]
    return render_template("retrieveSecret.html", code=code, error="Too many attempts, try again later.")


#Home Page
@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
