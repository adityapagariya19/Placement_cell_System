# models/user.py
"""
User Model — OOP Concepts: Classes, Encapsulation, Inheritance, Abstraction
"""

import hashlib
from config.db_config import db


def _hash_password(password: str) -> str:
    """SHA-1 hash (matches seed data hashes). For new projects use bcrypt."""
    return hashlib.sha1(password.encode()).hexdigest()


# ══════════════════════════════════════════════════════════════════
#  BASE CLASS  (Abstraction)
# ══════════════════════════════════════════════════════════════════
class User:
    """
    Abstract base class for all system users.
    OOP: Encapsulation (private _password), Abstraction (get_dashboard_data is abstract)
    """

    def __init__(self, user_id: int, username: str, full_name: str,
                 email: str, phone: str, role: str):
        self._user_id   = user_id      # Encapsulation: protected attribute
        self._username  = username
        self._full_name = full_name
        self._email     = email
        self._phone     = phone
        self._role      = role

    # ── Getters (Encapsulation) ─────────────────────────────────
    @property
    def user_id(self):   return self._user_id
    @property
    def username(self):  return self._username
    @property
    def full_name(self): return self._full_name
    @property
    def email(self):     return self._email
    @property
    def phone(self):     return self._phone
    @property
    def role(self):      return self._role

    def get_dashboard_data(self) -> dict:
        """Abstract method — each subclass implements its own dashboard."""
        raise NotImplementedError("Subclasses must implement get_dashboard_data()")

    def get_unread_notifications(self) -> list:
        return db.execute_query(
            "SELECT * FROM notifications WHERE user_id=%s AND is_read=0 ORDER BY created_at DESC",
            (self._user_id,), fetch="all"
        ) or []

    def mark_notification_read(self, notif_id: int):
        db.execute_query("UPDATE notifications SET is_read=1 WHERE id=%s", (notif_id,))

    def mark_all_notifications_read(self):
        db.execute_query("UPDATE notifications SET is_read=1 WHERE user_id=%s", (self._user_id,))

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self._user_id} role={self._role}>"


# ══════════════════════════════════════════════════════════════════
#  ADMIN  (Inherits User)
# ══════════════════════════════════════════════════════════════════
class Admin(User):
    """
    TPO Officer / Admin — full system access.
    OOP: Inheritance from User, Polymorphism (get_dashboard_data overrides base)
    """

    def get_dashboard_data(self) -> dict:
        """Polymorphism: Admin's version of dashboard data."""
        total_students = db.execute_query(
            "SELECT COUNT(*) AS cnt FROM students", fetch="one")["cnt"]

        placed = db.execute_query(
            "SELECT COUNT(*) AS cnt FROM students WHERE placed=1", fetch="one")["cnt"]

        total_companies = db.execute_query(
            "SELECT COUNT(*) AS cnt FROM companies", fetch="one")["cnt"]

        active_drives = db.execute_query(
            "SELECT COUNT(*) AS cnt FROM drives WHERE status IN ('Active','Upcoming')", fetch="one")["cnt"]

        total_applications = db.execute_query(
            "SELECT COUNT(*) AS cnt FROM applications", fetch="one")["cnt"]

        avg_ctc = db.execute_query(
            "SELECT ROUND(AVG(ctc_offered),2) AS avg FROM offer_letters WHERE accepted=1",
            fetch="one")["avg"] or 0

        branch_stats = db.execute_query(
            """SELECT s.branch,
                      COUNT(*) AS total,
                      SUM(s.placed) AS placed
               FROM students s GROUP BY s.branch ORDER BY total DESC""",
            fetch="all") or []

        recent_selections = db.execute_query(
            """SELECT u.full_name, s.branch, c.company_name, d.job_title,
                      ol.ctc_offered, ol.offer_type
               FROM offer_letters ol
               JOIN applications a ON ol.application_id = a.id
               JOIN students s ON a.student_id = s.id
               JOIN users u ON s.user_id = u.id
               JOIN drives d ON a.drive_id = d.id
               JOIN companies c ON d.company_id = c.id
               ORDER BY ol.offer_date DESC LIMIT 10""",
            fetch="all") or []

        top_recruiters = db.execute_query(
            """SELECT c.company_name, COUNT(ol.id) AS offers, MAX(ol.ctc_offered) AS max_ctc
               FROM offer_letters ol
               JOIN applications a ON ol.application_id = a.id
               JOIN drives d ON a.drive_id = d.id
               JOIN companies c ON d.company_id = c.id
               WHERE ol.accepted=1
               GROUP BY c.company_name ORDER BY offers DESC LIMIT 5""",
            fetch="all") or []

        return {
            "total_students":     total_students,
            "placed":             placed,
            "placement_pct":      round(placed / total_students * 100, 1) if total_students else 0,
            "total_companies":    total_companies,
            "active_drives":      active_drives,
            "total_applications": total_applications,
            "avg_ctc":            float(avg_ctc),
            "branch_stats":       branch_stats,
            "recent_selections":  recent_selections,
            "top_recruiters":     top_recruiters,
        }

    # ── CRUD helpers for admin ──────────────────────────────────
    def get_all_students(self) -> list:
        return db.execute_query(
            """SELECT u.full_name, u.email, u.phone,
                      s.id, s.roll_no, s.branch, s.batch_year,
                      s.cgpa, s.active_backlogs, s.skills, s.placed
               FROM students s JOIN users u ON s.user_id=u.id
               ORDER BY s.roll_no""", fetch="all") or []

    def get_all_drives(self) -> list:
        return db.execute_query(
            """SELECT d.*, c.company_name, c.domain, c.city
               FROM drives d JOIN companies c ON d.company_id=c.id
               ORDER BY d.created_at DESC""", fetch="all") or []

    def get_all_applications(self) -> list:
        return db.execute_query(
            """SELECT a.id, a.status, a.current_round, a.applied_at,
                      u.full_name AS student_name, s.roll_no, s.branch,
                      c.company_name, d.job_title, d.ctc_lpa
               FROM applications a
               JOIN students s ON a.student_id=s.id
               JOIN users u ON s.user_id=u.id
               JOIN drives d ON a.drive_id=d.id
               JOIN companies c ON d.company_id=c.id
               ORDER BY a.applied_at DESC""", fetch="all") or []

    def update_application_status(self, app_id: int, status: str, round_name: str, remarks: str):
        db.execute_query(
            "UPDATE applications SET status=%s, current_round=%s, remarks=%s WHERE id=%s",
            (status, round_name, remarks, app_id))
        # Auto-create offer letter if selected
        if status == "Selected":
            drive = db.execute_query(
                "SELECT d.ctc_lpa FROM applications a JOIN drives d ON a.drive_id=d.id WHERE a.id=%s",
                (app_id,), fetch="one")
            existing = db.execute_query(
                "SELECT id FROM offer_letters WHERE application_id=%s", (app_id,), fetch="one")
            if not existing and drive:
                db.execute_query(
                    "INSERT INTO offer_letters (application_id, ctc_offered, offer_type) VALUES (%s,%s,'Regular')",
                    (app_id, drive["ctc_lpa"]))
                # Mark student as placed
                db.execute_query(
                    """UPDATE students SET placed=1 WHERE id=(
                           SELECT student_id FROM applications WHERE id=%s)""",
                    (app_id,))

    def send_notification(self, user_id: int, title: str, message: str):
        db.execute_query(
            "INSERT INTO notifications (user_id, title, message) VALUES (%s,%s,%s)",
            (user_id, title, message))

    def notify_eligible_students(self, drive_id: int) -> int:
        """Bulk-notify all eligible students for a drive."""
        drive = db.execute_query(
            "SELECT d.*, c.company_name FROM drives d JOIN companies c ON d.company_id=c.id WHERE d.id=%s",
            (drive_id,), fetch="one")
        if not drive:
            return 0
        import json
        branches = json.loads(drive["eligible_branches"])
        placeholders = ",".join(["%s"] * len(branches))
        eligible = db.execute_query(
            f"""SELECT u.id FROM students s JOIN users u ON s.user_id=u.id
                WHERE s.batch_year=%s AND s.cgpa>=%s AND s.active_backlogs<=%s
                AND s.branch IN ({placeholders})""",
            (drive["eligible_batch"], drive["min_cgpa"],
             drive["max_backlogs"], *branches), fetch="all") or []
        for row in eligible:
            self.send_notification(
                row["id"],
                f"New Drive: {drive['company_name']} — {drive['job_title']}",
                f"{drive['company_name']} is conducting a {drive['job_type']} drive "
                f"for {drive['job_title']} at {drive['ctc_lpa']} LPA. "
                f"Last date to apply: {drive['last_apply_date']}.")
        return len(eligible)

    def add_company(self, company_name, domain, website, hr_name, hr_email,
                    hr_phone, city, description) -> int:
        return db.execute_query(
            """INSERT INTO companies (company_name,domain,website,hr_name,hr_email,
               hr_phone,city,description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
            (company_name, domain, website, hr_name, hr_email,
             hr_phone, city, description))

    def add_drive(self, company_id, job_title, job_description, ctc_lpa,
                  job_location, job_type, min_cgpa, max_backlogs,
                  eligible_branches, eligible_batch, drive_date,
                  last_apply_date, rounds, status) -> int:
        import json
        branches_json = json.dumps(eligible_branches) if isinstance(eligible_branches, list) else eligible_branches
        rounds_json   = json.dumps(rounds) if isinstance(rounds, list) else rounds
        return db.execute_query(
            """INSERT INTO drives (company_id,job_title,job_description,ctc_lpa,
               job_location,job_type,min_cgpa,max_backlogs,eligible_branches,
               eligible_batch,drive_date,last_apply_date,rounds,status)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (company_id, job_title, job_description, ctc_lpa, job_location,
             job_type, min_cgpa, max_backlogs, branches_json, eligible_batch,
             drive_date, last_apply_date, rounds_json, status))


# ══════════════════════════════════════════════════════════════════
#  STUDENT  (Inherits User)
# ══════════════════════════════════════════════════════════════════
class Student(User):
    """
    Student user — can view drives, apply, check status.
    OOP: Inheritance + Polymorphism
    """

    def __init__(self, user_id, username, full_name, email, phone, role,
                 student_id, roll_no, branch, batch_year, cgpa,
                 active_backlogs, skills, placed):
        super().__init__(user_id, username, full_name, email, phone, role)
        self.student_id      = student_id
        self.roll_no         = roll_no
        self.branch          = branch
        self.batch_year      = batch_year
        self.cgpa            = float(cgpa)
        self.active_backlogs = active_backlogs
        self.skills          = skills or ""
        self.placed          = bool(placed)

    def get_dashboard_data(self) -> dict:
        """Polymorphism: Student's personalised dashboard."""
        my_applications = db.execute_query(
            """SELECT a.id, a.status, a.current_round, a.applied_at, a.remarks,
                      c.company_name, d.job_title, d.ctc_lpa, d.job_type, d.job_location
               FROM applications a
               JOIN drives d ON a.drive_id=d.id
               JOIN companies c ON d.company_id=c.id
               WHERE a.student_id=%s ORDER BY a.applied_at DESC""",
            (self.student_id,), fetch="all") or []

        eligible_drives = self._get_eligible_drives()

        offers = db.execute_query(
            """SELECT ol.*, c.company_name, d.job_title
               FROM offer_letters ol
               JOIN applications a ON ol.application_id=a.id
               JOIN drives d ON a.drive_id=d.id
               JOIN companies c ON d.company_id=c.id
               WHERE a.student_id=%s""",
            (self.student_id,), fetch="all") or []

        return {
            "applications":    my_applications,
            "eligible_drives": eligible_drives,
            "offers":          offers,
        }

    def _get_eligible_drives(self) -> list:
        """Return drives for which this student meets criteria."""
        all_drives = db.execute_query(
            """SELECT d.*, c.company_name, c.city, c.domain
               FROM drives d JOIN companies c ON d.company_id=c.id
               WHERE d.status IN ('Active','Upcoming')
               ORDER BY d.drive_date""", fetch="all") or []
        import json
        eligible = []
        for drive in all_drives:
            branches = json.loads(drive["eligible_branches"] or "[]")
            if (self.branch in branches
                    and self.cgpa >= float(drive["min_cgpa"])
                    and self.active_backlogs <= drive["max_backlogs"]
                    and self.batch_year == drive["eligible_batch"]):
                # Check not already applied
                already = db.execute_query(
                    "SELECT id FROM applications WHERE student_id=%s AND drive_id=%s",
                    (self.student_id, drive["id"]), fetch="one")
                drive["already_applied"] = already is not None
                eligible.append(drive)
        return eligible

    def apply_to_drive(self, drive_id: int) -> bool:
        existing = db.execute_query(
            "SELECT id FROM applications WHERE student_id=%s AND drive_id=%s",
            (self.student_id, drive_id), fetch="one")
        if existing:
            return False
        db.execute_query(
            "INSERT INTO applications (student_id, drive_id) VALUES (%s,%s)",
            (self.student_id, drive_id))
        return True

    def update_profile(self, skills: str, phone: str):
        db.execute_query(
            "UPDATE students SET skills=%s WHERE id=%s", (skills, self.student_id))
        db.execute_query(
            "UPDATE users SET phone=%s WHERE id=%s", (phone, self._user_id))
        self.skills  = skills
        self._phone  = phone


# ══════════════════════════════════════════════════════════════════
#  COMPANY HR  (Inherits User)
# ══════════════════════════════════════════════════════════════════
class CompanyHR(User):
    """
    Company HR user — manages drives and views applicants.
    OOP: Inheritance + Polymorphism
    """

    def __init__(self, user_id, username, full_name, email, phone, role, company_id, company_name):
        super().__init__(user_id, username, full_name, email, phone, role)
        self.company_id   = company_id
        self.company_name = company_name

    def get_dashboard_data(self) -> dict:
        drives = db.execute_query(
            "SELECT * FROM drives WHERE company_id=%s ORDER BY created_at DESC",
            (self.company_id,), fetch="all") or []

        applicant_counts = {}
        for d in drives:
            cnt = db.execute_query(
                "SELECT COUNT(*) AS c FROM applications WHERE drive_id=%s",
                (d["id"],), fetch="one")
            applicant_counts[d["id"]] = cnt["c"] if cnt else 0

        return {"drives": drives, "applicant_counts": applicant_counts}

    def get_applicants(self, drive_id: int) -> list:
        return db.execute_query(
            """SELECT a.id, a.status, a.current_round, a.applied_at,
                      u.full_name, s.roll_no, s.branch, s.cgpa,
                      s.active_backlogs, s.skills
               FROM applications a
               JOIN students s ON a.student_id=s.id
               JOIN users u ON s.user_id=u.id
               WHERE a.drive_id=%s ORDER BY s.cgpa DESC""",
            (drive_id,), fetch="all") or []


# ══════════════════════════════════════════════════════════════════
#  AUTH  (Factory method pattern)
# ══════════════════════════════════════════════════════════════════
class AuthManager:
    """Handles login and registration. Returns the correct User subclass."""

    @staticmethod
    def login(username: str, password: str, role: str):
        """
        Authenticate user and return appropriate User subclass instance.
        Returns None if credentials are wrong.
        """
        hashed = _hash_password(password)
        print("LOGIN DEBUG:", username, hashed, role)
        row = db.execute_query(
    "SELECT * FROM users WHERE username=%s AND password=%s AND role=%s",
    (username, hashed, role),   # 👈 MUST be 3 values
    fetch="one"
)
        if not row:
            return None

        # Update last_login
        db.execute_query(
            "UPDATE users SET last_login=NOW() WHERE id=%s", (row["id"],))

        role = row["role"]

        if role == "admin":
            return Admin(row["id"], row["username"], row["full_name"],
                         row["email"], row["phone"], role)

        elif role == "student":
            s = db.execute_query(
                "SELECT * FROM students WHERE user_id=%s", (row["id"],), fetch="one")
            if s:
                return Student(row["id"], row["username"], row["full_name"],
                               row["email"], row["phone"], role,
                               s["id"], s["roll_no"], s["branch"], s["batch_year"],
                               s["cgpa"], s["active_backlogs"], s["skills"], s["placed"])

        elif role == "company":
            c = db.execute_query(
                "SELECT * FROM companies WHERE user_id=%s", (row["id"],), fetch="one")
            if c:
                return CompanyHR(row["id"], row["username"], row["full_name"],
                                 row["email"], row["phone"], role,
                                 c["id"], c["company_name"])
        return None

    @staticmethod
    def register_student(username, password, full_name, email, phone,
                         roll_no, branch, batch_year, cgpa, active_backlogs, skills) -> bool:
        hashed = _hash_password(password)
        try:
            uid = db.execute_query(
                """INSERT INTO users (username,password,role,full_name,email,phone)
                   VALUES (%s,%s,'student',%s,%s,%s)""",
                (username, hashed, full_name, email, phone))
            db.execute_query(
                """INSERT INTO students (user_id,roll_no,branch,batch_year,cgpa,active_backlogs,skills)
                   VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                (uid, roll_no, branch, batch_year, cgpa, active_backlogs, skills))
            return True
        except Exception:
            return False
