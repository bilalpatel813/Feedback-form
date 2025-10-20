from flask import Flask, request, render_template, redirect, url_for, session
import pymysql
from dotenv import load_dotenv
load_dotenv()
import os
app = Flask(__name__)
app.secret_key = "suiisecretkey"
dB= pymysql.connect(
    host= os.environ.get('DB_host'),
    password=os.environ.get('DB_pass'),
    user= os.environ.get('DB_user'),
    db=os.environ.get('DB_db'),
    port=31839
)
# ADMIN LOGIN CREDENTIALS 
Admin_username = os.environ.get('Ad_user')
Admin_password = os.environ.get('Ad_pass')
# keep as string for safety

#-------------------------------------
@app.route('/')
def home():
    return render_template("form.html")

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    rate = request.form['rate']
    suggestion = request.form['suggestion']
    cursor = dB.cursor()
    sql = "INSERT INTO feedbackdata(name, email, rate, suggestion) VALUES (%s, %s, %s, %s)"
    values = (name, email, rate, suggestion)
    try:
        cursor.execute(sql, values)
        dB.commit()
        return render_template("form.html")
    except Exception as e:
        dB.rollback()
        return f"<h2>Error: {e}</h2>"
    return redirect(url_for('home'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == Admin_username and password == Admin_password:
            session['login'] = True
            return redirect(url_for('admin'))
        else:
            return "<h2>Invalid username or password</h2>"
    
    return render_template("login.html")
@app.route('/admin') 
def admin():
    if not session.get('login'):
        return redirect(url_for('login'))
    cursor = dB.cursor()
    cursor.execute('SELECT * FROM feedbackdata  ORDER BY id ASC')
    rows = cursor.fetchall()
    cursor.close()
    return render_template("admin.html", feedback=rows)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)