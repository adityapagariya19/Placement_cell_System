# 🎓 PlaceTrack Pro
## College Placement Cell Management System
### Complete Setup Guide — Windows 10/11

---

## 📌 Project Overview

**PlaceTrack Pro** is a full-featured desktop application for managing college placement activities.
Built with **Python (Tkinter)** using **OOP principles** and **MySQL via XAMPP**.

| Detail | Value |
|--------|-------|
| Language | Python 3.11+ |
| GUI | Tkinter (built-in) |
| Database | MySQL via XAMPP |
| OOP Concepts | Classes, Inheritance, Encapsulation, Polymorphism, Abstraction, Singleton |

---

## 👥 User Roles

| Role | Login Credentials | Access |
|------|------------------|--------|
| Admin (TPO) | `admin` / `Admin@123` | Full system control |
| Student | `stu001` / `Student@123` | Apply to drives, track status |
| Company HR | `tcs_hr` / `Company@123` | Manage drives, view applicants |

> All student accounts: `stu001` to `stu008` with password `Student@123`
> All company HR accounts: `tcs_hr`, `infosys_hr`, `wipro_hr`, `cognizant_hr`, `accenture_hr`, `amazon_hr`, `microsoft_hr` with password `Company@123`

---

## 🛠 STEP-BY-STEP INSTALLATION GUIDE

### ═══ STEP 1: Install Python 3.11+ ═══

1. Open browser → go to: **https://www.python.org/downloads/**
2. Click **"Download Python 3.11.x"** (or latest 3.11/3.12 version)
3. Run the downloaded `.exe` installer
4. ⚠️ **VERY IMPORTANT**: Check ✅ **"Add Python to PATH"** before clicking Install
5. Click **"Install Now"**
6. After install, click **"Close"**

**Verify Python is installed:**
- Press `Win + R`, type `cmd`, press Enter
- In Command Prompt, type:
```
python --version
```
You should see something like: `Python 3.11.8`

If you see `Python 3.x.x` → ✅ Python installed correctly!

---

### ═══ STEP 2: Install XAMPP ═══

1. Open browser → go to: **https://www.apachefriends.org/**
2. Click **"Download XAMPP for Windows"**
3. Run the downloaded installer (`xampp-windows-x64-*.exe`)
4. Click **Next** through all installer screens (default settings are fine)
5. Installation folder will be `C:\xampp` — keep this default
6. Click **Finish** → XAMPP Control Panel will open

---

### ═══ STEP 3: Start XAMPP Services ═══

1. Open **XAMPP Control Panel** (if not open: search "XAMPP" in Start Menu)
2. Find **Apache** row → click **"Start"** button (it will turn green)
3. Find **MySQL** row → click **"Start"** button (it will turn green)

✅ Both Apache and MySQL should show **green** with port numbers.

> ⚠️ If port 80 conflicts: Apache might fail. MySQL (port 3306) is the important one.
> Only MySQL MUST be running. Apache is for phpMyAdmin (web interface).

---

### ═══ STEP 4: Create the Database ═══

**Method A — Using phpMyAdmin (Easiest):**

1. Open browser → go to: **http://localhost/phpmyadmin**
2. Click **"New"** in the left sidebar (to create a new database)
3. Type database name: `placetrack_pro`
4. Collation: select `utf8mb4_unicode_ci`
5. Click **"Create"**
6. You should see `placetrack_pro` appear in the left sidebar
7. Click on `placetrack_pro` in the left sidebar to select it
8. Click the **"Import"** tab at the top
9. Click **"Choose File"** → navigate to `PlaceTrackPro\database\placetrack.sql`
10. Scroll down → click **"Import"** button
11. You should see **"Import has been successfully finished"** ✅

**Method B — Using Command Line:**
```cmd
cd C:\xampp\mysql\bin
mysql.exe -u root -e "CREATE DATABASE placetrack_pro;"
mysql.exe -u root placetrack_pro < "C:\path\to\PlaceTrackPro\database\placetrack.sql"
```

---

### ═══ STEP 5: Extract the Project ═══

1. Extract the `PlaceTrackPro.zip` file to any location
   Example: `C:\Users\YourName\Desktop\PlaceTrackPro`
2. Make sure the folder structure looks like this:
```
PlaceTrackPro\
├── main.py
├── requirements.txt
├── config\
│   ├── __init__.py
│   └── db_config.py
├── models\
│   ├── __init__.py
│   └── user.py
├── views\
│   ├── __init__.py
│   ├── ui_utils.py
│   ├── login_view.py
│   ├── admin_view.py
│   ├── student_view.py
│   └── company_view.py
├── controllers\
│   └── __init__.py
├── database\
│   └── placetrack.sql
└── README.md
```

---

### ═══ STEP 6: Install Python Libraries ═══

1. Press `Win + R` → type `cmd` → press Enter
2. Navigate to your project folder:
```cmd
cd C:\Users\YourName\Desktop\PlaceTrackPro
```
(Replace the path with where you extracted the project)

3. Install all required libraries:
```cmd
pip install -r requirements.txt
```

Wait for installation to complete. You should see "Successfully installed..." messages.

**Libraries installed:**
- `mysql-connector-python` — Connects Python to MySQL
- `matplotlib` — Charts and graphs in Reports section
- `Pillow` — Image processing

> Tkinter is **built into Python**, no need to install it separately.

---

### ═══ STEP 7: Run the Application ═══

1. Make sure XAMPP MySQL is still running (green in XAMPP Control Panel)
2. In Command Prompt (from project folder):
```cmd
python main.py
```

3. The **PlaceTrack Pro Login** window will appear! 🎉

---

## 🚀 FIRST TIME USAGE GUIDE

### Login as Admin (TPO Officer):
- Username: `admin`
- Password: `Admin@123`
- Click **"SIGN IN →"**

### Explore as Student:
- Username: `stu001`
- Password: `Student@123`
- Click **"SIGN IN →"**
- Go to **"Available Drives"** → click **"Apply Now →"**

### Explore as Company HR:
- Username: `tcs_hr`
- Password: `Company@123`
- Click **"SIGN IN →"**
- Go to **"Applicants"** to see who applied

---

## 🗄️ DATABASE STRUCTURE

The database `placetrack_pro` contains these tables:

| Table | Purpose |
|-------|---------|
| `users` | Authentication for all roles |
| `students` | Student academic details |
| `companies` | Company profiles & HR contacts |
| `drives` | Placement drive listings |
| `applications` | Student applications to drives |
| `offer_letters` | Issued offer letters |
| `notifications` | In-app notification system |

---

## 🏗️ OOP CONCEPTS USED

| Concept | Where Used |
|---------|-----------|
| **Classes & Objects** | User, Student, Admin, CompanyHR, DBConfig, LoginView, AdminDashboard etc. |
| **Inheritance** | `Student(User)`, `Admin(User)`, `CompanyHR(User)` |
| **Encapsulation** | Private `_user_id`, `_password`, getter properties, `execute_query()` |
| **Polymorphism** | `get_dashboard_data()` in all 3 User subclasses returns different data |
| **Abstraction** | `User` base class with abstract `get_dashboard_data()` method |
| **Singleton Pattern** | `DBConfig._instance` — only one DB connection ever created |
| **Factory Method** | `AuthManager.login()` returns correct User subclass |

---

## 📁 FILE DESCRIPTIONS

| File | Description |
|------|-------------|
| `main.py` | App entry point, starts login, routes to dashboards |
| `config/db_config.py` | Singleton DB connection manager |
| `models/user.py` | All OOP classes: User, Student, Admin, CompanyHR, AuthManager |
| `views/ui_utils.py` | Shared theme colors, fonts, reusable widget helpers |
| `views/login_view.py` | Login & registration window |
| `views/admin_view.py` | Admin dashboard (Overview, Students, Companies, Drives, Applications, Reports) |
| `views/student_view.py` | Student dashboard (Drives, Apply, Applications, Offers, Profile) |
| `views/company_view.py` | Company HR dashboard (Drives, Applicants) |
| `database/placetrack.sql` | Complete DB schema + real seed data |

---

## ⚠️ TROUBLESHOOTING

### "Cannot connect to MySQL" error:
→ Open XAMPP → Make sure MySQL is running (green)
→ Try clicking Stop then Start again for MySQL

### "No module named 'mysql'" error:
→ Run: `pip install mysql-connector-python`

### Login says "Invalid credentials":
→ Make sure you ran the SQL file (Step 4)
→ Use exact credentials from the table above

### Application opens but shows blank:
→ Resize the window slightly — Tkinter sometimes needs a resize to redraw

### "python is not recognized":
→ Python was not added to PATH during install
→ Reinstall Python and check the "Add to PATH" checkbox

### Charts not showing in Reports:
→ Run: `pip install matplotlib`

---

## 📊 SEED DATA INCLUDED

Real companies with actual HR details format:
- **TCS** — Ravi Menon (Systems Engineer, ₹3.36 LPA)
- **Infosys** — Anita Desai (Specialist Programmer, ₹4.5 LPA)
- **Wipro** — Suresh Kumar (Project Engineer, ₹3.5 LPA)
- **Cognizant** — Pooja Nair (Programmer Analyst, ₹4.0 LPA)
- **Accenture** — Deepak Rao (Associate SE, ₹4.5 LPA)
- **Amazon** — Sneha Pillai (SDE Intern, ₹50K/month)
- **Microsoft** — Arjun Verma (SWE Intern, ₹75K/month)

8 student profiles across branches: CSE, IT, ECE, Mechanical

---

## 📝 PROJECT INFO

**Project Name:** PlaceTrack Pro  
**Version:** 1.0  
**Language:** Python 3.11+  
**Database:** MySQL 5.7+ (XAMPP)  
**Platform:** Windows 10/11  
**Academic Year:** 2024–25  

---

*This project was built for educational purposes demonstrating real-world OOP and database integration.*
