from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin123'
app.config['MYSQL_DB'] = 'first_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Login Page
@app.route('/')
def login():
    return render_template('login.html')

# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('register'))
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()
        
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Authentication Route
@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    
    if user and password == user['password']:
        session['username'] = username
        return redirect(url_for('student_details'))
    else:
        flash('Incorrect username or password', 'error')
        return redirect(url_for('login'))

# Student Details Route
@app.route('/student_details', methods=['GET', 'POST'])
def student_details():
    if 'username' in session:
        if request.method == 'POST':
            student_name = request.form['student_name']
            student_id = request.form['student_id']
            phone = request.form['phone']
            email = request.form['email']
            gender = request.form['gender']
            languages = ','.join(request.form.getlist('languages'))
            
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO students (name, student_id, phone, email, gender, languages) VALUES (%s, %s, %s, %s, %s, %s)",
                        (student_name, student_id, phone, email, gender, languages))
            mysql.connection.commit()
            cur.close()
            
            flash('Details submitted successfully', 'success')
            return redirect(url_for('student_details'))
        
        return render_template('student_details.html')
    else:
        return redirect(url_for('login'))

# Logout Route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
