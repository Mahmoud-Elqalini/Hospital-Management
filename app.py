from flask import Flask, request, render_template, flash
import pyodbc
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)

# Establish a connection to the SQL Server
DRIVER_NAME = 'SQL Server'
SERVER_NAME = '??????????????????????'
conn = pyodbc.connect('Driver={SQL Server};'
                    'Server=??????????????????????????;'
                    'Database=HospitalManagementSystem;'
                    'Trusted_Connection=yes;')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()


# ########################################### Function ########################################################
def add_doctor(cursor, conn, email, gender, password, name, salary):
    try:
        query = \
            f'''EXEC insertdoctor '{email}', '{gender}', '{password}', '{name}', {salary} '''
        cursor.execute(query)
        conn.commit()
        flash('Doctor added successfully.', 'success')
    except pyodbc.Error as e:
        error_message = str(e)
        if 'HY007' in error_message:
            flash('Duplicate Doctor Email found. Please, use a different Email.', 'danger')
        else:
            flash(f"Database error: {error_message}", 'danger')


def add_patient(cursor, conn, email, password, name, address, gender):
    try:
        query = \
            f'''EXEC insertpatient '{email}', '{password}', '{name}', '{address}', '{gender}' '''
        cursor.execute(query)
        conn.commit()
        flash('Patient added successfully.', 'success')
    except pyodbc.Error as e:
        error_message = str(e)
        if 'HY007' in error_message:
            flash('This patient is already in.', 'danger')
        else:
            flash(f"Database error: {error_message}", 'danger')


def add_history(cursor, conn, ph_id, surgeries, conditions, medication, email):
    try:
        query = \
            f'''EXEC InsertMedicalHistory {ph_id}, '{conditions}', '{surgeries}', '{medication}', '{email}' '''
        cursor.execute(query)
        conn.commit()
        flash('History added successfully.', 'success')
    except pyodbc.Error as e:
        error_message = str(e)
        if 'HY007' in error_message:
            flash('Duplicate History ID found. Please, use a different ID.', 'danger')
        elif '23000' in error_message:
            flash('It is not allowed to have a Duplicate History ID.', 'danger')
        else:
            flash(f"Database error: {error_message}", 'danger')


def add_schedule(cursor, conn, schedule_id, start_time, end_time, break_time, doctor_holiday, email):
    try:
        query = \
            f'''EXEC AddSchedule {schedule_id}, '{start_time}', '{end_time}', '{break_time}', '{doctor_holiday}', '{email}' '''
        cursor.execute(query)
        conn.commit()
        flash('Schedule added successfully.', 'success')
    except pyodbc.Error as e:
        error_message = str(e)
        if 'HY007' in error_message:
            flash('Duplicate Schedule ID found. Please, use a different ID.', 'danger')
        else:
            flash(f"Database error: {error_message}", 'danger')


def add_appointment(cursor, conn, appointment_id, date, start_time, end_time, status):
    try:
        query = \
            f'''EXEC Addappointment {appointment_id}, '{date}', '{start_time}', '{end_time}', '{status}' '''
        cursor.execute(query)
        conn.commit()
        flash('Appointment added successfully.', 'success')
    except pyodbc.Error as e:
        error_message = str(e)
        if 'HY007' in error_message:
            flash('Duplicate Appointment ID found. Please, use a different ID.', 'danger')
        else:
            flash(f"Database error: {error_message}", 'danger')


def add_diagnose(cursor, conn, appointment_id, doctor_email, diagnose, prescription):
    try:
        query = \
            f'''EXEC Adddiagnose {appointment_id}, '{doctor_email}', '{diagnose}', '{prescription}' '''
        cursor.execute(query)
        conn.commit()
        flash('Diagnose added successfully.', 'success')
    except pyodbc.Error as e:
        error_message = str(e)
        if 'HY007' in error_message:
            flash('Duplicate Diagnose found. Please, use a different Appointment ID Or Doctor Email.', 'danger')
        elif '23000' in error_message:
            flash('It is not allowed to have a diagnosis that does not have Appointment ID or Doctor Email.', 'danger')
        else:
            flash(f"Database error: {error_message}", 'danger')


def get_data(table_name):
    cursor.execute(f'''SELECT * FROM {table_name} ''')
    rows = cursor.fetchall()
    return rows


# #################################################################Search & delete function ###########################
def search(cursor, keyword, table_name, attr):
    query =\
        f'''SELECT * 
            FROM {table_name}
            WHERE {attr} LIKE '%{keyword}%' '''
    cursor.execute(query)
    results = cursor.fetchall()
    return results


def delete(cursor, conn, email, table_name, attrb):
    try:
        query_check = f"SELECT COUNT(*) FROM {table_name} WHERE {attrb} = '{email}'"
        cursor.execute(query_check)
        result = cursor.fetchone()
        if result[0] > 0:
            query_delete = f'''DELETE FROM {table_name} WHERE {attrb} = '{email}' '''
            cursor.execute(query_delete)
            conn.commit()
            flash('Deleted successfully.', 'success')
        else:
            flash(f"No record found with {attrb} = '{email}'.", 'danger')

    except pyodbc.Error as e:
        error_message = str(e)
        flash(f"Database error: {error_message}", 'danger')


# ############################################## render function ###############################################
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/doctor.html')
def doctor():
    doctor_data = get_data('Doctor')
    return render_template('doctor.html', doctors=doctor_data)


@app.route('/patient.html')
def patient():
    patient_data = get_data("Patient")
    return render_template('patient.html', patients=patient_data)


@app.route('/patienthistory.html')
def history():
    patient_data = get_data("MedicalHistory")
    return render_template('patienthistory.html', histories=patient_data)


@app.route('/doctor_schedule.html')
def schedule():
    schedule_data = get_data("Schedule")
    return render_template('doctor_schedule.html', schedules=schedule_data)


@app.route('/appointment.html')
def appointment():
    appointment_data = get_data("Appointment")
    return render_template('appointment.html', appointments=appointment_data)


@app.route('/diagnose.html')
def diagnose():
    diagnose_data = get_data("Diagnose")
    return render_template('diagnose.html', diagnoses=diagnose_data)


# #################################################submit data #####################################################
@app.route('/add_doctor', methods=['POST'])
def submit_doctor():
    if request.method == 'POST':  # method of send data
        email = request.form['doctor_email']
        password = request.form['doctor_password']
        gender = request.form['doctor_gender']
        name = request.form['doctor_name']
        salary = request.form['doctor_salary']
        add_doctor(cursor, conn, email, gender, password, name, salary)
        doctor_data = get_data('Doctor')
        return render_template('doctor.html', doctors=doctor_data)


@app.route('/add_patient', methods=['POST'])
def submit_patient():
    if request.method == 'POST':  # method of send data
        email = request.form['Patient_email']
        password = request.form['patient_password']
        name = request.form['patient_name']
        address = request.form['patient_gender']
        gender = request.form['patient_address']
        add_patient(cursor, conn, email, password, name, address, gender)
        patient_data = get_data("Patient")
        return render_template('patient.html', patients=patient_data)


@app.route('/add_history', methods=['POST'])
def submit_history():
    if request.method == 'POST':  # method of send data
        ph_id = request.form['MH_id']
        surgeries = request.form['patient_surgeries']
        conditions = request.form['patient_conditions']
        medication = request.form['patient_medication']
        email = request.form['Patient_email']
        add_history(cursor, conn, ph_id, surgeries, conditions, medication, email)
        history_data = get_data("MedicalHistory")
        return render_template('patienthistory.html', histories=history_data)


@app.route('/add_schedule', methods=['POST'])
def submit_schedule():
    if request.method == 'POST':  # method of send data
        schedule_id = request.form['schedule_id']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        break_time = request.form['break_time']
        doctor_holiday = request.form['doctor_holiday']
        email = request.form['doctor_email']
        add_schedule(cursor, conn, schedule_id, start_time, end_time, break_time, doctor_holiday, email)
        schedule_data = get_data("Schedule")
        return render_template('doctor_schedule.html', schedules=schedule_data)


@app.route('/add_Appointment', methods=['POST'])
def submit_appointment():
    if request.method == 'POST':  # method of send data
        appointment_id = request.form['appointment_id']
        date = request.form['date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        status = request.form['status']
        add_appointment(cursor, conn, appointment_id, date, start_time, end_time, status)
        appointment_data = get_data("Appointment")
        return render_template('appointment.html', appointments=appointment_data)


@app.route('/add_diagnose', methods=['POST'])
def submit_diagnose():
    if request.method == 'POST':  # method of send data
        appointment_id = request.form['appointment_id']
        doctor_email = request.form['doctor_email']
        diagnose = request.form['diagnose']
        prescription = request.form['prescription']
        add_diagnose(cursor, conn, appointment_id, doctor_email, diagnose, prescription)
        diagnose_data = get_data("Diagnose")
        return render_template('diagnose.html', diagnoses=diagnose_data)


# #################################################search data #####################################################
@app.route('/search_doctor', methods=['GET'])
def search_doctor():
    if request.method == 'GET':
        keyword = request.args.get('doctor_name')
        doctor_data = search(cursor, keyword, 'Doctor', 'Doctor_name')
        return render_template('doctor.html', doctors=doctor_data)


@app.route('/search_patient', methods=['GET'])
def search_patient():
    if request.method == 'GET':
        keyword = request.args.get('patient_name')
        patient_data = search(cursor, keyword, 'Patient', 'name')
        return render_template('patient.html', patients=patient_data)


@app.route('/search_history', methods=['GET'])
def search_history():
    if request.method == 'GET':
        keyword = request.args.get('patient_email')
        history_data = search(cursor, keyword, 'MedicalHistory', 'patient_email')
        return render_template('patienthistory.html', histories=history_data)


@app.route('/search_schedule', methods=['GET'])
def search_schedule():
    if request.method == 'GET':
        keyword = request.args.get('doctor_email')
        schedule_data = search(cursor, keyword, 'Schedule', 'doctor_email')
        return render_template('doctor_schedule.html', schedules=schedule_data)


@app.route('/search_appointment', methods=['GET'])
def search_appointment():
    if request.method == 'GET':
        keyword = request.args.get('appointment_id')
        appointment_data = search(cursor, keyword, 'Appointment', 'appointment_id')
        return render_template('appointment.html', appointments=appointment_data)


@app.route('/search_diagnose', methods=['GET'])
def search_diagnose():
    if request.method == 'GET':
        keyword = request.args.get('doctor_email')
        diagnose_data = search(cursor, keyword, 'Diagnose', 'doctor')
        return render_template('diagnose.html', diagnoses=diagnose_data)


# ###############################################################delete data ########################################
@app.route('/delete_doctor', methods=['POST'])
def delete_doctor():
    if request.method == 'POST':  # method of send data
        doctor_email = request.form['doctor_email']
        delete(cursor, conn,doctor_email, 'Doctor ', 'email')
        doctor_data = get_data("Doctor")
        return render_template('doctor.html', doctors=doctor_data)


@app.route('/delete_patient', methods=['POST'])
def delete_patient():
    if request.method == 'POST':  # method of send data
        patient_email = request.form['Patient_id']
        delete(cursor, conn, patient_email, 'Patient', 'email')
        patient_data = get_data('Patient')
        return render_template('patient.html', patients=patient_data)


@app.route('/delete_history', methods=['POST'])
def delete_history():
    if request.method == 'POST':  # method of send data
        history_id = request.form['history_id']
        delete(cursor, conn, history_id, 'MedicalHistory', 'MH_id')
        history_data = get_data('MedicalHistory')
        return render_template('patienthistory.html', histories=history_data)


@app.route('/delete_schedule', methods=['POST'])
def delete_schedule():
    if request.method == 'POST':  # method of send data
        schedule_id = request.form['schedule_id']
        delete(cursor, conn, schedule_id, 'Schedule', 'Schedule_id')
        schedule_data = get_data('Schedule')
        return render_template('doctor_schedule.html', schedules=schedule_data)


@app.route('/delete_appointment', methods=['POST'])
def delete_appointment():
    if request.method == 'POST':  # method of send data
        appointment_id = request.form['appointment_id']
        delete(cursor, conn, appointment_id, 'Appointment', 'appointment_id')
        appointment_data = get_data('Appointment')
        return render_template('appointment.html', appointments=appointment_data)


@app.route('/delete_diagnose', methods=['POST'])
def delete_diagnose():
    if request.method == 'POST':  # method of send data
        doctor_email = request.form['doctor_email']
        delete(cursor, conn, doctor_email, 'Diagnose', 'doctor')
        diagnose_data = get_data('Diagnose')
        return render_template('diagnose.html', diagnoses=diagnose_data)


app.run(debug=True)

# Close the cursor and connection
cursor.close()
conn.close()
