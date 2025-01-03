CREATE DATABASE HospitalManagementSystem;
USE HospitalManagementSystem;

CREATE TABLE Patient(
email varchar(50) PRIMARY KEY,
[password] varchar(25) NOT NULL,
[name] varchar(50) NOT NULL,
[address] varchar(50) NOT NULL,
gender VARCHAR(10) NOT NULL
);

CREATE TABLE MedicalHistory(
MH_id int PRIMARY KEY,
[date&time] DATETIME DEFAULT CURRENT_TIMESTAMP,
conditions VARCHAR(100) NOT NULL, 
surgeries VARCHAR(100) NOT NULL, 
medication VARCHAR(100) NOT NULL
);

CREATE TABLE Doctor(
email varchar(50) PRIMARY KEY,
doctor_id int NOT NULL,
gender varchar(20) NOT NULL,
[password] varchar(30) NOT NULL,
[name] varchar(50) NOT NULL
);

CREATE TABLE Appointment(
appointment_id int PRIMARY KEY,
date DATE NOT NULL,
starttime TIME NOT NULL,
endtime TIME NOT NULL,
status varchar(20) NOT NULL
);

CREATE TABLE PatientAttendAppointment(
patient varchar(50) NOT NULL,
appt int NOT NULL,
symptoms varchar(40) NOT NULL,
FOREIGN KEY (patient) REFERENCES Patient (email) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (appt) REFERENCES Appointment (appointment_id) ON DELETE CASCADE ON UPDATE CASCADE,
PRIMARY KEY (patient, appt)
);

CREATE TABLE Schedule(
schedule_id int PRIMARY KEY,
starttime TIME NOT NULL,
endtime TIME NOT NULL,
breaktime TIME NOT NULL,
holiday varchar(20) NOT NULL,
);


CREATE TABLE Diagnose(
appt int NOT NULL,
doctor varchar(50) NOT NULL,
diagnosis varchar(50) NOT NULL,
prescription varchar(100) NOT NULL,
FOREIGN KEY (appt) REFERENCES Appointment (appointment_id) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (doctor) REFERENCES Doctor (email) ON DELETE CASCADE ON UPDATE CASCADE,
PRIMARY KEY (appt, doctor)
);


CREATE TABLE DoctorViewsHistory(
history int NOT NULL,
doctor varchar(50) NOT NULL,
FOREIGN KEY (doctor) REFERENCES Doctor (email) ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (history) REFERENCES MedicalHistory (MH_id) ON DELETE CASCADE ON UPDATE CASCADE,
PRIMARY KEY (history, doctor)
);


