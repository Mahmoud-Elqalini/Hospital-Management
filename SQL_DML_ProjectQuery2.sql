INSERT INTO Patient(email,password,name,address,gender)
VALUES
('mahmoud@gmail.com','mahmoud13','mahmoud','tanta', 'male'),
('mohamed@gmail.com','mohamed13','mohamed','zagazeeg', 'male'),
('ali@gmail.com','ali13','ali','cairo', 'male')
;

INSERT INTO MedicalHistory(MH_id,conditions,surgeries,medication)
VALUES
(1,'Pain in abdomen','Heart Surgery','Crocin'),
(2,'Frequent Indigestion','none','none'),
(3,'Body Pain','none','Iodex')
;

INSERT INTO Doctor(email, doctor_id, gender, password, name)
VALUES
('ahmed@gmail.com', 100, 'male', 'ahmed13', 'ahmed hamdy'),
('hasan@gmail.com', 200, 'male', 'hasan13', 'hasan mohamed')
;

INSERT INTO Appointment(appointment_id,date,starttime,endtime,status)
VALUES
(1, '2020-05-15', '09:00', '10:00', 'Done'),
(2, '2020-05-16', '10:00', '11:00', 'Done'),
(3, '2020-05-18', '14:00', '15:00', 'Done')
;

INSERT INTO PatientAttendAppointment(patient,appt,symptoms)
VALUES
('mahmoud@gmail.com',1, 'itchy throat'),
('mohamed@gmail.com',2, 'fever'),
('ali@gmail.com',3, 'fever')
;

INSERT INTO Schedule(schedule_id,starttime,endtime,breaktime,holiday)
VALUES
(1,'09:00','17:00','12:00','Tuesday'),
(2,'09:00','17:00','12:00','Friday'),
(3,'09:00','17:00','12:00','Sunday'),
(4,'09:00','17:00','12:00','Wednesday'),
(5,'09:00','17:00','12:00','Friday')
;

INSERT INTO PatientsFillHistory(patient,history)
VALUES
('mahmoud@gmail.com', 1),
('mohamed@gmail.com', 2),
('ali@gmail.com', 3)
;

INSERT INTO Diagnose(appt,doctor,diagnosis,prescription)
VALUES
(1,'ahmed@gmail.com', 'Bloating', 'Ibuprofen as needed'),
(2,'hasan@gmail.com', 'Muscle soreness', 'Stretch morning/night'),
(3,'hasan@gmail.com', 'Vitamin Deficiency', 'Good Diet')
;

INSERT INTO DocsHaveSchedules(sched,doctor)
VALUES
(1,'ahmed@gmail.com'),
(2,'hasan@gmail.com')
;

INSERT INTO DoctorViewsHistory(history,doctor)
VALUES
(1,'ahmed@gmail.com'),
(2,'ahmed@gmail.com'),
(3,'hasan@gmail.com')
;

INSERT INTO ScheduleAppointment(sched,doctor)
VALUES
(1,'ahmed@gmail.com'),
(2,'ahmed@gmail.com'),
(3,'hasan@gmail.com')
;

---------------------------------------------------------stored procedure------------------------------------
USE [HospitalManagementSystem]

CREATE PROCEDURE Addappointment
    @appointment_id INT,
	@date DATE,
    @start_time TIME,
    @end_time TIME,
    @status VARCHAR(150)
AS
BEGIN
    DECLARE @app_id int;
    SELECT @app_id = appointment_id
    FROM Appointment
    WHERE appointment_id = @appointment_id;

    IF @app_id IS NOT NULL
    BEGIN
		RAISERROR ('Appointment ID does exist in the database.', 16, 1);
        RETURN;
    END

    INSERT INTO Appointment(appointment_id, date, starttime, endtime, status)
    VALUES (@appointment_id, @date, @start_time, @end_time, @status);
END;

--##################################################################################################

USE [HospitalManagementSystem]

CREATE PROCEDURE Adddiagnose
    @appointment_id INT,
	@email VARCHAR(50),
    @diagnose VARCHAR(50),
    @prescription VARCHAR(100)
AS
BEGIN
    DECLARE @app_id int;
	DECLARE @doc_email VARCHAR(50);
    SELECT @app_id = appt, @doc_email = doctor
    FROM Diagnose
    WHERE appt = @appointment_id AND doctor = @email;

    IF @app_id IS NOT NULL And @doc_email IS NOT NULL
    BEGIN
		RAISERROR ('Diagnose does exist in the database.', 16, 1);
        RETURN;
    END

    INSERT INTO Diagnose(appt, doctor, diagnosis, prescription)
    VALUES (@appointment_id, @email, @diagnose, @prescription);
END;

--########################################################################################################

USE [HospitalManagementSystem]

CREATE PROCEDURE AddSchedule
    @schedule_id INT,
    @start_time VARCHAR(50),
    @end_time VARCHAR(50),
    @break_time VARCHAR(50),
    @doctor_holiday VARCHAR(150),
    @email VARCHAR(50)
AS
BEGIN
    DECLARE @doc_email VARCHAR(50);
    SELECT @doc_email = email
    FROM Doctor
    WHERE Doctor.email = @email;

    IF @doc_email IS NULL
    BEGIN
		RAISERROR ('Doctor''s email does not exist in the database.', 16, 1);
        RETURN;
    END

    INSERT INTO Schedule (schedule_id, doctor_email, starttime, endtime, breaktime, holiday)
    VALUES (@schedule_id, @doc_email, @start_time, @end_time, @break_time, @doctor_holiday);
END;


--#####################################################################################################################

USE [HospitalManagementSystem]

CREATE PROCEDURE GetMedicalHistory
AS
BEGIN
    SELECT 
        MH_id AS [Medical History ID],
        [date&time] AS [Date and Time],
        conditions,
        medication,
        patient_email AS [Patient Email],
        name,
        address,
        gender
    FROM MedicalHistory
    INNER JOIN Patient
        ON MedicalHistory.patient_email = Patient.email;
END;