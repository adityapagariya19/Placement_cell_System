# views/admin_view.py
"""
Admin (TPO Officer) Dashboard — full control.
Sections: Overview, Students, Companies, Drives, Applications, Reports
"""

import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import json, datetime
from views.ui_utils import *
from models.user import Admin


class AdminDashboard:
    SECTIONS = [
        ("📊", "Overview"),
        ("👨‍🎓", "Students"),
        ("🏢", "Companies"),
        ("📋", "Drives"),
        ("📝", "Applications"),
        ("🔔", "Notifications"),
        ("📈", "Reports"),
    ]

    def __init__(self, root: tk.Tk, user: Admin, on_logout):
        self.root      = root
        self.user      = user
        self.on_logout = on_logout
        self.win       = tk.Toplevel(root)
        self._current  = "Overview"
        setup_window(self.win, "PlaceTrack Pro — Admin Dashboard", 1300, 800)
        self.win.protocol("WM_DELETE_WINDOW", self._logout)
        self._build_shell()
        self._show_section("Overview")

    # ════════════════════════════════════════════════════════════
    #  SHELL  (sidebar + content area)
    # ════════════════════════════════════════════════════════════
    def _build_shell(self):
        # Top bar
        topbar = make_frame(self.win, bg=C["sidebar"])
        topbar.pack(fill="x")
        tk.Frame(topbar, bg=C["accent"], height=3).pack(fill="x")
        inner_top = make_frame(topbar, bg=C["sidebar"])
        inner_top.pack(fill="x", padx=20, pady=8)
        make_label(inner_top, "🎓 PlaceTrack Pro", style="subtitle",
                   fg=C["white"], bg=C["sidebar"]).pack(side="left")
        make_label(inner_top, "ADMIN — TPO PANEL", style="small",
                   fg=C["accent"], bg=C["sidebar"]).pack(side="left", padx=16)

        notif_count = len(self.user.get_unread_notifications())
        notif_lbl = f"🔔 {notif_count}" if notif_count else "🔔"
        tk.Button(inner_top, text=notif_lbl, font=FONT["btn"],
                  bg=C["sidebar"], fg=C["warning"], relief="flat",
                  cursor="hand2", activebackground=C["sidebar"],
                  command=lambda: self._show_section("Notifications")
                  ).pack(side="right", padx=8)
        make_label(inner_top, f"👤 {self.user.full_name}",
                   fg=C["text_dim"], bg=C["sidebar"]).pack(side="right", padx=8)
        make_button(inner_top, "Logout", self._logout,
                    style="danger").pack(side="right", padx=4)

        # Body
        body = make_frame(self.win, bg=C["bg"])
        body.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = make_frame(body, bg=C["sidebar"])
        self.sidebar.pack(side="left", fill="y")
        tk.Frame(self.sidebar, bg=C["border"], width=1).pack(side="right", fill="y")

        self.nav_btns = {}
        for icon, name in self.SECTIONS:
            btn = tk.Button(self.sidebar, text=f"  {icon}  {name}",
                            font=FONT["nav"], bg=C["sidebar"],
                            fg=C["text_dim"], relief="flat",
                            anchor="w", padx=12, pady=12, width=18,
                            cursor="hand2",
                            activebackground=C["selected"],
                            command=lambda n=name: self._show_section(n))
            btn.pack(fill="x")
            self.nav_btns[name] = btn

        # Content
        self.content = make_frame(body, bg=C["bg"])
        self.content.pack(side="left", fill="both", expand=True)

    def _set_active_nav(self, name):
        for n, btn in self.nav_btns.items():
            btn.config(bg=C["selected"] if n == name else C["sidebar"],
                       fg=C["white"] if n == name else C["text_dim"])

    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _show_section(self, name):
        self._current = name
        self._set_active_nav(name)
        self._clear_content()
        {
            "Overview":      self._build_overview,
            "Students":      self._build_students,
            "Companies":     self._build_companies,
            "Drives":        self._build_drives,
            "Applications":  self._build_applications,
            "Notifications": self._build_notifications,
            "Reports":       self._build_reports,
        }[name]()

    # ════════════════════════════════════════════════════════════
    #  OVERVIEW
    # ════════════════════════════════════════════════════════════
    def _build_overview(self):
        scroll_outer = make_frame(self.content, bg=C["bg"])
        scroll_outer.pack(fill="both", expand=True)
        inner, _ = make_scrollable(scroll_outer)

        # Header
        hdr = make_frame(inner, bg=C["bg"])
        hdr.pack(fill="x", padx=24, pady=(20, 8))
        make_label(hdr, "📊 Dashboard Overview", style="title", fg=C["white"]).pack(side="left")
        make_label(hdr, f"AY 2024–25", style="body", fg=C["text_dim"]).pack(side="right")

        data = self.user.get_dashboard_data()

        # KPI cards
        kpi_frame = make_frame(inner, bg=C["bg"])
        kpi_frame.pack(fill="x", padx=24, pady=8)
        for i in range(4): kpi_frame.columnconfigure(i, weight=1)

        kpis = [
            ("Total Students",    data["total_students"],   C["accent"]),
            ("Students Placed",   data["placed"],           C["success"]),
            ("Placement %",       f"{data['placement_pct']}%", C["gold"]),
            ("Active Drives",     data["active_drives"],    C["warning"]),
            ("Total Companies",   data["total_companies"],  C["accent2"]),
            ("Applications",      data["total_applications"], "#AB47BC"),
            ("Avg CTC (LPA)",     f"₹{data['avg_ctc']}",   C["success"]),
        ]
        for i, (label, val, color) in enumerate(kpis):
            stat_card(kpi_frame, label, val, color, row=0, col=i % 4)
            if i == 3:
                kpi_frame2 = make_frame(inner, bg=C["bg"])
                kpi_frame2.pack(fill="x", padx=24, pady=4)
                for j in range(4): kpi_frame2.columnconfigure(j, weight=1)
                kpi_frame = kpi_frame2

        # Branch stats table
        make_separator(inner).pack(fill="x", padx=24, pady=16)
        make_label(inner, "Branch-wise Placement Stats",
                   style="heading", fg=C["accent"]).pack(anchor="w", padx=24)

        cols = [("branch","Branch",280), ("total","Total Students",140),
                ("placed","Placed",100), ("pct","Placement %",120)]
        tree = make_treeview(inner, cols, height=7)
        tree.pack(fill="x", padx=24, pady=8)
        for i, row in enumerate(data["branch_stats"]):
            total = row["total"] or 0
            placed = int(row["placed"] or 0)
            pct = f"{round(placed/total*100,1)}%" if total else "0%"
            tag = "even" if i % 2 else "odd"
            tree.insert("", "end",
                        values=(row["branch"], total, placed, pct), tags=(tag,))

        # Recent selections
        make_separator(inner).pack(fill="x", padx=24, pady=16)
        make_label(inner, "🏆 Recent Selections",
                   style="heading", fg=C["gold"]).pack(anchor="w", padx=24)

        rcols = [("name","Student",160), ("branch","Branch",200),
                 ("company","Company",180), ("role","Role",180),
                 ("ctc","CTC (LPA)",90), ("type","Offer",80)]
        rtree = make_treeview(inner, rcols, height=8)
        rtree.pack(fill="x", padx=24, pady=8)
        for i, s in enumerate(data["recent_selections"]):
            tag = "even" if i % 2 else "odd"
            rtree.insert("", "end",
                         values=(s["full_name"], s["branch"], s["company_name"],
                                 s["job_title"], f"₹{s['ctc_offered']}", s["offer_type"]),
                         tags=(tag,))

    # ════════════════════════════════════════════════════════════
    #  STUDENTS
    # ════════════════════════════════════════════════════════════
    def _build_students(self):
        outer = make_frame(self.content, bg=C["bg"])
        outer.pack(fill="both", expand=True)

        # Toolbar
        toolbar = make_frame(outer, bg=C["bg"])
        toolbar.pack(fill="x", padx=20, pady=12)
        make_label(toolbar, "👨‍🎓 All Students", style="subtitle", fg=C["white"]).pack(side="left")

        self._stu_search = tk.StringVar()
        e = make_entry(toolbar, textvariable=self._stu_search, width=24)
        e.pack(side="right", ipady=6, padx=6)
        make_label(toolbar, "🔍 Search:", fg=C["text_dim"]).pack(side="right")

        # Table
        cols = [
            ("roll","Roll No",90), ("name","Name",160), ("branch","Branch",220),
            ("batch","Batch",60), ("cgpa","CGPA",60), ("backlogs","Backlogs",70),
            ("skills","Skills",260), ("placed","Status",80),
        ]
        frame = make_frame(outer, bg=C["bg"])
        frame.pack(fill="both", expand=True, padx=20)

        self._stu_tree = make_treeview(frame, cols, height=22)
        sb = ttk.Scrollbar(frame, orient="vertical",
                           command=self._stu_tree.yview)
        self._stu_tree.configure(yscrollcommand=sb.set)
        self._stu_tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self._all_students = self.user.get_all_students()
        self._stu_search.trace_add("write", lambda *_: self._filter_students())
        self._filter_students()

    def _filter_students(self):
        q = self._stu_search.get().lower()
        self._stu_tree.delete(*self._stu_tree.get_children())
        for i, s in enumerate(self._all_students):
            if q and q not in (s["full_name"] + s["roll_no"] + s["branch"]).lower():
                continue
            status = "✅ Placed" if s["placed"] else "🔵 Active"
            tag = "even" if i % 2 else "odd"
            self._stu_tree.insert("", "end",
                values=(s["roll_no"], s["full_name"], s["branch"],
                        s["batch_year"], s["cgpa"],
                        s["active_backlogs"], s["skills"] or "—", status),
                tags=(tag,))

    # ════════════════════════════════════════════════════════════
    #  COMPANIES
    # ════════════════════════════════════════════════════════════
    def _build_companies(self):
        outer = make_frame(self.content, bg=C["bg"])
        outer.pack(fill="both", expand=True)

        toolbar = make_frame(outer, bg=C["bg"])
        toolbar.pack(fill="x", padx=20, pady=12)
        make_label(toolbar, "🏢 Companies", style="subtitle", fg=C["white"]).pack(side="left")
        make_button(toolbar, "+ Add Company", self._add_company_dialog,
                    style="primary").pack(side="right")

        from config.db_config import db
        companies = db.execute_query(
            "SELECT * FROM companies ORDER BY company_name", fetch="all") or []

        scroll_outer = make_frame(outer, bg=C["bg"])
        scroll_outer.pack(fill="both", expand=True, padx=20)
        inner, _ = make_scrollable(scroll_outer)

        for c in companies:
            card = make_card(inner)
            card.pack(fill="x", pady=6)
            card.columnconfigure(1, weight=1)

            # Left: icon + name
            left = make_frame(card, bg=C["card"])
            left.pack(side="left", padx=16, pady=12)
            tk.Label(left, text="🏢", font=("Segoe UI", 28),
                     bg=C["card"], fg=C["accent"]).pack()
            make_label(left, c["company_name"], style="heading",
                       fg=C["white"], bg=C["card"]).pack()
            make_badge(left, c["domain"] or "IT").pack(pady=4)

            # Right: details
            right = make_frame(card, bg=C["card"])
            right.pack(side="left", padx=16, pady=12, fill="x", expand=True)
            details = [
                (f"📧 {c['hr_email'] or '—'}",   C["text_dim"]),
                (f"📞 {c['hr_phone'] or '—'}",    C["text_dim"]),
                (f"📍 {c['city'] or '—'}",         C["text_dim"]),
                (f"👤 HR: {c['hr_name'] or '—'}", C["text"]),
            ]
            for txt, col in details:
                make_label(right, txt, style="body",
                           fg=col, bg=C["card"]).pack(anchor="w")
            if c["description"]:
                desc = c["description"][:100] + ("…" if len(c["description"]) > 100 else "")
                make_label(right, desc, style="small",
                           fg=C["text_dim"], bg=C["card"]).pack(anchor="w", pady=(4, 0))

    def _add_company_dialog(self):
        dlg = tk.Toplevel(self.win)
        dlg.title("Add Company")
        dlg.configure(bg=C["bg"])
        dlg.geometry("500x540")
        make_label(dlg, "Add New Company", style="subtitle", fg=C["white"]).pack(pady=16)

        fields_cfg = [
            ("Company Name *", "company_name"),
            ("Domain (e.g. IT Services)", "domain"),
            ("Website URL", "website"),
            ("HR Contact Name *", "hr_name"),
            ("HR Email *", "hr_email"),
            ("HR Phone", "hr_phone"),
            ("City *", "city"),
            ("Description", "description"),
        ]
        vars_ = {}
        for label, key in fields_cfg:
            make_label(dlg, label, style="label", fg=C["text_dim"]).pack(anchor="w", padx=32)
            v = tk.StringVar()
            vars_[key] = v
            e = make_entry(dlg, textvariable=v, width=40)
            e.pack(padx=32, pady=(2, 10), ipady=6)

        def save():
            v = {k: var.get().strip() for k, var in vars_.items()}
            if not all(v[k] for k in ["company_name","hr_name","hr_email","city"]):
                messagebox.showwarning("Validation", "Fill required (*) fields.")
                return
            self.user.add_company(**v)
            messagebox.showinfo("Success", "Company added successfully!")
            dlg.destroy()
            self._show_section("Companies")

        make_button(dlg, "Save Company", save, style="success").pack(pady=8, ipadx=8, ipady=4)

    # ════════════════════════════════════════════════════════════
    #  DRIVES
    # ════════════════════════════════════════════════════════════
    def _build_drives(self):
        outer = make_frame(self.content, bg=C["bg"])
        outer.pack(fill="both", expand=True)

        toolbar = make_frame(outer, bg=C["bg"])
        toolbar.pack(fill="x", padx=20, pady=12)
        make_label(toolbar, "📋 Placement Drives", style="subtitle", fg=C["white"]).pack(side="left")
        make_button(toolbar, "+ New Drive", self._add_drive_dialog, style="primary").pack(side="right")

        drives = self.user.get_all_drives()
        scroll_outer = make_frame(outer, bg=C["bg"])
        scroll_outer.pack(fill="both", expand=True, padx=20)
        inner, _ = make_scrollable(scroll_outer)

        for d in drives:
            card = make_card(inner)
            card.pack(fill="x", pady=6)

            # Header row
            hdr_row = make_frame(card, bg=C["card"])
            hdr_row.pack(fill="x", padx=16, pady=(12, 4))
            make_label(hdr_row, d["job_title"], style="heading",
                       fg=C["white"], bg=C["card"]).pack(side="left")
            status_color = STATUS_COLORS.get(d["status"], C["text_dim"])
            make_badge(hdr_row, d["status"], color=status_color).pack(side="right", padx=4)
            make_badge(hdr_row, d["job_type"], color=C["accent2"]).pack(side="right", padx=4)

            # Company + CTC
            sub = make_frame(card, bg=C["card"])
            sub.pack(fill="x", padx=16, pady=2)
            make_label(sub, f"🏢 {d['company_name']}",
                       fg=C["accent"], bg=C["card"]).pack(side="left")
            make_label(sub, f"  📍 {d['city']}",
                       fg=C["text_dim"], bg=C["card"]).pack(side="left")
            make_label(sub, f"💰 ₹{d['ctc_lpa']} LPA",
                       fg=C["gold"], bg=C["card"]).pack(side="right")

            # Eligibility
            info = make_frame(card, bg=C["card"])
            info.pack(fill="x", padx=16, pady=(4, 8))
            make_label(info,
                       f"Min CGPA: {d['min_cgpa']}  |  Max Backlogs: {d['max_backlogs']}  |  Batch: {d['eligible_batch']}  |  Drive Date: {d['drive_date'] or '—'}",
                       style="small", fg=C["text_dim"], bg=C["card"]).pack(side="left")

            # Notify button
            notify_btn = make_button(card, "🔔 Notify Eligible",
                command=lambda did=d["id"]: self._notify_students(did),
                style="outline")
            notify_btn.pack(side="right", padx=12, pady=8)

    def _notify_students(self, drive_id):
        count = self.user.notify_eligible_students(drive_id)
        messagebox.showinfo("Notification Sent",
                            f"Notified {count} eligible student(s) about this drive.")

    def _add_drive_dialog(self):
        from config.db_config import db
        companies = db.execute_query(
            "SELECT id, company_name FROM companies ORDER BY company_name", fetch="all") or []
        if not companies:
            messagebox.showwarning("No Companies", "Add at least one company first.")
            return

        dlg = tk.Toplevel(self.win)
        dlg.title("New Placement Drive")
        dlg.configure(bg=C["bg"])
        dlg.geometry("560x780")

        canvas = tk.Canvas(dlg, bg=C["bg"], highlightthickness=0)
        sb = ttk.Scrollbar(dlg, orient="vertical", command=canvas.yview)
        wrap = make_frame(canvas, bg=C["bg"])
        canvas.create_window((0,0), window=wrap, anchor="nw")
        wrap.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        make_label(wrap, "New Placement Drive", style="subtitle", fg=C["white"]).pack(pady=16, padx=24)

        company_names = [c["company_name"] for c in companies]
        company_map   = {c["company_name"]: c["id"] for c in companies}
        v_company = tk.StringVar(value=company_names[0])

        simple_fields = [
            ("Company *", None, "combobox", company_names),
            ("Job Title *", "job_title", "entry", None),
            ("Job Description", "job_desc", "entry", None),
            ("CTC (LPA) *", "ctc_lpa", "entry", None),
            ("Job Location *", "job_location", "entry", None),
            ("Job Type", "job_type", "combobox", JOB_TYPES),
            ("Min CGPA *", "min_cgpa", "entry", None),
            ("Max Backlogs", "max_backlogs", "entry", None),
            ("Eligible Batch Year *", "eligible_batch", "entry", None),
            ("Drive Date (YYYY-MM-DD)", "drive_date", "entry", None),
            ("Last Apply Date (YYYY-MM-DD)", "last_apply_date", "entry", None),
            ("Rounds (comma separated)", "rounds", "entry", None),
            ("Status", "status", "combobox", DRIVE_STATUSES),
        ]
        vars_ = {}
        for label, key, wtype, opts in simple_fields:
            make_label(wrap, label, style="label", fg=C["text_dim"]).pack(anchor="w", padx=28, pady=(6,0))
            v = tk.StringVar(value=(opts[0] if opts else ""))
            if key: vars_[key] = v
            if wtype == "combobox":
                if key is None: v = v_company  # company selector
                cb = ttk.Combobox(wrap, textvariable=v, values=opts,
                                  state="readonly", width=38, font=FONT["body"])
                cb.pack(padx=28, pady=(2, 0))
            else:
                e = make_entry(wrap, textvariable=v, width=40)
                e.pack(padx=28, pady=(2, 0), ipady=6)

        # Branch checkboxes
        make_label(wrap, "Eligible Branches *", style="label", fg=C["text_dim"]).pack(anchor="w", padx=28, pady=(10,0))
        branch_vars = {}
        for b in BRANCHES:
            bv = tk.BooleanVar(value=(b in ["Computer Science & Engineering", "Information Technology"]))
            branch_vars[b] = bv
            tk.Checkbutton(wrap, text=b, variable=bv,
                           bg=C["bg"], fg=C["text"],
                           selectcolor=C["accent"],
                           activebackground=C["bg"],
                           font=FONT["body"], cursor="hand2").pack(anchor="w", padx=36)

        def save():
            company_name = v_company.get()
            company_id   = company_map.get(company_name)
            branches     = [b for b, bv in branch_vars.items() if bv.get()]
            if not company_id or not vars_["job_title"].get().strip() or not branches:
                messagebox.showwarning("Validation", "Fill required (*) fields & select at least one branch.")
                return
            rounds_raw = vars_["rounds"].get().strip()
            rounds_list = [r.strip() for r in rounds_raw.split(",") if r.strip()]
            try:
                self.user.add_drive(
                    company_id   = company_id,
                    job_title    = vars_["job_title"].get().strip(),
                    job_description = vars_["job_desc"].get().strip(),
                    ctc_lpa      = float(vars_["ctc_lpa"].get()),
                    job_location = vars_["job_location"].get().strip(),
                    job_type     = vars_["job_type"].get(),
                    min_cgpa     = float(vars_["min_cgpa"].get() or 6.0),
                    max_backlogs = int(vars_["max_backlogs"].get() or 0),
                    eligible_branches = branches,
                    eligible_batch = int(vars_["eligible_batch"].get()),
                    drive_date   = vars_["drive_date"].get() or None,
                    last_apply_date = vars_["last_apply_date"].get() or None,
                    rounds       = rounds_list,
                    status       = vars_["status"].get(),
                )
                messagebox.showinfo("Success", "Drive added successfully!")
                dlg.destroy()
                self._show_section("Drives")
            except Exception as ex:
                messagebox.showerror("Error", str(ex))

        make_button(wrap, "Save Drive", save, style="success").pack(pady=14, ipadx=8, ipady=4)

    # ════════════════════════════════════════════════════════════
    #  APPLICATIONS
    # ════════════════════════════════════════════════════════════
    def _build_applications(self):
        outer = make_frame(self.content, bg=C["bg"])
        outer.pack(fill="both", expand=True)

        toolbar = make_frame(outer, bg=C["bg"])
        toolbar.pack(fill="x", padx=20, pady=12)
        make_label(toolbar, "📝 Applications", style="subtitle", fg=C["white"]).pack(side="left")
        make_label(toolbar, "(Double-click to update status)",
                   style="small", fg=C["text_dim"]).pack(side="left", padx=12)

        self._app_filter = tk.StringVar(value="All")
        for status in ["All", "Applied", "Aptitude", "Technical", "HR", "Selected", "Rejected"]:
            color = STATUS_COLORS.get(status, C["text_dim"])
            tk.Radiobutton(toolbar, text=status, variable=self._app_filter,
                           value=status, command=self._filter_apps,
                           bg=C["bg"], fg=color, selectcolor=C["card"],
                           activebackground=C["bg"],
                           font=FONT["small"], cursor="hand2").pack(side="right", padx=2)

        frame = make_frame(outer, bg=C["bg"])
        frame.pack(fill="both", expand=True, padx=20)

        cols = [
            ("name","Student",150), ("roll","Roll No",80), ("branch","Branch",200),
            ("company","Company",160), ("role","Role",160),
            ("ctc","CTC (LPA)",80), ("round","Current Round",120), ("status","Status",90),
        ]
        self._app_tree = make_treeview(frame, cols, height=24)
        sb = ttk.Scrollbar(frame, orient="vertical", command=self._app_tree.yview)
        self._app_tree.configure(yscrollcommand=sb.set)
        self._app_tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        self._app_tree.bind("<Double-1>", self._on_app_double_click)

        self._all_apps = self.user.get_all_applications()
        self._filter_apps()

    def _filter_apps(self):
        q = self._app_filter.get()
        self._app_tree.delete(*self._app_tree.get_children())
        for i, a in enumerate(self._all_apps):
            if q != "All" and a["status"] != q:
                continue
            tag = "even" if i % 2 else "odd"
            self._app_tree.insert("", "end",
                values=(a["student_name"], a["roll_no"], a["branch"],
                        a["company_name"], a["job_title"],
                        f"₹{a['ctc_lpa']}", a["current_round"], a["status"]),
                tags=(tag,), iid=str(a["id"]))

    def _on_app_double_click(self, event):
        sel = self._app_tree.selection()
        if not sel: return
        app_id = int(sel[0])
        app = next((a for a in self._all_apps if a["id"] == app_id), None)
        if not app: return
        self._update_status_dialog(app)

    def _update_status_dialog(self, app):
        dlg = tk.Toplevel(self.win)
        dlg.title("Update Application Status")
        dlg.configure(bg=C["bg"])
        dlg.geometry("420x380")

        make_label(dlg, f"Updating: {app['student_name']}", style="heading", fg=C["white"]).pack(pady=16)
        make_label(dlg, f"{app['company_name']} — {app['job_title']}", fg=C["accent"]).pack()

        make_label(dlg, "New Status:", style="label", fg=C["text_dim"]).pack(pady=(16,2), anchor="w", padx=32)
        v_status = tk.StringVar(value=app["status"])
        cb = ttk.Combobox(dlg, textvariable=v_status,
                          values=["Applied","Aptitude","Technical","HR","Selected","Rejected","Waitlisted"],
                          state="readonly", width=32, font=FONT["body"])
        cb.pack(padx=32)

        make_label(dlg, "Current Round:", style="label", fg=C["text_dim"]).pack(pady=(12,2), anchor="w", padx=32)
        v_round = tk.StringVar(value=app["current_round"])
        e_round = make_entry(dlg, textvariable=v_round, width=34)
        e_round.pack(padx=32, ipady=6)

        make_label(dlg, "Remarks:", style="label", fg=C["text_dim"]).pack(pady=(12,2), anchor="w", padx=32)
        txt_remarks = tk.Text(dlg, height=3, width=36,
                              bg=C["card"], fg=C["text"],
                              font=FONT["body"], relief="flat",
                              insertbackground=C["text"])
        txt_remarks.pack(padx=32)

        def save():
            self.user.update_application_status(
                app["id"], v_status.get(), v_round.get(), txt_remarks.get("1.0","end-1c"))
            self._all_apps = self.user.get_all_applications()
            self._filter_apps()
            messagebox.showinfo("Updated", "Application status updated!")
            dlg.destroy()

        make_button(dlg, "Update Status", save, style="success").pack(pady=14, ipadx=8, ipady=4)

    # ════════════════════════════════════════════════════════════
    #  NOTIFICATIONS
    # ════════════════════════════════════════════════════════════
    def _build_notifications(self):
        outer = make_frame(self.content, bg=C["bg"])
        outer.pack(fill="both", expand=True)
        make_label(outer, "🔔 Notifications", style="subtitle", fg=C["white"]).pack(anchor="w", padx=20, pady=12)
        make_button(outer, "Mark All Read",
                    command=lambda: [self.user.mark_all_notifications_read(),
                                     self._show_section("Notifications")],
                    style="ghost").pack(anchor="e", padx=20)

        from config.db_config import db
        notifs = db.execute_query(
            "SELECT * FROM notifications ORDER BY created_at DESC LIMIT 50", fetch="all") or []

        scroll_outer = make_frame(outer, bg=C["bg"])
        scroll_outer.pack(fill="both", expand=True, padx=20)
        inner, _ = make_scrollable(scroll_outer)

        if not notifs:
            make_label(inner, "No notifications.", fg=C["text_dim"]).pack(pady=40)
            return
        for n in notifs:
            card = make_card(inner, bg=C["card"] if n["is_read"] else C["selected"])
            card.pack(fill="x", pady=4)
            hdr = make_frame(card, bg=card.cget("bg"))
            hdr.pack(fill="x", padx=14, pady=(10, 4))
            make_label(hdr, n["title"], style="heading",
                       fg=C["white"] if not n["is_read"] else C["text"],
                       bg=card.cget("bg")).pack(side="left")
            make_label(hdr, str(n["created_at"])[:16], style="small",
                       fg=C["text_dim"], bg=card.cget("bg")).pack(side="right")
            if n["message"]:
                make_label(card, n["message"], style="body",
                           fg=C["text_dim"], bg=card.cget("bg"),
                           wraplength=800, justify="left").pack(anchor="w", padx=14, pady=(0, 10))

    # ════════════════════════════════════════════════════════════
    #  REPORTS
    # ════════════════════════════════════════════════════════════
    def _build_reports(self):
        outer = make_frame(self.content, bg=C["bg"])
        outer.pack(fill="both", expand=True)
        make_label(outer, "📈 Placement Reports", style="subtitle", fg=C["white"]).pack(anchor="w", padx=20, pady=12)

        try:
            import matplotlib
            matplotlib.use("TkAgg")
            from matplotlib.figure import Figure
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            import matplotlib.pyplot as plt

            data = self.user.get_dashboard_data()
            fig = Figure(figsize=(13, 9), facecolor=C["bg"])
            fig.subplots_adjust(hspace=0.45, wspace=0.35)

            # Chart 1 — Placement %
            ax1 = fig.add_subplot(2, 2, 1)
            branches = [b["branch"].split("&")[0].strip()[:18] for b in data["branch_stats"]]
            pcts     = [round(int(b["placed"] or 0) / (b["total"] or 1) * 100, 1)
                        for b in data["branch_stats"]]
            bars = ax1.bar(branches, pcts, color=[C["accent"], C["success"],
                                                   C["warning"], C["accent2"],
                                                   "#AB47BC", C["danger"]][:len(branches)])
            ax1.set_facecolor(C["card"])
            ax1.set_title("Branch-wise Placement %", color=C["text"], fontsize=10)
            ax1.tick_params(colors=C["text_dim"], labelsize=7)
            ax1.set_ylabel("Placement %", color=C["text_dim"])
            for bar, pct in zip(bars, pcts):
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                         f"{pct}%", ha="center", color=C["text"], fontsize=7)

            # Chart 2 — Top Recruiters
            ax2 = fig.add_subplot(2, 2, 2)
            if data["top_recruiters"]:
                names  = [r["company_name"][:12] for r in data["top_recruiters"]]
                offers = [r["offers"] for r in data["top_recruiters"]]
                colors_pie = [C["accent"], C["success"], C["warning"], C["accent2"], "#AB47BC"]
                wedges, texts, autotexts = ax2.pie(
                    offers, labels=names, autopct="%1.0f%%",
                    colors=colors_pie[:len(names)], startangle=90,
                    textprops={"color": C["text"], "fontsize": 7})
                for at in autotexts: at.set_color(C["bg"])
            ax2.set_facecolor(C["card"])
            ax2.set_title("Top Recruiters (by offers)", color=C["text"], fontsize=10)

            # Chart 3 — CTC distribution bar
            ax3 = fig.add_subplot(2, 2, 3)
            from config.db_config import db
            ctc_data = db.execute_query(
                """SELECT c.company_name, MAX(ol.ctc_offered) AS max_ctc
                   FROM offer_letters ol
                   JOIN applications a ON ol.application_id=a.id
                   JOIN drives d ON a.drive_id=d.id
                   JOIN companies c ON d.company_id=c.id
                   GROUP BY c.company_name ORDER BY max_ctc DESC""",
                fetch="all") or []
            if ctc_data:
                cn = [r["company_name"][:10] for r in ctc_data]
                cv = [float(r["max_ctc"]) for r in ctc_data]
                ax3.barh(cn, cv, color=C["gold"])
                ax3.set_facecolor(C["card"])
                ax3.set_title("Max CTC per Company (LPA)", color=C["text"], fontsize=10)
                ax3.tick_params(colors=C["text_dim"], labelsize=8)
                ax3.set_xlabel("LPA", color=C["text_dim"])

            # Chart 4 — Overall donut
            ax4 = fig.add_subplot(2, 2, 4)
            placed   = data["placed"]
            unplaced = data["total_students"] - placed
            wedges, texts, autos = ax4.pie(
                [placed, unplaced], labels=["Placed", "Unplaced"],
                autopct="%1.1f%%",
                colors=[C["success"], C["border"]],
                startangle=90, wedgeprops={"width": 0.5},
                textprops={"color": C["text"], "fontsize": 9})
            for at in autos: at.set_color(C["bg"])
            ax4.set_title("Overall Placement Status", color=C["text"], fontsize=10)

            canvas = FigureCanvasTkAgg(fig, master=outer)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=8)

        except ImportError:
            make_label(outer,
                       "📊 Install matplotlib to see charts:\n\npip install matplotlib",
                       style="heading", fg=C["text_dim"]).pack(pady=80)

    def _logout(self):
        self.win.destroy()
        self.on_logout()
