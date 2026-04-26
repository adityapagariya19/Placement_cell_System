# main.py
"""
PlaceTrack Pro — College Placement Cell Management System
Entry point: creates Login window and starts the Tkinter event loop.
"""

import tkinter as tk
from tkinter import messagebox
import sys, os

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(__file__))

from config.db_config import db
from models.user import AuthManager
from views.login_view import LoginView
from views.admin_view import AdminDashboard
from views.student_view import StudentDashboard
from views.company_view import CompanyDashboard


class PlaceTrackApp:
    """
    Root application controller.
    OOP: Orchestrates view switching and holds a reference to the current user.
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()          # hide until login loaded
        self.current_user = None
        self._verify_db()
        self._show_login()
        self.root.mainloop()

    def _verify_db(self):
        """Check DB connection on startup."""
        try:
            db.get_connection()
        except ConnectionError as e:
            messagebox.showerror(
                "Database Connection Failed",
                str(e) + "\n\nPlease start XAMPP → Apache + MySQL, then relaunch."
            )
            sys.exit(1)

    def _show_login(self):
        """Display the login window."""
        LoginView(self.root, on_login=self._handle_login,
                  on_register=self._handle_register)
        self.root.deiconify()

    def _handle_login(self, username: str, password: str, role: str):
        user = AuthManager.login(username, password, role)
        if user is None:
            return False          # LoginView shows error
        self.current_user = user
        self.root.withdraw()
        self._open_dashboard()
        return True

    def _handle_register(self, data: dict):
        ok = AuthManager.register_student(**data)
        return ok

    def _open_dashboard(self):
        """Open the correct dashboard based on user role."""
        role = self.current_user.role
        if role == "admin":
            AdminDashboard(self.root, self.current_user, on_logout=self._on_logout)
        elif role == "student":
            StudentDashboard(self.root, self.current_user, on_logout=self._on_logout)
        elif role == "company":
            CompanyDashboard(self.root, self.current_user, on_logout=self._on_logout)

    def _on_logout(self):
        """Called when any dashboard logs out."""
        self.current_user = None
        self.root.deiconify()
        self._show_login()


if __name__ == "__main__":
    PlaceTrackApp()
