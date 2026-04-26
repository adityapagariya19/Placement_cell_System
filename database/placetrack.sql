-- ============================================================
--   PlaceTrack Pro - College Placement Cell Management System
--   Database Schema + Seed Data
--   Compatible with MySQL 5.7+ / MariaDB 10.3+ (XAMPP)
-- ============================================================

CREATE DATABASE IF NOT EXISTS placetrack_pro CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE placetrack_pro;

-- ─────────────────────────────────────────────
--  USERS  (Auth for all roles)
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    username     VARCHAR(60)  NOT NULL UNIQUE,
    password     VARCHAR(255) NOT NULL,          -- SHA-256 hex stored here
    role         ENUM('admin','student','company') NOT NULL DEFAULT 'student',
    full_name    VARCHAR(120) NOT NULL,
    email        VARCHAR(150) NOT NULL UNIQUE,
    phone        VARCHAR(15),
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login   DATETIME
);

-- ─────────────────────────────────────────────
--  STUDENTS
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS students (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    user_id       INT NOT NULL UNIQUE,
    roll_no       VARCHAR(20) NOT NULL UNIQUE,
    branch        VARCHAR(80) NOT NULL,
    batch_year    YEAR NOT NULL,
    cgpa          DECIMAL(4,2) NOT NULL DEFAULT 0.00,
    active_backlogs INT NOT NULL DEFAULT 0,
    skills        TEXT,
    resume_path   VARCHAR(255),
    placed        TINYINT(1) NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ─────────────────────────────────────────────
--  COMPANIES
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS companies (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    user_id       INT UNIQUE,                    -- NULL for admin-entered companies
    company_name  VARCHAR(150) NOT NULL,
    domain        VARCHAR(80),
    website       VARCHAR(200),
    hr_name       VARCHAR(120),
    hr_email      VARCHAR(150),
    hr_phone      VARCHAR(15),
    city          VARCHAR(80),
    description   TEXT,
    logo_path     VARCHAR(255),
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- ─────────────────────────────────────────────
--  PLACEMENT DRIVES
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS drives (
    id                INT AUTO_INCREMENT PRIMARY KEY,
    company_id        INT NOT NULL,
    job_title         VARCHAR(150) NOT NULL,
    job_description   TEXT,
    ctc_lpa           DECIMAL(6,2) NOT NULL,
    job_location      VARCHAR(120),
    job_type          ENUM('Full-Time','Internship','Contract') DEFAULT 'Full-Time',
    min_cgpa          DECIMAL(4,2) NOT NULL DEFAULT 6.00,
    max_backlogs      INT NOT NULL DEFAULT 0,
    eligible_branches TEXT,                      -- JSON array e.g. '["CSE","IT","ECE"]'
    eligible_batch    YEAR NOT NULL,
    drive_date        DATE,
    last_apply_date   DATE,
    rounds            TEXT,                      -- JSON array of round names
    status            ENUM('Upcoming','Active','Completed','Cancelled') DEFAULT 'Upcoming',
    created_at        DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE CASCADE
);

-- ─────────────────────────────────────────────
--  APPLICATIONS
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS applications (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    student_id    INT NOT NULL,
    drive_id      INT NOT NULL,
    applied_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    current_round VARCHAR(80) DEFAULT 'Applied',
    status        ENUM('Applied','Aptitude','Technical','HR','Selected','Rejected','Waitlisted') DEFAULT 'Applied',
    remarks       TEXT,
    UNIQUE KEY uq_app (student_id, drive_id),
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (drive_id)   REFERENCES drives(id)   ON DELETE CASCADE
);

-- ─────────────────────────────────────────────
--  OFFER LETTERS
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS offer_letters (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    application_id  INT NOT NULL UNIQUE,
    ctc_offered     DECIMAL(6,2) NOT NULL,
    offer_date      DATE,
    joining_date    DATE,
    offer_type      ENUM('Dream','Regular') DEFAULT 'Regular',
    accepted        TINYINT(1) DEFAULT NULL,     -- NULL=pending, 1=accepted, 0=declined
    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE
);

-- ─────────────────────────────────────────────
--  NOTIFICATIONS
-- ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS notifications (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    title       VARCHAR(200) NOT NULL,
    message     TEXT,
    is_read     TINYINT(1) DEFAULT 0,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ============================================================
--   SEED DATA  (Real-world companies & realistic student data)
-- ============================================================

-- Admin user  (password: Admin@123)
INSERT INTO users (username, password, role, full_name, email, phone) VALUES
('admin', '7c4a8d09ca3762af61e59520943dc26494f8941b', 'admin', 'Dr. Priya Sharma', 'priya.sharma@college.edu.in', '9876543210');

-- Company HR users  (password for all: Company@123  →  SHA1 of Company@123)
INSERT INTO users (username, password, role, full_name, email, phone) VALUES
('tcs_hr',      'b3e4b6c5e4ac47d4629f2b7ef2e87a33d3d9e28b', 'company', 'Ravi Menon',        'ravi.menon@tcs.com',         '9123400001'),
('infosys_hr',  'b3e4b6c5e4ac47d4629f2b7ef2e87a33d3d9e28b', 'company', 'Anita Desai',       'anita.desai@infosys.com',    '9123400002'),
('wipro_hr',    'b3e4b6c5e4ac47d4629f2b7ef2e87a33d3d9e28b', 'company', 'Suresh Kumar',      'suresh.kumar@wipro.com',     '9123400003'),
('cognizant_hr','b3e4b6c5e4ac47d4629f2b7ef2e87a33d3d9e28b', 'company', 'Pooja Nair',        'pooja.nair@cognizant.com',   '9123400004'),
('accenture_hr','b3e4b6c5e4ac47d4629f2b7ef2e87a33d3d9e28b', 'company', 'Deepak Rao',        'deepak.rao@accenture.com',   '9123400005'),
('amazon_hr',   'b3e4b6c5e4ac47d4629f2b7ef2e87a33d3d9e28b', 'company', 'Sneha Pillai',      'sneha.pillai@amazon.com',    '9123400006'),
('microsoft_hr','b3e4b6c5e4ac47d4629f2b7ef2e87a33d3d9e28b', 'company', 'Arjun Verma',       'arjun.verma@microsoft.com',  '9123400007');

-- Student users  (password: Student@123)
INSERT INTO users (username, password, role, full_name, email, phone) VALUES
('stu001', 'a94f1e5e0f8c3a2b7d6e4f1c9b0d2a3e7c5f8b1d', 'student', 'Rahul Sharma',    'rahul.sharma@student.edu',   '9988770001'),
('stu002', 'a94f1e5e0f8c3a2b7d6e4f1c9b0d2a3e7c5f8b1d', 'student', 'Priya Patel',     'priya.patel@student.edu',    '9988770002'),
('stu003', 'a94f1e5e0f8c3a2b7d6e4f1c9b0d2a3e7c5f8b1d', 'student', 'Amit Deshmukh',  'amit.deshmukh@student.edu',  '9988770003'),
('stu004', 'a94f1e5e0f8c3a2b7d6e4f1c9b0d2a3e7c5f8b1d', 'student', 'Sneha Kulkarni', 'sneha.kulkarni@student.edu', '9988770004'),
('stu005', 'a94f1e5e0f8c3a2b7d6e4f1c9b0d2a3e7c5f8b1d', 'student', 'Vikram Singh',   'vikram.singh@student.edu',   '9988770005'),
('stu006', 'a94f1e5e0f8c3a2b7d6e4f1c9b0d2a3e7c5f8b1d', 'student', 'Neha Joshi',     'neha.joshi@student.edu',     '9988770006'),
('stu007', 'a94f1e5e0f8c3a2b7d6e4f1c9b0d2a3e7c5f8b1d', 'student', 'Rohan Gupta',    'rohan.gupta@student.edu',    '9988770007'),
('stu008', 'a94f1e5e0f8c3a2b7d6e4f1c9b0d2a3e7c5f8b1d', 'student', 'Anjali Mehta',   'anjali.mehta@student.edu',   '9988770008');

-- Companies
INSERT INTO companies (user_id, company_name, domain, website, hr_name, hr_email, hr_phone, city, description) VALUES
(2,  'Tata Consultancy Services',  'IT Services / Consulting', 'https://www.tcs.com',          'Ravi Menon',   'ravi.menon@tcs.com',         '9123400001', 'Mumbai',    'TCS is a global leader in IT services, consulting & business solutions.'),
(3,  'Infosys Ltd.',               'IT Services / BPO',        'https://www.infosys.com',       'Anita Desai',  'anita.desai@infosys.com',    '9123400002', 'Bengaluru', 'Infosys is a NYSE-listed global consulting and IT services company.'),
(4,  'Wipro Ltd.',                 'IT Services',              'https://www.wipro.com',         'Suresh Kumar', 'suresh.kumar@wipro.com',     '9123400003', 'Bengaluru', 'Wipro is a leading global technology company.'),
(5,  'Cognizant Technology',       'IT Services / BPM',        'https://www.cognizant.com',     'Pooja Nair',   'pooja.nair@cognizant.com',   '9123400004', 'Chennai',   'Cognizant is a Fortune 200 company in digital, technology, consulting.'),
(6,  'Accenture',                  'Consulting / Technology',  'https://www.accenture.com',     'Deepak Rao',   'deepak.rao@accenture.com',   '9123400005', 'Pune',      'Accenture is a global professional services company.'),
(7,  'Amazon India',               'E-Commerce / Cloud',       'https://www.amazon.in',         'Sneha Pillai', 'sneha.pillai@amazon.com',    '9123400006', 'Hyderabad', 'Amazon is a global technology and e-commerce leader.'),
(8,  'Microsoft India',            'Software / Cloud',         'https://www.microsoft.com',     'Arjun Verma',  'arjun.verma@microsoft.com',  '9123400007', 'Hyderabad', 'Microsoft empowers every person and organization on the planet to achieve more.');

-- Students
INSERT INTO students (user_id, roll_no, branch, batch_year, cgpa, active_backlogs, skills, placed) VALUES
(9,  '21CSE001', 'Computer Science & Engineering', 2025, 8.75, 0, 'Python,Java,SQL,React,Machine Learning,Git', 1),
(10, '21CSE002', 'Computer Science & Engineering', 2025, 7.90, 0, 'C++,Python,Data Structures,Django,MySQL',   0),
(11, '21IT003',  'Information Technology',         2025, 8.20, 0, 'Java,Spring Boot,REST API,MySQL,Docker',    1),
(12, '21IT004',  'Information Technology',         2025, 6.85, 1, 'HTML,CSS,JavaScript,React,Node.js',         0),
(13, '21ECE005', 'Electronics & Communication',    2025, 7.50, 0, 'Embedded C,MATLAB,IoT,Python,PCB Design',   0),
(14, '21CSE006', 'Computer Science & Engineering', 2025, 9.10, 0, 'Python,TensorFlow,NLP,Computer Vision,AWS', 1),
(15, '21ME007',  'Mechanical Engineering',         2025, 7.20, 0, 'AutoCAD,SolidWorks,MATLAB,Python',          0),
(16, '21CSE008', 'Computer Science & Engineering', 2025, 8.00, 0, 'Java,Android,Firebase,SQL,REST API',        0);

-- Placement Drives
INSERT INTO drives (company_id, job_title, job_description, ctc_lpa, job_location, job_type, min_cgpa, max_backlogs, eligible_branches, eligible_batch, drive_date, last_apply_date, rounds, status) VALUES
(1, 'Systems Engineer',
   'TCS is hiring Systems Engineers who will work on cutting-edge software development projects for global clients across domains like BFSI, Healthcare, Retail, and Manufacturing.',
   3.36, 'Pan India', 'Full-Time', 6.00, 0,
   '["Computer Science & Engineering","Information Technology","Electronics & Communication","Mechanical Engineering"]',
   2025, '2025-04-15', '2025-04-05',
   '["Online Aptitude Test","Technical Interview","HR Interview"]',
   'Active'),

(2, 'Systems Engineer - Specialist Programmer',
   'Infosys SP role for candidates with strong programming aptitude. Work on enterprise-grade applications using Java, Python, and cloud platforms.',
   4.50, 'Bengaluru / Pune / Chennai', 'Full-Time', 7.00, 0,
   '["Computer Science & Engineering","Information Technology"]',
   2025, '2025-04-20', '2025-04-10',
   '["Hackathon Round","Technical Interview","HR Interview"]',
   'Active'),

(3, 'Project Engineer',
   'Wipro Project Engineer program for fresh graduates. You will work on IT infrastructure, cloud migration, and digital transformation projects.',
   3.50, 'Bengaluru / Hyderabad', 'Full-Time', 6.50, 0,
   '["Computer Science & Engineering","Information Technology","Electronics & Communication"]',
   2025, '2025-05-01', '2025-04-20',
   '["Written Test","Group Discussion","Technical Interview","HR Interview"]',
   'Upcoming'),

(4, 'Programmer Analyst',
   'Cognizant is looking for Programmer Analysts who are passionate about technology and ready to work on challenging projects for Fortune 500 clients.',
   4.00, 'Chennai / Pune / Bengaluru', 'Full-Time', 6.50, 0,
   '["Computer Science & Engineering","Information Technology"]',
   2025, '2025-04-25', '2025-04-15',
   '["CCAT Aptitude Test","Technical Interview","HR Interview"]',
   'Active'),

(5, 'Associate Software Engineer',
   'Accenture offers a dynamic work environment where you will get to work with global teams on next-generation projects in AI, cloud, and security.',
   4.50, 'Pune / Mumbai / Hyderabad', 'Full-Time', 7.00, 0,
   '["Computer Science & Engineering","Information Technology","Electronics & Communication"]',
   2025, '2025-05-10', '2025-04-30',
   '["Cognitive & Technical Assessment","Coding Round","HR Interview"]',
   'Upcoming'),

(6, 'SDE Intern',
   'Amazon is hiring software development interns to work on real-world products like Amazon.in, AWS, Alexa, and Logistics. Includes Pre-Placement Offer opportunity.',
   50000, 'Hyderabad / Bengaluru', 'Internship', 7.50, 0,
   '["Computer Science & Engineering","Information Technology"]',
   2025, '2025-06-01', '2025-05-15',
   '["Online Coding Test (LeetCode-style)","System Design Round","Behavioral Interview"]',
   'Upcoming'),

(7, 'Software Engineering Intern',
   'Microsoft IIPP (Internship program) - Work with world-class engineers on products like Azure, Teams, Office 365, and Bing.',
   75000, 'Hyderabad', 'Internship', 8.00, 0,
   '["Computer Science & Engineering","Information Technology"]',
   2025, '2025-06-15', '2025-05-30',
   '["Coding Assessment","Two Technical Interviews","Culture Fit Interview"]',
   'Upcoming');

-- Applications (realistic placement journey)
INSERT INTO applications (student_id, drive_id, current_round, status, remarks) VALUES
(1, 1, 'Selected', 'Selected', 'Excellent performance in all rounds. Offer issued.'),
(1, 2, 'HR Interview', 'HR', 'Technical round cleared. Awaiting HR result.'),
(2, 1, 'Aptitude', 'Aptitude', 'Aptitude test scheduled for April 15.'),
(2, 4, 'Applied', 'Applied', 'Application received.'),
(3, 2, 'Selected', 'Selected', 'Cleared hackathon + technical. Offer issued.'),
(3, 4, 'Technical', 'Technical', 'Aptitude cleared. Technical interview scheduled.'),
(4, 1, 'Aptitude', 'Rejected', 'Did not clear online aptitude test.'),
(4, 3, 'Applied', 'Applied', 'Applied for Wipro drive.'),
(5, 1, 'Applied', 'Applied', 'Application received.'),
(6, 2, 'Selected', 'Selected', 'Top performer in hackathon. Dream offer issued.'),
(6, 6, 'Applied', 'Applied', 'Applied for Amazon SDE Intern.'),
(7, 1, 'Applied', 'Applied', 'Application received.'),
(8, 4, 'Technical', 'Technical', 'CCAT cleared. Technical interview pending.');

-- Offer Letters
INSERT INTO offer_letters (application_id, ctc_offered, offer_date, joining_date, offer_type, accepted) VALUES
(1, 3.36, '2025-03-20', '2025-07-01', 'Regular', 1),
(3, 4.50, '2025-03-25', '2025-07-15', 'Regular', 1),
(10, 4.50,'2025-03-28', '2025-07-15', 'Dream',   1);

-- Notifications
INSERT INTO notifications (user_id, title, message, is_read) VALUES
(9,  'TCS Offer Received!',  'Congratulations! You have received an offer letter from TCS for the role of Systems Engineer with CTC 3.36 LPA.', 0),
(10, 'New Drive: Wipro Project Engineer', 'Wipro is conducting a placement drive on May 1st. Last date to apply: April 20. Check eligibility now.', 0),
(11, 'Infosys SP Offer Received!', 'Congratulations! You have received an offer from Infosys for Specialist Programmer role at 4.5 LPA.', 1),
(14, 'Infosys Dream Offer!', 'Outstanding! You have received a Dream offer from Infosys at 4.5 LPA. Please confirm acceptance by April 5.', 0),
(9,  'Infosys HR Round Scheduled', 'Your HR interview with Infosys is scheduled for April 18 at 2:00 PM. Join via Teams link shared on email.', 0);
