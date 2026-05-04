<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:1a2332,100:1e3a5f&height=220&section=header&text=PlaceTrack%20Pro&fontSize=60&fontColor=4da6ff&fontAlignY=38&desc=College%20Placement%20Cell%20Management%20System&descAlignY=58&descSize=20&animation=fadeIn" width="100%"/>

<br/>

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-XAMPP-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-1F6AA5?style=for-the-badge&logo=python&logoColor=white)
![OOP](https://img.shields.io/badge/Paradigm-OOP-FF6B35?style=for-the-badge&logo=buffer&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-00C853?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Made with Love](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F%20in%20India-ff69b4?style=for-the-badge)

<br/>

> ### *"Most colleges still track placements on Excel sheets and WhatsApp messages.*
> ### *We thought — there has to be a better way. So we built it."* 💻

<br/>

[🚀 Features](#-key-features) &nbsp;•&nbsp; [📸 Screenshots](#-screenshots) &nbsp;•&nbsp; [⚙️ Setup](#-installation--setup) &nbsp;•&nbsp; [🧩 OOP](#-oop-concepts-used) &nbsp;•&nbsp; [🗄️ Database](#-database-schema) &nbsp;•&nbsp; [👥 Team](#-team)

<br/>

</div>

---

## 📌 Table of Contents

- [About The Project](#-about-the-project)
- [Key Features](#-key-features)
- [Screenshots](#-screenshots)
- [Tech Stack](#-tech-stack)
- [System Architecture](#-system-architecture)
- [OOP Concepts Used](#-oop-concepts-used)
- [Database Schema](#-database-schema)
- [Installation & Setup](#-installation--setup)
- [Project Structure](#-project-structure)
- [Team](#-team)
- [License](#-license)

---

## 🎯 About The Project

**PlaceTrack Pro** is a full-stack desktop application that completely digitizes and streamlines the college placement process. Built with **Python (full OOP architecture)** and **MySQL via XAMPP**, it replaces scattered Excel sheets, WhatsApp broadcasts, and manual tracking with a single unified role-based platform.

### 🔍 Problem It Solves

| ❌ Old Way | ✅ PlaceTrack Pro |
|---|---|
| Excel sheets for student records | Structured MySQL database |
| WhatsApp for drive announcements | In-app Notification Center |
| Manual eligibility checking | Smart Auto-Filter Eligibility Engine |
| No placement analytics | Real-time Dashboard with Charts |
| Paper offer letter tracking | Digital Offer Letter Tracker |
| No round-wise status tracking | Full Drive Pipeline (Applied → Selected) |

---

## ✨ Key Features

### 🔐 3-Role Authentication System
- Secure Login / Register with role-based redirect
- **TPO Admin** → Full system control
- **Student** → Profile, drives, applications, offer letters
- **Company HR** → Post drives, manage applicants, update results

### 🧠 Smart Eligibility Engine
- Auto-filters students by CGPA, branch, backlogs, batch year
- One-click **Notify Eligible** button per drive

### 📋 Drive Pipeline Tracker
```
Applied ──► Aptitude Test ──► Technical Interview ──► HR Round ──► ✅ Selected
                                                                  └──► ❌ Rejected
```

### 📊 Real-Time Analytics Dashboard
- Branch-wise placement % bar charts
- Top recruiters pie chart
- Max CTC per company horizontal bar chart
- Overall placement status donut chart
- Avg CTC, total placed, active drives — all live

### 📩 Offer Letter Tracker
- Multiple offers per student supported
- Dream Offer 🌟 vs Regular Offer flagging
- Accept / Decline / Pending with offer & joining dates

### 🔔 Notification Center
- Drive announcements, offer alerts, interview schedules
- Mark All Read functionality
- Timestamped real-time notifications

### 📁 Placement Reports
- Branch-wise & company-wise breakdowns
- 4 charts embedded: bar, pie, horizontal bar, donut

---

## 📸 Screenshots

### 🔐 Login Screen
> Split-screen design with role selector — Student, Admin, Company HR. Clean dark UI with feature highlights on left panel.

![Login Screen](https://drive.google.com/file/d/1aG48AmlHcPnO40EAZeJyKbJ0VuztlAsL/view?usp=drivesdk)

---

### 📊 Admin Dashboard — Overview
> Real-time stat cards: Total Students · Students Placed · Placement % · Active Drives · Total Companies · Applications · Avg CTC. Branch-wise breakdown table below.

![Admin Dashboard](screenshots/admin_dashboard.png)

---

### 👨‍🎓 Student Management Panel
> Full student database with Roll No, Name, Branch, Batch, CGPA, Backlogs, Skills and live Placement Status. Search bar included.

![Students Panel](screenshots/students.png)

---

### 🏢 New Placement Drive Form
> Create drives with Company selector, Job Title, Description, CTC (LPA), Location, Job Type, Min CGPA, Max Backlogs, Batch Year, Drive Date and Last Apply Date.

![New Drive Form](screenshots/new_drive.png)

---

### 🔔 Notification Center
> Real-time alerts — TCS offer received, Wipro new drive, Infosys Dream Offer, HR round scheduled. Fully timestamped.

![Notifications](screenshots/notifications.png)

---

### 📈 Placement Reports & Analytics
> 4-chart analytics page: Branch-wise Placement % (bar), Top Recruiters by Offers (pie), Max CTC per Company (horizontal bar), Overall Placement Status (donut).

![Reports](screenshots/reports.png)

---

### 🎓 Student Portal — Personal Dashboard
> Personalized welcome with CGPA, batch, backlogs, email. Stat cards for Applications, Eligible Drives, Offers Received. Eligible drive cards listed below with Apply button.

![Student Dashboard](screenshots/student_dashboard.png)

---

### 📄 Offer Letter Management
> All received offers with Company, Role, CTC, Offer Date, Joining Date, Regular/Dream badge and Accepted/Pending/Declined status.

![Offer Letters](screenshots/offer_letters.png)

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.11+ | Core application logic |
| **GUI Framework** | CustomTkinter | Modern dark-themed desktop UI |
| **Database** | MySQL 8.0 via XAMPP | Data storage & queries |
| **DB Connector** | mysql-connector-python | Python ↔ MySQL bridge |
| **Charts** | Matplotlib | Analytics & reports visualization |
| **Image Handling** | Pillow | Icons & image rendering |
| **Local Server** | XAMPP | Apache + MySQL local environment |

---

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────┐
│              PRESENTATION LAYER                  │
│        CustomTkinter Views / UI Screens          │
│   Login | Admin | Student | HR Dashboards        │
└──────────────────┬───────────────────────────────┘
                   │
┌──────────────────▼───────────────────────────────┐
│               CONTROLLER LAYER                   │
│         Business Logic / App Controllers         │
│   Auth | Drive | Application | Report Logic      │
└──────────────────┬───────────────────────────────┘
                   │
┌──────────────────▼───────────────────────────────┐
│                 MODEL LAYER                      │
│       OOP Classes / Data Models / Entities       │
│   User | Student | Admin | Company | Drive       │
└──────────────────┬───────────────────────────────┘
                   │
┌──────────────────▼───────────────────────────────┐
│               DATABASE LAYER                     │
│           MySQL via XAMPP / phpMyAdmin           │
│   users | students | drives | applications       │
└──────────────────────────────────────────────────┘
```

---

## 🧩 OOP Concepts Used

All **4 pillars of Object-Oriented Programming** are demonstrated:

### 1. 🔷 Abstraction
```python
from abc import ABC, abstractmethod

class BaseModule(ABC):
    """Abstract base — forces all modules to implement render & load_data"""

    @abstractmethod
    def render(self):
        pass  # Each UI module must implement its own render()

    @abstractmethod
    def load_data(self):
        pass  # Each module fetches its own data
```

### 2. 🔶 Encapsulation
```python
class DBConnection:
    """Singleton DB class — private credentials, one shared connection"""
    __instance = None

    def __init__(self):
        self.__host = "localhost"      # Private attribute
        self.__user = "root"           # Private attribute
        self.__password = ""           # Private attribute
        self.__database = "placement_cell"

    @staticmethod
    def get_instance():
        if DBConnection.__instance is None:
            DBConnection.__instance = DBConnection()
        return DBConnection.__instance

    def get_connection(self):
        return mysql.connector.connect(
            host=self.__host,
            user=self.__user,
            password=self.__password,
            database=self.__database
        )
```

### 3. 🔹 Inheritance
```python
class User:
    """Base class for all user types"""
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self._password = password   # Protected

    def get_info(self):
        return f"{self.name} ({self.email})"


class Student(User):               # Inherits from User
    def __init__(self, name, email, password, cgpa, branch, roll_no):
        super().__init__(name, email, password)
        self.cgpa = cgpa
        self.branch = branch
        self.roll_no = roll_no
        self.backlogs = 0


class Admin(User):                 # Inherits from User
    def __init__(self, name, email, password):
        super().__init__(name, email, password)
        self.role = "TPO_ADMIN"


class CompanyHR(User):             # Inherits from User
    def __init__(self, name, email, password, company_id):
        super().__init__(name, email, password)
        self.company_id = company_id
```

### 4. 🔸 Polymorphism
```python
# Same method name get_dashboard() — different behaviour per user type
class Student(User):
    def get_dashboard(self):
        return StudentDashboard(self)   # Returns student portal

class Admin(User):
    def get_dashboard(self):
        return AdminDashboard(self)     # Returns TPO admin panel

class CompanyHR(User):
    def get_dashboard(self):
        return HRDashboard(self)        # Returns HR company portal
```

---

## 🗄️ Database Schema

```sql
-- ============================================================
-- PlaceTrack Pro — MySQL Database Schema
-- Import this file into phpMyAdmin as: placement_cell
-- ============================================================

CREATE TABLE users (
    user_id     INT PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(100) UNIQUE NOT NULL,
    password    VARCHAR(255) NOT NULL,
    role        ENUM('admin','student','hr') NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE students (
    student_id  INT PRIMARY KEY AUTO_INCREMENT,
    user_id     INT REFERENCES users(user_id),
    roll_no     VARCHAR(20) UNIQUE,
    branch      VARCHAR(50),
    cgpa        DECIMAL(4,2),
    backlogs    INT DEFAULT 0,
    batch_year  YEAR,
    skills      TEXT,
    resume_path VARCHAR(255)
);

CREATE TABLE companies (
    company_id  INT PRIMARY KEY AUTO_INCREMENT,
    name        VARCHAR(100) NOT NULL,
    domain      VARCHAR(50),
    hr_name     VARCHAR(100),
    hr_email    VARCHAR(100),
    website     VARCHAR(200)
);

CREATE TABLE drives (
    drive_id     INT PRIMARY KEY AUTO_INCREMENT,
    company_id   INT REFERENCES companies(company_id),
    title        VARCHAR(150),
    description  TEXT,
    min_cgpa     DECIMAL(3,2),
    package_lpa  DECIMAL(5,2),
    job_location VARCHAR(200),
    job_type     ENUM('Full-Time','Internship','Contract'),
    deadline     DATE,
    drive_date   DATE,
    branches     TEXT,
    max_backlogs INT DEFAULT 0,
    batch_year   YEAR,
    status       ENUM('upcoming','active','closed')
);

CREATE TABLE applications (
    app_id      INT PRIMARY KEY AUTO_INCREMENT,
    student_id  INT REFERENCES students(student_id),
    drive_id    INT REFERENCES drives(drive_id),
    status      ENUM('applied','aptitude','technical','hr','selected','rejected'),
    applied_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE offer_letters (
    offer_id     INT PRIMARY KEY AUTO_INCREMENT,
    app_id       INT REFERENCES applications(app_id),
    package_lpa  DECIMAL(5,2),
    is_dream     BOOLEAN DEFAULT FALSE,
    status       ENUM('pending','accepted','declined'),
    offer_date   DATE,
    joining_date DATE
);

CREATE TABLE notifications (
    notif_id    INT PRIMARY KEY AUTO_INCREMENT,
    user_id     INT REFERENCES users(user_id),
    title       VARCHAR(150),
    message     TEXT,
    is_read     BOOLEAN DEFAULT FALSE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## ⚙️ Installation & Setup

### ✅ Prerequisites

| Tool | Version | Download |
|---|---|---|
| Python | 3.11+ | https://www.python.org/downloads/ |
| XAMPP | Latest | https://www.apachefriends.org/ |
| Git | Latest | https://git-scm.com/ |

---

### 📋 Step-by-Step Setup

**Step 1 — Clone the Repository**
```bash
git clone https://github.com/adityapagariya19/Placement_cell_System.git
cd Placement_cell_System
```

**Step 2 — Start XAMPP**
1. Open **XAMPP Control Panel**
2. Click **Start** next to **Apache**
3. Click **Start** next to **MySQL**
4. Open browser → go to `http://localhost/phpmyadmin`

**Step 3 — Import Database**
1. In phpMyAdmin → click **"New"** in left sidebar
2. Database name: `placement_cell` → click **Create**
3. Click `placement_cell` → go to **Import** tab
4. Choose file → select `database/placement_cell.sql`
5. Click **Go** ✅

**Step 4 — Install Dependencies**
```bash
pip install -r requirements.txt
```

**Step 5 — Run the App**
```bash
python main.py
```

---

### 🔑 Demo Login Credentials

| Role | Username | Password |
|---|---|---|
| 👨‍💼 Admin (TPO) | `admin` | `Admin@123` |
| 👨‍🎓 Student | `stu001` | `Student@123` |

---

## 📁 Project Structure

```
Placement_cell_System/
│
├── main.py                        ← Entry point
├── requirements.txt               ← Python dependencies
│
├── config/
│   └── db_config.py               ← DB connection (Singleton pattern)
│
├── models/                        ← All OOP Classes
│   ├── user.py                    ← Base User class
│   ├── student.py                 ← Student(User) — Inheritance
│   ├── admin.py                   ← Admin(User) — Inheritance
│   ├── company_hr.py              ← CompanyHR(User) — Inheritance
│   ├── company.py                 ← Company model
│   ├── drive.py                   ← Drive model
│   ├── application.py             ← Application model
│   └── offer_letter.py            ← OfferLetter model
│
├── views/                         ← All UI Screens
│   ├── login_view.py              ← Login / Register
│   ├── admin/
│   │   ├── dashboard_view.py      ← Admin overview + stats
│   │   ├── students_view.py       ← Student management
│   │   ├── companies_view.py      ← Company management
│   │   ├── drives_view.py         ← Drive management
│   │   ├── applications_view.py   ← Applications tracker
│   │   ├── notifications_view.py  ← Notifications
│   │   └── reports_view.py        ← Analytics & charts
│   └── student/
│       ├── dashboard_view.py      ← Student home
│       ├── drives_view.py         ← Available drives
│       ├── applications_view.py   ← My applications
│       ├── offers_view.py         ← Offer letters
│       ├── notifications_view.py  ← Notifications
│       └── profile_view.py        ← My profile
│
├── controllers/
│   └── app_controller.py          ← Main application controller
│
├── database/
│   └── placement_cell.sql         ← Full DB dump — import this!
│
├── screenshots/                   ← UI screenshots (for README)
│   ├── login.png
│   ├── admin_dashboard.png
│   ├── students.png
│   ├── new_drive.png
│   ├── notifications.png
│   ├── reports.png
│   ├── student_dashboard.png
│   └── offer_letters.png
│
└── README.md
```

---

## 👥 Team

<div align="center">

| | Name | Role |
|:---:|---|---|
| 🚀 | **Aditya Pagariya** | Project Lead & Backend Architect |
| 🗄️ | **Omkar Patange** | Database Design & SQL Engineer |
| 🎨 | **Sohel Sayyed** | UI/UX Designer & Frontend Developer |
| ⚙️ | **Shreepad Waghmare** | Business Logic & Module Integration |

**2nd Year · Computer Science & Engineering · 2026**

</div>

---

## 🔗 Project Links

| | Link |
|---|---|
| 🐙 GitHub | [adityapagariya19/Placement_cell_System](https://github.com/adityapagariya19/Placement_cell_System) |
| 📁 Google Drive | [View Project Files](https://drive.google.com/file/d/19HF1fmh10xqGTAe_pMpvJ_0q0JDe949f/view?usp=drivesdk) |

---

## 📄 License

This project is licensed under the **MIT License** — free to use, modify and distribute with attribution.

---

<div align="center">

**⭐ If this project helped you or impressed you — drop a star! It means everything to us. ⭐**

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1e3a5f,50:1a2332,100:0d1117&height=120&section=footer&animation=fadeIn" width="100%"/>

*Built with ❤️ by Team PlaceTrack Pro · 2026*

</div>
