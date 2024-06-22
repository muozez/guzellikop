from flask import Flask, render_template, request, redirect, url_for, session
from db_config import get_db_connection

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            return 'Giriş başarısız!'
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/update_price', methods=['GET', 'POST'])
def update_price():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        service = request.form['service']
        price = request.form['price']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO prices (service, price) VALUES (%s, %s)", (service, price))
        conn.commit()
        conn.close()
        
        return 'Fiyat güncellendi!'
    return render_template('update_price.html')

@app.route('/check_appointments')
def check_appointments():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointments WHERE user_id=%s", (session['user_id'],))
    appointments = cursor.fetchall()
    conn.close()
    
    return render_template('check_appointments.html', appointments=appointments)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/submit_contact_form', methods=['POST'])
def submit_contact_form():
    name = request.form['name']
    type = request.form['type']
    location = request.form['location']
    phone = request.form['phone']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO businesses (name, type, location, phone) VALUES (%s, %s, %s, %s)", (name, type, location, phone))
    conn.commit()
    conn.close()
    
    return 'İletişim formu gönderildi!'

if __name__ == '__main__':
    app.run(debug=True)
