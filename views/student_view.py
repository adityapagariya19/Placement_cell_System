# views/student_view.py
"""Student Dashboard — View drives, apply, track applications, check offers."""

import tkinter as tk
from tkinter import messagebox, ttk
from views.ui_utils import *
from models.user import Student


class StudentDashboard:
    SECTIONS = [
        ("🏠", "My Dashboard"),
        ("📋", "Available Drives"),
        ("📝", "My Applications"),
        ("🎁", "Offer Letters"),
        ("🔔", "Notifications"),
        ("👤", "My Profile"),
    ]

    def __init__(self, root, user: Student, on_logout):
        self.root      = root
        self.user      = user
        self.on_logout = on_logout
        self.win       = tk.Toplevel(root)
        setup_window(self.win, f"PlaceTrack Pro — Student: {user.full_name}", 1200, 780)
        self.win.protocol("WM_DELETE_WINDOW", self._logout)
        self._build_shell()
        self._show_section("My Dashboard")

    def _build_shell(self):
        topbar = make_frame(self.win, bg=C["sidebar"])
        topbar.pack(fill="x")
        tk.Frame(topbar, bg=C["success"], height=3).pack(fill="x")
        inner_top = make_frame(topbar, bg=C["sidebar"])
        inner_top.pack(fill="x", padx=20, pady=8)
        make_label(inner_top, "🎓 PlaceTrack Pro", style="subtitle",
                   fg=C["white"], bg=C["sidebar"]).pack(side="left")
        make_label(inner_top, "STUDENT PORTAL", style="small",
                   fg=C["success"], bg=C["sidebar"]).pack(side="left", padx=12)

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

        body = make_frame(self.win, bg=C["bg"])
        body.pack(fill="both", expand=True)

        self.sidebar = make_frame(body, bg=C["sidebar"])
        self.sidebar.pack(side="left", fill="y")
        tk.Frame(self.sidebar, bg=C["border"], width=1).pack(side="right", fill="y")

        self.nav_btns = {}
        for icon, name in self.SECTIONS:
            btn = tk.Button(self.sidebar, text=f"  {icon}  {name}",
                            font=FONT["nav"], bg=C["sidebar"],
                            fg=C["text_dim"], relief="flat",
                            anchor="w", padx=12, pady=12, width=18,
                            cursor="hand2", activebackground=C["selected"],
                            command=lambda n=name: self._show_section(n))
            btn.pack(fill="x")
            self.nav_btns[name] = btn

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
        self._set_active_nav(name)
        self._clear_content()
        {
            "My Dashboard":    self._build_dashboard,
            "Available Drives":self._build_drives,
            "My Applications": self._build_applications,
            "Offer Letters":   self._build_offers,
            "Notifications":   self._build_notifications,
            "My Profile":      self._build_profile,
        }[name]()

    # ── Dashboard ──────────────────────────────────────────────
    def _build_dashboard(self):
        scroll_outer = make_frame(self.content, bg=C["bg"])
        scroll_outer.pack(fill="both", expand=True)
        inner, _ = make_scrollable(scroll_outer)

        # Greeting
        hdr = make_frame(inner, bg=C["bg"])
        hdr.pack(fill="x", padx=24, pady=(20, 8))
        make_label(hdr, f"Welcome back, {self.user.full_name.split()[0]}! 👋",
                   style="title", fg=C["white"]).pack(side="left")
        placed_badge = "✅ PLACED" if self.user.placed else "🔵 ACTIVE"
        placed_col   = C["success"] if self.user.placed else C["accent"]
        make_badge(hdr, placed_badge, color=placed_col).pack(side="right")

        # Profile card
        pcard = make_card(inner)
        pcard.pack(fill="x", padx=24, pady=8)
        pl = make_frame(pcard, bg=C["card"])
        pl.pack(side="left", padx=20, pady=16)
        tk.Label(pl, text="🎓", font=("Segoe UI", 36), bg=C["card"], fg=C["accent"]).pack()
        make_label(pl, self.user.roll_no, style="heading", fg=C["accent"], bg=C["card"]).pack()
        make_label(pl, self.user.branch, style="small", fg=C["text_dim"], bg=C["card"]).pack()

        pr = make_frame(pcard, bg=C["card"])
        pr.pack(side="left", padx=20, pady=16, fill="x", expand=True)
        for label, val in [("CGPA", f"{self.user.cgpa}"), ("Batch", str(self.user.batch_year)),
                            ("Backlogs", str(self.user.active_backlogs)),
                            ("Email", self.user.email)]:
            row = make_frame(pr, bg=C["card"])
            row.pack(anchor="w", pady=2)
            make_label(row, f"{label}:", style="label", fg=C["text_dim"], bg=C["card"]).pack(side="left", padx=(0,8))
            make_label(row, val, style="body", fg=C["text"], bg=C["card"]).pack(side="left")

        data = self.user.get_dashboard_data()

        # KPI mini
        kpi_frame = make_frame(inner, bg=C["bg"])
        kpi_frame.pack(fill="x", padx=24, pady=8)
        for i in range(3): kpi_frame.columnconfigure(i, weight=1)
        stat_card(kpi_frame, "Applications", len(data["applications"]), C["accent"], 0, 0)
        stat_card(kpi_frame, "Eligible Drives", len(data["eligible_drives"]), C["success"], 0, 1)
        stat_card(kpi_frame, "Offers Received", len(data["offers"]), C["gold"], 0, 2)

        # Eligible drives preview
        if data["eligible_drives"]:
            make_separator(inner).pack(fill="x", padx=24, pady=12)
            make_label(inner, "🎯 Drives You're Eligible For",
                       style="heading", fg=C["accent"]).pack(anchor="w", padx=24)
            for d in data["eligible_drives"][:3]:
                self._drive_card(inner, d, compact=True)

        # Recent applications
        if data["applications"]:
            make_separator(inner).pack(fill="x", padx=24, pady=12)
            make_label(inner, "📝 Recent Applications",
                       style="heading", fg=C["white"]).pack(anchor="w", padx=24)
            cols = [("company","Company",180),("role","Role",180),
                    ("round","Current Round",140),("status","Status",100)]
            tree = make_treeview(inner, cols, height=5)
            tree.pack(fill="x", padx=24, pady=8)
            for a in data["applications"][:6]:
                tree.insert("","end",
                            values=(a["company_name"],a["job_title"],
                                    a["current_round"],a["status"]))

    # ── Available Drives ────────────────────────────────────────
    def _build_drives(self):
        outer = make_frame(self.content, bg=C["bg"])
        outer.pack(fill="both", expand=True)

        toolbar = make_frame(outer, bg=C["bg"])
        toolbar.pack(fill="x", padx=20, pady=12)
        make_label(toolbar, "📋 Placement Drives", style="subtitle", fg=C["white"]).pack(side="left")
        make_label(toolbar, "Only drives matching your eligibility are shown",
                   style="small", fg=C["text_dim"]).pack(side="left", padx=12)

        data = self.user.get_dashboard_data()
        drives = data["eligible_drives"]

        scroll_outer = make_frame(outer, bg=C["bg"])
        scroll_outer.pack(fill="both", expand=True, padx=20)
        inner, _ = make_scrollable(scroll_outer)

        if not drives:
            make_label(inner, "No eligible drives at the moment.\nCheck back soon! 🎓",
                       style="heading", fg=C["text_dim"]).pack(pady=60)
            return
        for d in drives:
            self._drive_card(inner, d, compact=False)

    def _drive_card(self, parent, d, compact=False):
        import json
        card = make_card(parent)
        card.pack(fill="x", padx=0 if compact else 0, pady=5)

        # Header
        hdr = make_frame(card, bg=C["card"])
        hdr.pack(fill="x", padx=16, pady=(12, 4))
        make_label(hdr, d["job_title"], style="heading",
                   fg=C["white"], bg=C["card"]).pack(side="left")
        status_col = STATUS_COLORS.get(d["status"], C["text_dim"])
        make_badge(hdr, d["status"], color=status_col).pack(side="right", padx=4)
        make_badge(hdr, d["job_type"], color=C["accent2"]).pack(side="right", padx=4)

        sub = make_frame(card, bg=C["card"])
        sub.pack(fill="x", padx=16, pady=2)
        make_label(sub, f"🏢 {d['company_name']}",
                   fg=C["accent"], bg=C["card"]).pack(side="left")
        make_label(sub, f"  📍 {d.get('city','')} / {d.get('job_location','')}",
                   fg=C["text_dim"], bg=C["card"]).pack(side="left")
        make_label(sub, f"💰 ₹{d['ctc_lpa']} LPA",
                   fg=C["gold"], bg=C["card"]).pack(side="right")

        if not compact:
            info = make_frame(card, bg=C["card"])
            info.pack(fill="x", padx=16, pady=(4, 0))
            rounds = json.loads(d.get("rounds") or "[]")
            make_label(info,
                       f"Min CGPA: {d['min_cgpa']}  |  Rounds: {' → '.join(rounds) if rounds else '—'}  |  Last Apply: {d.get('last_apply_date','—')}",
                       style="small", fg=C["text_dim"], bg=C["card"]).pack(side="left")

        # Apply button
        btn_frame = make_frame(card, bg=C["card"])
        btn_frame.pack(anchor="e", padx=16, pady=8)
        if d.get("already_applied"):
            make_label(btn_frame, "✅ Applied", style="body",
                       fg=C["success"], bg=C["card"]).pack(side="right")
        else:
            make_button(btn_frame, "Apply Now →",
                        command=lambda did=d["id"]: self._apply(did),
                        style="primary").pack(side="right")

    def _apply(self, drive_id):
        ok = self.user.apply_to_drive(drive_id)
        if ok:
            messagebox.showinfo("Applied!", "Your application has been submitted successfully! 🎉")
            self._show_section("Available Drives")
        else:
            messagebox.showwarning("Already Applied", "You have already applied to this drive.")

    # ── My Applications ─────────────────────────────────────────
    def _build_applications(self):
        outer = make_frame(self.content, bg=C["bg"])
        outer.pack(fill="both", expand=True)
        make_label(outer, "📝 My Applications", style="subtitle", fg=C["white"]).pack(anchor="w", padx=20, pady=12)

        data = self.user.get_dashboard_data()
        apps = data["applications"]

        scroll_outer = make_frame(outer, bg=C["bg"])
        scroll_outer.pack(fill="both", expand=True, padx=20)
        inner, _ = make_scrollable(scroll_outer)

        if not apps:
            make_label(inner, "No applications yet. Browse drives and apply! 🚀",
                       style="heading", fg=C["text_dim"]).pack(pady=60)
            return

        for app in apps:
            card = make_card(inner)
            card.pack(fill="x", pady=5)

            hdr = make_frame(card, bg=C["card"])
            hdr.pack(fill="x", padx=16, pady=(12, 4))
            make_label(hdr, app["job_title"], style="heading",
                       fg=C["white"], bg=C["card"]).pack(side="left")
            sc = STATUS_COLORS.get(app["status"], C["text_dim"])
            make_badge(hdr, app["status"], color=sc).pack(side="right")

            sub = make_frame(card, bg=C["card"])
            sub.pack(fill="x", padx=16, pady=(0, 4))
            make_label(sub, f"🏢 {app['company_name']}",
                       fg=C["accent"], bg=C["card"]).pack(side="left")
            make_label(sub, f"  💰 ₹{app['ctc_lpa']} LPA",
                       fg=C["gold"], bg=C["card"]).pack(side="left")

            info = make_frame(card, bg=C["card"])
            info.pack(fill="x", padx=16, pady=(0, 10))
            make_label(info, f"Current Round: {app['current_round']}   |   Applied: {str(app['applied_at'])[:10]}",
                       style="small", fg=C["text_dim"], bg=C["card"]).pack(side="left")
            if app.get("remarks"):
                make_label(info, f"  |  Remarks: {app['remarks'][:60]}",
                           style="small", fg=C["text_dim"], bg=C["card"]).pack(side="left")

    # ── Offer Letters ───────────────────────────────────────────
    def _build_offers(self):
        outer = make_frame(self.content, bg=C["bg"])
        outer.pack(fill="both", expand=True)
        make_label(outer, "🎁 Offer Letters", style="subtitle", fg=C["white"]).pack(anchor="w", padx=20, pady=12)

        data  = self.user.get_dashboard_data()
        offers = data["offers"]

        scroll_outer = make_frame(outer, bg=C["bg"])
        scroll_outer.pack(fill="both", expand=True, padx=20)
        inner, _ = make_scrollable(scroll_outer)

        if not offers:
            make_label(inner, "No offer letters yet. Keep applying! 💪",
                       style="heading", fg=C["text_dim"]).pack(pady=60)
            return

        for o in offers:
            color = C["gold"] if o["offer_type"] == "Dream" else C["success"]
            card  = make_card(inner, bg=C["card"])
            card.config(highlightbackground=color, highlightthickness=2)
            card.pack(fill="x", pady=8)

            hdr = make_frame(card, bg=C["card"])
            hdr.pack(fill="x", padx=16, pady=(14, 6))
            icon = "⭐" if o["offer_type"] == "Dream" else "📄"
            make_label(hdr, f"{icon} {o['company_name']} — {o['job_title']}",
                       style="heading", fg=color, bg=C["card"]).pack(side="left")
            make_badge(hdr, o["offer_type"], color=color).pack(side="right")

            details = make_frame(card, bg=C["card"])
            details.pack(fill="x", padx=16, pady=(0, 14))
            acc_map = {None: "⏳ Pending", 1: "✅ Accepted", 0: "❌ Declined"}
            acc_col = {None: C["warning"], 1: C["success"], 0: C["danger"]}
            accepted = o.get("accepted")
            for txt in [
                f"💰 CTC: ₹{o['ctc_offered']} LPA",
                f"📅 Offer Date: {o.get('offer_date','—')}",
                f"🚀 Joining Date: {o.get('joining_date','—')}",
                f"Status: {acc_map.get(accepted, '—')}",
            ]:
                make_label(details, txt, style="body", fg=C["text"], bg=C["card"]).pack(anchor="w", pady=2)

    # ── Notifications ───────────────────────────────────────────
    def _build_notifications(self):
        outer = make_frame(self.content, bg=C["bg"])
        outer.pack(fill="both", expand=True)
        make_label(outer, "🔔 Notifications", style="subtitle", fg=C["white"]).pack(anchor="w", padx=20, pady=12)
        make_button(outer, "Mark All Read",
                    command=lambda: [self.user.mark_all_notifications_read(),
                                     self._show_section("Notifications")],
                    style="ghost").pack(anchor="e", padx=20)

        notifs = self.user.get_unread_notifications()
        from config.db_config import db
        all_notifs = db.execute_query(
            "SELECT * FROM notifications WHERE user_id=%s ORDER BY created_at DESC",
            (self.user.user_id,), fetch="all") or []

        scroll_outer = make_frame(outer, bg=C["bg"])
        scroll_outer.pack(fill="both", expand=True, padx=20)
        inner, _ = make_scrollable(scroll_outer)

        if not all_notifs:
            make_label(inner, "All caught up! No notifications.", fg=C["text_dim"]).pack(pady=40)
            return
        for n in all_notifs:
            card = make_card(inner, bg=C["selected"] if not n["is_read"] else C["card"])
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

    # ── Profile ─────────────────────────────────────────────────
    def _build_profile(self):
        outer = make_frame(self.content, bg=C["bg"])
        outer.pack(fill="both", expand=True)

        scroll_outer = make_frame(outer, bg=C["bg"])
        scroll_outer.pack(fill="both", expand=True)
        inner, _ = make_scrollable(scroll_outer)

        make_label(inner, "👤 My Profile", style="subtitle", fg=C["white"]).pack(anchor="w", padx=24, pady=16)

        card = make_card(inner)
        card.pack(fill="x", padx=24, pady=8)

        rows = [
            ("Full Name",    self.user.full_name),
            ("Roll Number",  self.user.roll_no),
            ("Branch",       self.user.branch),
            ("Batch Year",   str(self.user.batch_year)),
            ("CGPA",         str(self.user.cgpa)),
            ("Backlogs",     str(self.user.active_backlogs)),
            ("Email",        self.user.email),
        ]
        for label, val in rows:
            row = make_frame(card, bg=C["card"])
            row.pack(fill="x", padx=20, pady=5)
            make_label(row, f"{label}:", style="label",
                       fg=C["text_dim"], bg=C["card"], width=14, anchor="w").pack(side="left")
            make_label(row, val, style="body", fg=C["text"], bg=C["card"]).pack(side="left")

        make_separator(inner).pack(fill="x", padx=24, pady=16)
        make_label(inner, "Edit Profile", style="heading", fg=C["accent"]).pack(anchor="w", padx=24)

        edit_card = make_card(inner)
        edit_card.pack(fill="x", padx=24, pady=8)

        v_skills = tk.StringVar(value=self.user.skills)
        v_phone  = tk.StringVar(value=self.user.phone or "")

        make_label(edit_card, "Skills (comma separated)", style="label",
                   fg=C["text_dim"], bg=C["card"]).pack(anchor="w", padx=20, pady=(12,2))
        make_entry(edit_card, textvariable=v_skills, width=60).pack(padx=20, ipady=7, pady=(0,10))

        make_label(edit_card, "Phone", style="label",
                   fg=C["text_dim"], bg=C["card"]).pack(anchor="w", padx=20, pady=(0,2))
        make_entry(edit_card, textvariable=v_phone, width=30).pack(padx=20, ipady=7, pady=(0,12))

        def save_profile():
            self.user.update_profile(v_skills.get(), v_phone.get())
            messagebox.showinfo("Saved", "Profile updated successfully!")

        make_button(edit_card, "Save Changes", save_profile,
                    style="success").pack(anchor="w", padx=20, pady=(0, 16), ipadx=8, ipady=4)

    def _logout(self):
        self.win.destroy()
        self.on_logout()
