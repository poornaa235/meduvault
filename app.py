from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="root",
    password="nHarshapranu@4141",
    database="meduvault"
)
cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select_role', methods=['POST'])
def select_role():
    role = request.form['role']
    session['role'] = role
    if role == 'hospital':
        return redirect('/login')
    else:
        return redirect('/personal_entry')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT password, role FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result and result[0] == password and result[1] == 'hospital':
            session['username'] = username
            return redirect('/hospital_dashboard')
        else:
            return render_template('login.html', error="Incorrect username or password")
    return render_template('login.html')
@app.route('/submit_personal_details', methods=['POST'])
def submit_personal_details():
    aadhar = session.get('aadhar')
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    blood_group = request.form['blood_group']
    cursor.execute("INSERT INTO personal_details (aadhar_number, name, age, gender, blood_group) VALUES (%s, %s, %s, %s, %s)",
                   (aadhar, name, age, gender, blood_group))
    db.commit()
    return render_template('success.html', message="Personal details submitted successfully")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
        db.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/hospital_dashboard')
def hospital_dashboard():
    return render_template('hospital_dashboard.html')

@app.route('/hospital_action', methods=['POST'])
def hospital_action():
    aadhar = request.form['aadhar']
    action = request.form['action']
    session['aadhar'] = aadhar

    if action == 'view':
        return redirect('/view_data')
    elif action == 'update_medical':
        return redirect('/update_medical')
    elif action == 'update_allergy':
        return redirect('/update_allergy')
    elif action == 'view_personal':
        return redirect('/view_personal_details')
    else:
        return "Invalid action"

@app.route('/view_data')
def view_data():
    aadhar = session.get('aadhar')
    cursor.execute("SELECT * FROM medical_history WHERE aadhar_number = %s", (aadhar,))
    medical = cursor.fetchall()
    cursor.execute("SELECT * FROM insurance WHERE aadhar_number = %s", (aadhar,))
    insurance = cursor.fetchall()
    cursor.execute("SELECT * FROM allergies WHERE aadhar_number = %s", (aadhar,))
    allergies = cursor.fetchall()
    cursor.execute("SELECT * FROM personal_details WHERE aadhar_number = %s", (aadhar,))
    personal = cursor.fetchone()
    return render_template('view_data.html', medical=medical, insurance=insurance, allergies=allergies, personal=personal)

@app.route('/update_medical', methods=['GET', 'POST'])
def update_medical():
    if request.method == 'POST':
        aadhar = request.form['aadhar']
        diagnosis = request.form['diagnosis']
        treatment = request.form['treatment']
        date = request.form['date']
        cursor.execute("INSERT INTO medical_history (aadhar_number, diagnosis, treatment, date) VALUES (%s, %s, %s, %s)",
                       (aadhar, diagnosis, treatment, date))
        db.commit()
        return render_template('success.html', message="Medical history updated successfully")
    return render_template('update_medical.html')

@app.route('/update_allergy', methods=['GET', 'POST'])
def update_allergy():
    if request.method == 'POST':
        aadhar = request.form['aadhar']
        allergen = request.form['allergen']
        reaction = request.form['reaction']
        cursor.execute("INSERT INTO allergies (aadhar_number, allergen, reaction) VALUES (%s, %s, %s)",
                       (aadhar, allergen, reaction))
        db.commit()
        return "Allergy info updated successfully"
    return render_template('update_allergy.html')

@app.route('/view_personal_details')
def view_personal_details():
    aadhar = session.get('aadhar')
    cursor.execute("SELECT * FROM personal_details WHERE aadhar_number = %s", (aadhar,))
    personal = cursor.fetchone()
    return render_template('view_personal_details.html', personal=personal)

@app.route('/personal_entry', methods=['GET', 'POST'])
def personal_entry():
    if request.method == 'POST':
        aadhar = request.form['aadhar']
        session['aadhar'] = aadhar
        return redirect('/personal_dashboard')
    return render_template('personal_entry.html')

@app.route('/personal_dashboard')
def personal_dashboard():
    aadhar = session.get('aadhar')
    cursor.execute("SELECT * FROM medical_history WHERE aadhar_number = %s", (aadhar,))
    medical = cursor.fetchall()
    cursor.execute("SELECT * FROM allergies WHERE aadhar_number = %s", (aadhar,))
    allergies = cursor.fetchall()
    cursor.execute("SELECT * FROM personal_details WHERE aadhar_number = %s", (aadhar,))
    personal = cursor.fetchone()
    return render_template('personal_dashboard.html', medical=medical, allergies=allergies, personal=personal)


@app.route('/insurance_options', methods=['GET', 'POST'])
def insurance_options():
    aadhar = session.get('aadhar')
    if request.method == 'POST':
        action = request.form['action']
        if action == 'view':
            cursor.execute("SELECT * FROM insurance WHERE aadhar_number = %s", (aadhar,))
            insurance = cursor.fetchall()
            return render_template('insurance_options.html', insurance=insurance)
        elif action == 'update':
            return render_template('update_insurance.html')
    return render_template('insurance_options.html')

@app.route('/submit_insurance_update', methods=['POST'])
def submit_insurance_update():
    aadhar = session.get('aadhar')
    provider = request.form['provider']
    policy_number = request.form['policy_number']
    coverage = request.form['coverage']
    cursor.execute("DELETE FROM insurance WHERE aadhar_number = %s", (aadhar,))
    cursor.execute("INSERT INTO insurance (aadhar_number, provider, policy_number, coverage) VALUES (%s, %s, %s, %s)",
                   (aadhar, provider, policy_number, coverage))
    db.commit()
    return render_template('success.html',message="Insurance updated successfully")
if __name__ == '__main__':
    app.run(debug=True)
