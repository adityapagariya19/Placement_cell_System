# views/login_view.py
"""
Login & Registration window.
Clean, professional dark UI with tabs for login and new student registration.
"""

import tkinter as tk
from tkinter import messagebox, ttk
from views.ui_utils import *


class LoginView:
    def __init__(self, root: tk.Tk, on_login, on_register):
        self.root        = root
        self.on_login    = on_login
        self.on_register = on_register
        self._build()

    def _build(self):
        setup_window(self.root, "PlaceTrack Pro — Login", 880, 580)

        outer = make_frame(self.root, bg=C["bg"])
        outer.pack(fill="both", expand=True)

        # ── Left panel (branding) ───────────────────────────────
        left = make_frame(outer, bg=C["sidebar"])
        left.place(relx=0, rely=0, relwidth=0.45, relheight=1)

        # Decorative top strip
        tk.Frame(left, bg=C["accent"], height=4).pack(fill="x")

        tk.Label(left, text="🎓", font=("Segoe UI", 54),
                 fg=C["accent"], bg=C["sidebar"]).pack(pady=(60, 8))
        tk.Label(left, text="PlaceTrack Pro",
                 font=("Segoe UI", 26, "bold"),
                 fg=C["white"], bg=C["sidebar"]).pack()
        tk.Label(left, text="College Placement Cell",
                 font=FONT["subtitle"],
                 fg=C["accent2"], bg=C["sidebar"]).pack(pady=4)

        make_separator(left).pack(fill="x", padx=40, pady=24)

        features = [
            ("📊", "Analytics Dashboard"),
            ("🏢", "Company Drive Tracking"),
            ("✅", "Eligibility Engine"),
            ("🔔", "Real-time Notifications"),
            ("📄", "Offer Letter Management"),
        ]
        for icon, feat in features:
            row = make_frame(left, bg=C["sidebar"])
            row.pack(fill="x", padx=36, pady=4)
            tk.Label(row, text=icon, font=("Segoe UI", 13),
                     bg=C["sidebar"], fg=C["accent"]).pack(side="left", padx=(0, 8))
            tk.Label(row, text=feat, font=FONT["body"],
                     bg=C["sidebar"], fg=C["text_dim"]).pack(side="left")

        tk.Label(left, text="© 2025 Placement Cell System",
                 font=FONT["small"], fg=C["text_dim"], bg=C["sidebar"]).pack(
                     side="bottom", pady=18)

        # ── Right panel (forms) ─────────────────────────────────
        right = make_frame(outer, bg=C["bg"])
        right.place(relx=0.45, rely=0, relwidth=0.55, relheight=1)

        # Notebook tabs
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Login.TNotebook", background=C["bg"],
                         borderwidth=0, tabmargins=0)
        style.configure("Login.TNotebook.Tab",
                         background=C["sidebar"], foreground=C["text_dim"],
                         font=FONT["nav"], padding=[20, 10], borderwidth=0)
        style.map("Login.TNotebook.Tab",
                  background=[("selected", C["bg"])],
                  foreground=[("selected", C["accent"])])

        nb = ttk.Notebook(right, style="Login.TNotebook")
        nb.pack(fill="both", expand=True, padx=0, pady=0)

        login_tab = make_frame(nb, bg=C["bg"])
        reg_tab   = make_frame(nb, bg=C["bg"])
        nb.add(login_tab, text="  Sign In  ")
        nb.add(reg_tab,   text="  Register  ")

        self._build_login_tab(login_tab)
        self._build_register_tab(reg_tab)

    def _build_login_tab(self, parent):
        wrap = make_frame(parent, bg=C["bg"])
        wrap.place(relx=0.5, rely=0.5, anchor="center")

        make_label(wrap, "Welcome Back 👋", style="subtitle",
                   fg=C["white"]).pack(pady=(0, 4))
        make_label(wrap, "Sign in to your account", style="small",
                   fg=C["text_dim"]).pack(pady=(0, 28))

        # Username
        self._login_user = tk.StringVar()
        self._login_pass = tk.StringVar()

        for label, var, show in [("Username", self._login_user, ""),
                                   ("Password", self._login_pass, "•")]:
            make_label(wrap, label, style="label",
                       fg=C["text_dim"]).pack(anchor="w")
            e = make_entry(wrap, textvariable=var, show=show, width=32)
            e.pack(pady=(4, 14), ipady=8)

        # Role selector
        make_label(wrap, "Login as", style="label",
                   fg=C["text_dim"]).pack(anchor="w")
        self._role_var = tk.StringVar(value="Student")
        role_frame = make_frame(wrap, bg=C["bg"])
        role_frame.pack(pady=(4, 20), anchor="w")
        for r in ["Student", "Admin", "Company HR"]:
            tk.Radiobutton(role_frame, text=r, variable=self._role_var,
                           value=r, bg=C["bg"], fg=C["text"],
                           selectcolor=C["accent"],
                           activebackground=C["bg"], font=FONT["body"],
                           cursor="hand2").pack(side="left", padx=8)

        btn = make_button(wrap, "SIGN IN →", self._do_login, style="primary", width=32)
        btn.pack(pady=4, ipady=4)

        make_label(wrap, "Demo: admin / Admin@123", style="small",
                   fg=C["text_dim"]).pack(pady=(16, 0))
        make_label(wrap, "Student: stu001 / Student@123", style="small",
                   fg=C["text_dim"]).pack()

    def _do_login(self):
        username = self._login_user.get().strip()
        password = self._login_pass.get()
        if not username or not password:
            messagebox.showwarning("Validation", "Please enter username and password.")
            return
        role_map = {
            "Admin": "admin",
            "Student": "student",
            "Company HR": "company"
        }       

        selected_role = self._role_var.get().strip()

        role_map = {
            "Admin": "admin",
            "Student": "student",
            "Company HR": "company"
        }

        role = role_map.get(selected_role)
        # 🔥 DEBUG LINE (ADD HERE)
        print("ROLE DEBUG:", selected_role, "→", role)
        if role is None:
            messagebox.showerror("Error", f"Invalid role selected: {selected_role}")
            return

        result = self.on_login(username, password, role)
        if result is False:
            messagebox.showerror("Login Failed",
                                 "Invalid username or password.\nPlease try again.")

    def _build_register_tab(self, parent):
        canvas = tk.Canvas(parent, bg=C["bg"], highlightthickness=0)
        sb = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        inner = make_frame(canvas, bg=C["bg"])
        canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        wrap = make_frame(inner, bg=C["bg"])
        wrap.pack(padx=40, pady=20)

        make_label(wrap, "Create Student Account", style="subtitle",
                   fg=C["white"]).pack(pady=(0, 4))
        make_label(wrap, "Fill all fields to register", style="small",
                   fg=C["text_dim"]).pack(pady=(0, 16))

        fields = [
            ("Full Name",        "full_name",      "", 28),
            ("Username",         "username",        "", 28),
            ("Password",         "password",        "•", 28),
            ("Email",            "email",           "", 28),
            ("Phone",            "phone",           "", 28),
            ("Roll Number",      "roll_no",         "", 28),
            ("Batch Year (e.g. 2025)", "batch_year","", 28),
            ("CGPA (e.g. 7.80)", "cgpa",            "", 28),
            ("Active Backlogs",  "active_backlogs", "", 28),
            ("Skills (comma separated)", "skills",  "", 28),
        ]
        self._reg_vars = {}
        for label, key, show, w in fields:
            make_label(wrap, label, style="label",
                       fg=C["text_dim"]).pack(anchor="w")
            var = tk.StringVar()
            self._reg_vars[key] = var
            e = make_entry(wrap, textvariable=var, show=show, width=w)
            e.pack(pady=(4, 12), ipady=7)

        make_label(wrap, "Branch", style="label",
                   fg=C["text_dim"]).pack(anchor="w")
        self._branch_var = tk.StringVar(value=BRANCHES[0])
        cb = ttk.Combobox(wrap, textvariable=self._branch_var,
                          values=BRANCHES, font=FONT["body"],
                          state="readonly", width=30)
        cb.pack(pady=(4, 16))

        make_button(wrap, "CREATE ACCOUNT", self._do_register,
                    style="success", width=32).pack(ipady=4)

    def _do_register(self):
        v = {k: var.get().strip() for k, var in self._reg_vars.items()}
        v["branch"] = self._branch_var.get()

        if not all(v[k] for k in ["full_name", "username", "password",
                                    "email", "roll_no", "batch_year", "cgpa"]):
            messagebox.showwarning("Validation", "Please fill all required fields.")
            return
        try:
            float(v["cgpa"])
            int(v["batch_year"])
            int(v["active_backlogs"] or 0)
        except ValueError:
            messagebox.showerror("Validation", "CGPA, Batch Year and Backlogs must be numbers.")
            return

        ok = self.on_register({
            "username":        v["username"],
            "password":        v["password"],
            "full_name":       v["full_name"],
            "email":           v["email"],
            "phone":           v.get("phone", ""),
            "roll_no":         v["roll_no"],
            "branch":          v["branch"],
            "batch_year":      int(v["batch_year"]),
            "cgpa":            float(v["cgpa"]),
            "active_backlogs": int(v.get("active_backlogs") or 0),
            "skills":          v.get("skills", ""),
        })
        if ok:
            messagebox.showinfo("Success", "Account created! You can now sign in.")
        else:
            messagebox.showerror("Error",
                                  "Registration failed.\nUsername, email or roll number may already exist.")
