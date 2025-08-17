-- To DROP Database
DROP DATABASE IF EXISTS project_698;

-- Create a DataBase Madhavi Clinical Laboratory System
CREATE DATABASE project_698;

-- Use the new DataBase to create Tables
USE project_698;
-- SHOW TABLES;

-- We use 'DROP TABLE IF EXISTS' to drop tables if they already exist --
DROP TABLE IF EXISTS ordered_tests;
DROP TABLE IF EXISTS patient_details;
DROP TABLE IF EXISTS staff;
DROP TABLE IF EXISTS diagnostic_test_info;
DROP TABLE IF EXISTS patient_reports;

-- Creating the Staff Table --
CREATE TABLE IF NOT EXISTS staff (
    staff_username VARCHAR(50) PRIMARY KEY, -- Unique identifier for each staff member
    staff_first_name VARCHAR(50),
    staff_last_name VARCHAR(50),
    password VARCHAR(255) NOT NULL, -- Store hashed passwords
    role ENUM('Lab Technician', 'Lab Assistant') NOT NULL, -- Restrict roles to predefined values
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Auto-set the creation timestamp
);


-- Creating the Patient details Table --
CREATE TABLE IF NOT EXISTS patient_details (
	patient_id INT AUTO_INCREMENT PRIMARY KEY,
	registered_by VARCHAR(50),
	registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	patient_first_name VARCHAR(50) NOT NULL,
	patient_last_name VARCHAR(50) NOT NULL,
	patient_email VARCHAR(100) NOT NULL UNIQUE,
	date_of_birth DATE NOT NULL,
	Age INT,
	Gender ENUM('Male', 'Female', 'Other') NOT NULL,
	Street_Address VARCHAR(255),
	City VARCHAR(100) NOT NULL,
	State VARCHAR(50) NOT NULL,
	Zipcode VARCHAR(10),
	Contact_Phone VARCHAR(15) UNIQUE NOT NULL,
    FOREIGN KEY (registered_by) REFERENCES Staff(staff_username) ON DELETE SET NULL,
    CHECK (LENGTH(Zipcode) BETWEEN 5 AND 10), -- Ensure valid Zipcode length
    CHECK (LENGTH(Contact_Phone) BETWEEN 10 AND 15) -- Ensure valid phone number format
);



-- Creating the Diagnostic test Information Table --
CREATE TABLE IF NOT EXISTS diagnostic_test_info (
    test_id INT PRIMARY KEY AUTO_INCREMENT, -- Unique ID for each test
    test_code VARCHAR(20) UNIQUE NOT NULL, -- Unique short code for the test (e.g., HB1, WBC01)
    test_name VARCHAR(100) NOT NULL, -- Full test name (e.g., Hemoglobin, WBC Count)
    normal_values VARCHAR(50), -- Reference range for the test (e.g., 13.5-17.5 g/dL)
    units VARCHAR(20), -- Measurement unit (e.g., g/dL, mg/dL, uL)
     is_available BOOLEAN DEFAULT 1 -- To select availability 
);

-- Creating the patient reports Table --alter
CREATE TABLE IF NOT EXISTS patient_reports (
    report_id INT PRIMARY KEY AUTO_INCREMENT,
    report_status ENUM('Pending', 'Completed', 'Reviewed') NOT NULL,
    report_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    file_path VARCHAR(255) NOT NULL
);

-- Creating the Ordered Tests Table --
CREATE TABLE IF NOT EXISTS ordered_tests (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    patient_id INT NOT NULL,
    test_id INT NOT NULL,
    report_id INT NOT NULL,
    result_value VARCHAR(50) NOT NULL,
    tested_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patient_details(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (test_id) REFERENCES diagnostic_test_info(test_id) ON DELETE CASCADE,
    FOREIGN KEY (report_id) REFERENCES patient_reports(report_id) ON DELETE CASCADE
);

INSERT INTO staff (staff_username, staff_first_name, staff_last_name, password, role) VALUES
('jwilson', 'James', 'Wilson', '$2a$10$RmhzQnyJWZFyO3WGe0Pq.eUYt5FhRF.IEfIrWCnJF1Zp4RNT3eQoC', 'Lab Technician'),
('msmith', 'Mary', 'Smith', '$2b$12$Ap85./F7.mpZfYHWV1mzsOtJP0yzuo.koI7Cft6xGWhS0QVG3f8dK', 'Lab Assistant'),
('sbrown', 'Sarah', 'Brown', '$2b$12$dUWQhyDG4PGMtF7fuR97uejR69MEipB0rUYL4E8wfag3i1umZrtdm', 'Lab Assistant'),
('llee', 'Lisa', 'Lee', '$2b$12$M3OsuhKTLWGW/C6PmHUSPOwPI./pZqXB2xNAgmL/smG5jFzwCtHAm', 'Lab Assistant');

-- Insert Sample Data for Patient details Table (30+ records)
INSERT INTO patient_details (patient_id, registered_by, registration_date, patient_first_name, patient_last_name, patient_email, date_of_birth, Age, Gender, Street_Address, City, State, Zipcode, Contact_Phone) 
VALUES 
(1, 'jwilson', '2023-09-02', 'Romonda', 'Budgey', 'rbudgey0@nasa.gov', '1978-02-02', '58', 'Female', '069 Rusk Road', 'Philadelphia', 'Pennsylvania', '19120', '215-260-8493'),
(2, 'msmith', '2023-12-05', 'Saudra', 'Du Pre', 'sdupre1@dagondesign.com', '1945-08-08', '69', 'Female', '624 Sycamore Way', 'Minneapolis', 'Minnesota', '55441', '952-627-0415'),
(3, 'llee', '2025-02-04', 'Amalita', 'Ashwood', 'aashwood2@uiuc.edu', '1942-12-04', '92', 'Female', '46 Evergreen Place', 'Grand Rapids', 'Michigan', '49518', '616-157-0336'),
(4, 'llee', '2024-05-06', 'Darill', 'Potte', 'dpotte3@php.net', '1987-04-28', '72', 'Male', '1 Menomonie Terrace', 'Houston', 'Texas', '77240', '713-173-2579'),
(5, 'jwilson', '2023-04-14', 'Annadiane', 'Zanetello', 'azanetello4@java.com', '1960-12-24', '20', 'Female', '48 Anderson Terrace', 'Cleveland', 'Ohio', '44185', '216-200-9238'),
(6, 'jwilson', '2024-06-13', 'Roderic', 'Stitcher', 'rstitcher5@twitter.com', '1936-08-12', '52', 'Male', '6 Shelley Plaza', 'Louisville', 'Kentucky', '40250', '502-438-8234'),
(7, 'msmith', '2023-11-22', 'Bernadene', 'Botterell', 'bbotterell6@dion.ne.jp', '1955-04-23', '10', 'Female', '5232 Birchwood Pass', 'Brockton', 'Massachusetts', '02305', '508-563-2777'),
(8, 'msmith', '2024-03-30', 'Drusilla', 'Pursey', 'dpursey7@bbc.co.uk', '2002-04-14', '61', 'Female', '95 Artisan Circle', 'San Diego', 'California', '92160', '619-488-5987'),
(9, 'llee', '2023-07-20', 'Chrotoem', 'Howsin', 'chowsin8@hexun.com', '1944-11-05', '62', 'Male', '5930 Warner Terrace', 'Dayton', 'Ohio', '45454', '937-362-3360'),
(10, 'sbrown', '2024-03-01', 'Maddie', 'Mapowder', 'mmapowder9@dmoz.org', '1962-05-15', '83', 'Female', '71 Ramsey Avenue', 'Worcester', 'Massachusetts', '01605', '508-314-6365'),
(11, 'llee', '2024-08-24', 'Devlin', 'McKinn', 'dmckinna@php.net', '1935-01-06', '71', 'Male', '096 Birchwood Avenue', 'Houston', 'Texas', '77299', '713-545-0535'),
(12, 'jwilson', '2024-03-04', 'Hans', 'Coils', 'hcoilsb@businessinsider.com', '1951-01-26', '38', 'Male', '239 Redwing Trail', 'Jersey City', 'New Jersey', '07310', '973-136-1068'),
(13, 'sbrown', '2023-12-12', 'Klaus', 'Brosetti', 'kbrosettic@marketwatch.com', '1967-06-23', '94', 'Male', '16 Bellgrove Way', 'Alhambra', 'California', '91841', '626-906-5724'),
(14, 'jwilson', '2023-09-03', 'Ina', 'Babst', 'ibabstd@chronoengine.com', '2000-12-17', '62', 'Female', '665 Mosinee Road', 'San Diego', 'California', NULL, '619-121-6573'),
(15, 'llee', '2024-09-05', 'Tansy', 'Brenard', 'tbrenarde@tuttocitta.it', '1964-03-30', '79', 'Female', '32405 Manitowish Pass', 'Johnstown', 'Pennsylvania', '15906', '814-389-1934'),
(16, 'jwilson', '2024-12-23', 'Stormie', 'Puckring', 'spuckringf@google.com.br', '2006-01-10', '31', 'Female', '96279 Dixon Junction', 'Dallas', 'Texas', '75379', '214-456-4478'),
(17, 'sbrown', '2024-07-25', 'Frank', 'Giroldi', 'fgiroldig@msu.edu', '1977-01-23', '02', 'Male', '24265 Lake View Park', 'Akron', 'Ohio', '44329', '330-976-2046'),
(18, 'jwilson', '2024-12-07', 'Mar', 'Mozzi', 'mmozzih@purevolume.com', '1992-06-13', '88', 'Male', '128 Bluejay Court', 'Charlotte', 'North Carolina', '28278', '704-816-2138'),
(19, 'llee', '2023-03-31', 'Francisco', 'Topp', 'ftoppi@usatoday.com', '1963-08-09', '37', 'Male', '2303 Service Drive', 'Tucson', 'Arizona', '85754', '520-304-6852'),
(20, 'sbrown', '2023-10-14', 'Brandi', 'Blais', 'bblaisj@state.gov', '1965-10-25', '46', 'Female', '042 Elka Pass', 'Cleveland', 'Ohio', '44130', '440-480-0618'),
(21, 'llee', '2024-10-16', 'Lynna', 'Partington', 'lpartingtonk@examiner.com', '2005-08-13', '59', 'Female', '62063 Cordelia Street', 'New Orleans', 'Louisiana', '70187', '504-874-7875'),
(22, 'jwilson', '2023-12-31', 'Nikkie', 'Elcoux', 'nelcouxl@jimdo.com', '1961-07-16', '84', 'Female', '5358 Village Green Parkway', 'Shreveport', 'Louisiana', '71137', '318-463-5237'),
(23, 'jwilson', '2024-07-03', 'Immanuel', 'Trask', 'itraskm@foxnews.com', '1962-01-05', '97', 'Male', '07 International Plaza', 'Phoenix', 'Arizona', '85062', '602-975-7439'),
(24, 'sbrown', '2025-02-07', 'Alric', 'Cockerill', 'acockerilln@photobucket.com', '1989-08-27', '62', 'Male', '775 Reindahl Center', 'Carol Stream', 'Illinois', '60351', '309-370-2603'),
(25, 'sbrown', '2023-08-14', 'Constantin', 'Reisenstein', 'creisensteino@csmonitor.com', '1994-03-11', '45', 'Male', '7452 Pennsylvania Junction', 'Honolulu', 'Hawaii', NULL, '808-370-7239'),
(26, 'jwilson', '2024-09-26', 'Suzann', 'Dulton', 'sdultonp@time.com', '1945-04-05', '96', 'Female', '6 Truax Drive', 'Huntsville', 'Alabama', '35810', '256-938-6688'),
(27, 'jwilson', '2024-12-14', 'Jobi', 'Bowkley', 'jbowkleyq@1688.com', '1980-05-24', '15', 'Female', '086 West Road', 'Albuquerque', 'New Mexico', NULL, '505-917-3745'),
(28, 'jwilson', '2024-10-21', 'Gilberto', 'Frankland', 'gfranklandr@dailymotion.com', '1972-10-04', '95', 'Male', '1 Independence Drive', 'Buffalo', 'New York', '14269', '716-750-1944'),
(29, 'sbrown', '2023-07-15', 'Fawne', 'Webby', 'fwebbys@naver.com', '1944-06-03', '55', 'Female', '36004 Meadow Ridge Parkway', 'Oklahoma City', 'Oklahoma', '73190', '405-755-2788'),
(30, 'jwilson', '2023-06-01', 'Glenn', 'Sadat', 'gsadatt@altervista.org', '1998-12-25', '37', 'Female', '1 Golden Leaf Way', 'New Orleans', 'Louisiana', '70154', '504-488-9778'),
(31, 'jwilson', '2024-06-26', 'Robbi', 'Roy', 'rroyu@lycos.com', '2001-01-08', '46', 'Female', '8870 Annamark Alley', 'Chicago', 'Illinois', '60641', '630-184-3413'),
(32, 'sbrown', '2024-11-12', 'Perceval', 'Clogg', 'pcloggv@slideshare.net', '1931-01-15', '64', 'Male', '56309 Rutledge Court', 'Tyler', 'Texas', '75705', '903-670-4298'),
(33, 'jwilson', '2023-12-22', 'Melodee', 'Salerno', 'msalernow@jigsy.com', '1930-11-24', '52', 'Female', '1017 Merchant Circle', 'Muskegon', 'Michigan', '49444', '231-589-7791'),
(34, 'sbrown', '2023-12-10', 'Brier', 'Brass', 'bbrassx@eventbrite.com', '1983-09-05', '67', 'Female', '2 Columbus Street', 'Salt Lake City', 'Utah', '84130', '801-383-2427'),
(35, 'jwilson', '2024-05-28', 'Beulah', 'Gecks', 'bgecksy@pinterest.com', '1997-04-08', '75', 'Female', '1 Hauk Park', 'Savannah', 'Georgia', '31405', '912-916-2836');




-- Insert Sample Data for Diagnostic Test Info Table
INSERT INTO diagnostic_test_info (test_code, test_name, normal_values, units) VALUES
('CBC01', 'Complete Blood Count', 'Various', 'Various'),
('HB01', 'Hemoglobin', '13.5-17.5 (M), 12.0-15.5 (F)', 'g/dL'),
('WBC01', 'White Blood Cell Count', '4.5-11.0', '10^3/μL'),
('PLT01', 'Platelet Count', '150-450', '10^3/μL'),
('GLU01', 'Glucose Fasting', '70-99', 'mg/dL'),
('CHOL01', 'Total Cholesterol', '<200', 'mg/dL'),
('LDL01', 'LDL Cholesterol', '<100', 'mg/dL'),
('HDL01', 'HDL Cholesterol', '>40 (M), >50 (F)', 'mg/dL'),
('TRIG01', 'Triglycerides', '<150', 'mg/dL'),
('HBA1C', 'Hemoglobin A1C', '<5.7', '%'),
('TSH01', 'Thyroid Stimulating Hormone', '0.4-4.0', 'mIU/L'),
('T4F01', 'Free T4', '0.8-1.8', 'ng/dL'),
('CREA01', 'Creatinine', '0.6-1.2 (M), 0.5-1.1 (F)', 'mg/dL'),
('BUN01', 'Blood Urea Nitrogen', '7-20', 'mg/dL'),
('EGFR01', 'eGFR', '>60', 'mL/min/1.73m²'),
('ALT01', 'Alanine Aminotransferase', '7-56', 'U/L'),
('AST01', 'Aspartate Aminotransferase', '10-40', 'U/L'),
('ALP01', 'Alkaline Phosphatase', '44-147', 'U/L'),
('BIL01', 'Total Bilirubin', '0.1-1.2', 'mg/dL'),
('VITD01', 'Vitamin D 25-Hydroxy', '30-100', 'ng/mL'),
('FERR01', 'Ferritin', '20-250 (M), 10-120 (F)', 'ng/mL'),
('IRON01', 'Iron', '65-175 (M), 50-170 (F)', 'μg/dL'),
('TIBC01', 'Total Iron Binding Capacity', '250-450', 'μg/dL'),
('B1201', 'Vitamin B12', '200-900', 'pg/mL'),
('FOL01', 'Folate', '2.7-17.0', 'ng/mL'),
('CRP01', 'C-Reactive Protein', '<3.0', 'mg/L'),
('ESR01', 'Erythrocyte Sedimentation Rate', '0-15 (M), 0-20 (F)', 'mm/hr'),
('URIC01', 'Uric Acid', '3.4-7.0 (M), 2.4-6.0 (F)', 'mg/dL'),
('CA01', 'Calcium', '8.6-10.3', 'mg/dL'),
('K01', 'Potassium', '3.5-5.0', 'mmol/L');

-- Insert Sample Data for Patient Reports Table (30+ records)
INSERT INTO patient_reports (report_status, report_date, file_path) VALUES
('Completed', '2024-03-01 10:15:00', '/reports/2024/03/01/report_10001.pdf'),
('Completed', '2024-03-01 11:30:00', '/reports/2024/03/01/report_10002.pdf'),
('Completed', '2024-03-02 09:45:00', '/reports/2024/03/02/report_10003.pdf'),
('Completed', '2024-03-02 14:20:00', '/reports/2024/03/02/report_10004.pdf'),
('Completed', '2024-03-03 08:30:00', '/reports/2024/03/03/report_10005.pdf'),
('Completed', '2024-03-03 13:15:00', '/reports/2024/03/03/report_10006.pdf'),
('Reviewed', '2024-03-04 10:45:00', '/reports/2024/03/04/report_10007.pdf'),
('Reviewed', '2024-03-04 15:30:00', '/reports/2024/03/04/report_10008.pdf'),
('Completed', '2024-03-05 09:00:00', '/reports/2024/03/05/report_10009.pdf'),
('Completed', '2024-03-05 14:45:00', '/reports/2024/03/05/report_10010.pdf'),
('Pending', '2024-03-06 11:00:00', '/reports/2024/03/06/report_10011.pdf'),
('Pending', '2024-03-06 16:15:00', '/reports/2024/03/06/report_10012.pdf'),
('Completed', '2024-03-07 08:45:00', '/reports/2024/03/07/report_10013.pdf'),
('Reviewed', '2024-03-07 13:30:00', '/reports/2024/03/07/report_10014.pdf'),
('Completed', '2024-03-08 10:20:00', '/reports/2024/03/08/report_10015.pdf'),
('Completed', '2024-03-08 15:00:00', '/reports/2024/03/08/report_10016.pdf'),
('Completed', '2024-03-09 09:15:00', '/reports/2024/03/09/report_10017.pdf'),
('Pending', '2024-03-09 14:30:00', '/reports/2024/03/09/report_10018.pdf'),
('Reviewed', '2024-03-10 08:00:00', '/reports/2024/03/10/report_10019.pdf'),
('Completed', '2024-03-10 13:45:00', '/reports/2024/03/10/report_10020.pdf'),
('Completed', '2024-03-11 10:30:00', '/reports/2024/03/11/report_10021.pdf'),
('Reviewed', '2024-03-11 15:15:00', '/reports/2024/03/11/report_10022.pdf'),
('Completed', '2024-03-12 09:30:00', '/reports/2024/03/12/report_10023.pdf'),
('Completed', '2024-03-12 14:00:00', '/reports/2024/03/12/report_10024.pdf'),
('Pending', '2024-03-13 11:15:00', '/reports/2024/03/13/report_10025.pdf'),
('Reviewed', '2024-03-13 16:30:00', '/reports/2024/03/13/report_10026.pdf'),
('Completed', '2024-03-14 08:15:00', '/reports/2024/03/14/report_10027.pdf'),
('Completed', '2024-03-14 13:00:00', '/reports/2024/03/14/report_10028.pdf'),
('Reviewed', '2024-03-15 10:00:00', '/reports/2024/03/15/report_10029.pdf'),
('Completed', '2024-03-15 15:45:00', '/reports/2024/03/15/report_10030.pdf'),
('Pending', '2024-03-16 09:45:00', '/reports/2024/03/16/report_10031.pdf'),
('Completed', '2024-03-16 14:15:00', '/reports/2024/03/16/report_10032.pdf');

-- Insert Sample Data for Ordered Tests Table (30+ records)
INSERT INTO ordered_tests (patient_id, test_id, report_id, result_value, tested_date) VALUES
(1, 2, 1, '14.2', '2024-03-01 10:00:00'),   -- John Doe, Hemoglobin
(1, 3, 1, '6.5', '2024-03-01 10:05:00'),    -- John Doe, WBC Count
(2, 6, 2, '185', '2024-03-01 11:20:00'),    -- Jane Smith, Total Cholesterol
(2, 7, 2, '92', '2024-03-01 11:25:00'),     -- Jane Smith, LDL Cholesterol
(3, 5, 3, '98', '2024-03-02 09:30:00'),     -- Michael Johnson, Glucose Fasting
(3, 10, 3, '5.5', '2024-03-02 09:35:00'),   -- Michael Johnson, Hemoglobin A1C
(4, 11, 4, '2.5', '2024-03-02 14:00:00'),   -- Emily Brown, TSH
(4, 12, 4, '1.2', '2024-03-02 14:05:00'),   -- Emily Brown, Free T4
(5, 2, 5, '15.5', '2024-03-03 08:15:00'),   -- William Davis, Hemoglobin
(5, 4, 5, '215', '2024-03-03 08:20:00'),    -- William Davis, Platelet Count
(6, 20, 6, '45', '2024-03-03 13:00:00'),    -- Sophia Wilson, Vitamin D
(6, 21, 6, '75', '2024-03-03 13:05:00'),    -- Sophia Wilson, Ferritin
(7, 13, 7, '0.9', '2024-03-04 10:30:00'),   -- Daniel Martinez, Creatinine
(7, 14, 7, '15', '2024-03-04 10:35:00'),    -- Daniel Martinez, BUN
(8, 16, 8, '30', '2024-03-04 15:15:00'),    -- Olivia Anderson, ALT
(8, 17, 8, '25', '2024-03-04 15:20:00'),    -- Olivia Anderson, AST
(9, 6, 9, '210', '2024-03-05 08:45:00'),    -- James Taylor, Total Cholesterol
(9, 9, 9, '170', '2024-03-05 08:50:00'),    -- James Taylor, Triglycerides
(10, 2, 10, '12.5', '2024-03-05 14:30:00'), -- Emma Thomas, Hemoglobin
(10, 21, 10, '80', '2024-03-05 14:35:00'),  -- Emma Thomas, Ferritin
(11, 5, 11, '105', '2024-03-06 10:45:00'),  -- Alexander Clark, Glucose Fasting
(12, 10, 12, '5.9', '2024-03-06 16:00:00'), -- Mia Rodriguez, Hemoglobin A1C
(13, 6, 13, '190', '2024-03-07 08:30:00'),  -- Benjamin Lee, Total Cholesterol
(14, 20, 14, '28', '2024-03-07 13:15:00'),  -- Ava Walker, Vitamin D
(15, 3, 15, '9.5', '2024-03-08 10:05:00'),  -- Henry Gonzalez, WBC Count
(16, 26, 16, '2.5', '2024-03-08 14:45:00'), -- Charlotte Harris, CRP
(17, 11, 17, '3.2', '2024-03-09 09:00:00'), -- Lucas Young, TSH
(18, 2, 18, '13.8', '2024-03-09 14:15:00'), -- Amelia King, Hemoglobin
(19, 16, 19, '35', '2024-03-10 07:45:00'),  -- Ethan Wright, ALT
(20, 20, 20, '38', '2024-03-10 13:30:00'),  -- Isabella Lopez, Vitamin D
(21, 5, 21, '92', '2024-03-11 10:15:00'),   -- Mason Hill, Glucose Fasting
(22, 6, 22, '175', '2024-03-11 15:00:00'),  -- Harper Scott, Total Cholesterol
(23, 28, 23, '5.2', '2024-03-12 09:15:00'), -- Noah Green, Uric Acid
(24, 2, 24, '12.8', '2024-03-12 13:45:00'), -- Evelyn Adams, Hemoglobin
(25, 4, 25, '350', '2024-03-13 11:00:00'),  -- Logan Baker, Platelet Count
(26, 13, 26, '0.8', '2024-03-13 16:15:00'), -- Abigail Nelson, Creatinine
(27, 10, 27, '6.1', '2024-03-14 08:00:00'), -- Jackson Carter, Hemoglobin A1C
(28, 2, 28, '13.2', '2024-03-14 12:45:00'), -- Elizabeth Mitchell, Hemoglobin
(29, 6, 29, '195', '2024-03-15 09:45:00'),  -- Sebastian Perez, Total Cholesterol
(30, 21, 30, '85', '2024-03-15 15:30:00'),  -- Scarlett Roberts, Ferritin
(1, 5, 31, '95', '2024-03-16 09:30:00'),    -- John Doe, Glucose Fasting (follow-up)
(2, 11, 32, '2.1', '2024-03-16 14:00:00');  -- Jane Smith, TSH (follow-up)




