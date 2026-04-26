# views/company_view.py
"""Company HR Dashboard — View own drives, see applicants, update status."""

import tkinter as tk
from tkinter import messagebox, ttk
from views.ui_utils import *
from models.user import CompanyHR


class CompanyDashboard:
    SECTIONS = [
        ("📊", "Dashboard"),
        ("📋", "My Drives"),
        ("👥", "Applicants"),
        ("🔔", "Notifications"),
    ]

    def __init__(self, root, user: CompanyHR, on_logout):
        self.root      = root
        self.user      = user
        self.on_logout = on_logout
        self.win       = tk.Toplevel(root)
        self._selected_drive_id = None
        setup_window(self.win, f"PlaceTrack Pro — {user.company_name}", 1150, 760)
        self.win.protocol("WM_DELETE_WINDOW", self._logout)
        self._build_shell()
        self._show_section("Dashboard")

    def _build_shell(self):
        topbar = make_frame(self.win, bg=C["sidebar"])
        topbar.pack(fill="x")
        tk.Frame(topbar, bg=C["accent2"], height=3).pack(fill="x")
        inner_top = make_frame(topbar, bg=C["sidebar"])
        inner_top.pack(fill="x", padx=20, pady=8)
        make_label(inner_top, "🎓 PlaceTrack Pro", style="subtitle",
                   fg=C["white"], bg=C["sidebar"]).pack(side="left")
        make_label(inner_top, "COMPANY HR PORTAL", style="small",
                   fg=C["accent2"], bg=C["sidebar"]).pack(side="left", padx=12)
        make_button(inner_top, "Logout", self._logout, style="danger").pack(side="right", padx=4)
        make_label(inner_top, f"🏢 {self.user.company_name}",
                   fg=C["text_dim"], bg=C["sidebar"]).pack(side="right", padx=12)

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
                            anchor="w", padx=12, pady=12, width=16,
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
            "Dashboard":   self._build_dashboard,
            "My Drives":   self._build_drives,
            "Applicants":  self._build_applicants,
            "Notifications": self._build_notifications,
        }[name]()

    def _build_dashboard(self):
        outer = make_frame(self.content, bg=C["bg"])
        outer.pack(fill="both", expand=True)
        scroll_outer = make_frame(outer, bg=C["bg"])
        scroll_outer.pack(fill="both", expand=True)
        inner, _ = make_scrollable(scroll_outer)

        make_label(inner, f"🏢 {self.user.company_name}", style="title",
                   fg=C["white"]).pack(anchor="w", padx=24, pady=(20, 4))
        make_label(inner, f"HR: {self.user.full_name}  |  {self.user.email}",
                   style="body", fg=C["text_dim"]).pack(anchor="w", padx=24)

        data = self.user.get_dashboard_data()
        drives = data["drives"]
        counts = data["applicant_counts"]

        kpi_frame = make_frame(inner, bg=C["bg"])
        kpi_frame.pack(fill="x", padx=24, pady=16)
        for i in range(3): kpi_frame.columnconfigure(i, weight=1)

        total_applicants = sum(counts.values())
        active_drives    = sum(1 for d in drives if d["status"] in ("Active", "Upcoming"))
        stat_card(kpi_frame, "Total Drives",      len(drives),        C["accent"],  0, 0)
        stat_card(kpi_frame, "Total Applicants",  total_applicants,   C["success"], 0, 1)
        stat_card(kpi_frame, "Active Drives",     active_drives,      C["warning"], 0, 2)

        make_separator(inner).pack(fill="x", padx=24, pady=12)
        make_label(inner, "My Drives Summary", style="heading", fg=C["accent"]).pack(anchor="w", padx=24)

        cols = [("title","Drive",220),("status","Status",100),
                ("ctc","CTC (LPA)",90),("date","Drive Date",110),("apps","Applicants",100)]
        tree = make_treeview(inner, cols, height=12)
        tree.pack(fill="x", padx=24, pady=8)
        for i, d in enumerate(drives):
            tag = "even" if i % 2 else "odd"
            tree.insert("","end",
                        values=(d["job_title"], d["status"],
                                f"₹{d['ctc_lpa']}", str(d["drive_date"] or "—"),
                                counts.get(d["id"], 0)),
                        tags=(tag,))

    def _build_drives(self):
        outer = make_frame(self.content, bg=C["bg"])
        outer.pack(fill="both", expand=True)
        make_label(outer, "📋 My Drives", style="subtitle", fg=C["white"]).pack(anchor="w", padx=20, pady=12)

        data   = self.user.get_dashboard_data()
        drives = data["drives"]
        counts = data["applicant_counts"]

        scroll_outer = make_frame(outer, bg=C["bg"])
        scroll_outer.pack(fill="both", expand=True, padx=20)
        inner, _ = make_scrollable(scroll_outer)

        if not drives:
            make_label(inner, "No drives posted yet.", fg=C["text_dim"]).pack(pady=60)
            return

        for d in drives:
            card = make_card(inner)
            card.pack(fill="x", pady=6)
            hdr = make_frame(card, bg=C["card"])
            hdr.pack(fill="x", padx=16, pady=(12, 4))
            make_label(hdr, d["job_title"], style="heading",
                       fg=C["white"], bg=C["card"]).pack(side="left")
            sc = STATUS_COLORS.get(d["status"], C["text_dim"])
            make_badge(hdr, d["status"], color=sc).pack(side="right")

            sub = make_frame(card, bg=C["card"])
            sub.pack(fill="x", padx=16, pady=(0, 4))
            make_label(sub, f"💰 ₹{d['ctc_lpa']} LPA  |  📍 {d.get('job_location','—')}  |  👥 {counts.get(d['id'],0)} applicants",
                       fg=C["text_dim"], bg=C["card"]).pack(side="left")

            btn_f = make_frame(card, bg=C["card"])
            btn_f.pack(anchor="e", padx=16, pady=8)
            make_button(btn_f, "👥 View Applicants",
                        command=lambda did=d["id"]: self._view_applicants(did),
                        style="outline").pack(side="right")

    def _view_applicants(self, drive_id):
        self._selected_drive_id = drive_id
        self._show_section("Applicants")

    def _build_applicants(self):
        outer = make_frame(self.content, bg=C["bg"])
        outer.pack(fill="both", expand=True)

        toolbar = make_frame(outer, bg=C["bg"])
        toolbar.pack(fill="x", padx=20, pady=12)
        make_label(toolbar, "👥 Applicants", style="subtitle", fg=C["white"]).pack(side="left")

        data   = self.user.get_dashboard_data()
        drives = data["drives"]

        if not drives:
            make_label(outer, "No drives to show applicants for.", fg=C["text_dim"]).pack(pady=60)
            return

        drive_names = [d["job_title"] for d in drives]
        drive_map   = {d["job_title"]: d["id"] for d in drives}

        v_drive = tk.StringVar(value=drives[0]["job_title"] if drives else "")
        if self._selected_drive_id:
            for d in drives:
                if d["id"] == self._selected_drive_id:
                    v_drive.set(d["job_title"])

        make_label(toolbar, "Drive:", fg=C["text_dim"]).pack(side="left", padx=8)
        cb = ttk.Combobox(toolbar, textvariable=v_drive,
                          values=drive_names, state="readonly",
                          width=30, font=FONT["body"])
        cb.pack(side="left")

        frame = make_frame(outer, bg=C["bg"])
        frame.pack(fill="both", expand=True, padx=20)

        cols = [("name","Name",160),("roll","Roll No",80),("branch","Branch",200),
                ("cgpa","CGPA",60),("backlogs","Backlogs",70),
                ("skills","Skills",260),("round","Round",120),("status","Status",90)]
        tree = make_treeview(frame, cols, height=22)
        sb   = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        def load_applicants(*_):
            drive_id   = drive_map.get(v_drive.get())
            if not drive_id: return
            tree.delete(*tree.get_children())
            applicants = self.user.get_applicants(drive_id)
            for i, a in enumerate(applicants):
                tag = "even" if i % 2 else "odd"
                tree.insert("","end",
                            values=(a["full_name"], a["roll_no"], a["branch"],
                                    a["cgpa"], a["active_backlogs"],
                                    (a["skills"] or "—")[:40], a["current_round"], a["status"]),
                            tags=(tag,))

        cb.bind("<<ComboboxSelected>>", load_applicants)
        load_applicants()

    def _build_notifications(self):
        outer = make_frame(self.content, bg=C["bg"])
        outer.pack(fill="both", expand=True)
        make_label(outer, "🔔 Notifications", style="subtitle", fg=C["white"]).pack(anchor="w", padx=20, pady=12)

        notifs = self.user.get_unread_notifications()
        scroll_outer = make_frame(outer, bg=C["bg"])
        scroll_outer.pack(fill="both", expand=True, padx=20)
        inner, _ = make_scrollable(scroll_outer)

        if not notifs:
            make_label(inner, "No new notifications.", fg=C["text_dim"]).pack(pady=40)
            return
        for n in notifs:
            card = make_card(inner)
            card.pack(fill="x", pady=4)
            hdr = make_frame(card, bg=C["card"])
            hdr.pack(fill="x", padx=14, pady=(10,4))
            make_label(hdr, n["title"], style="heading", fg=C["white"], bg=C["card"]).pack(side="left")
            make_label(hdr, str(n["created_at"])[:16], style="small",
                       fg=C["text_dim"], bg=C["card"]).pack(side="right")
            if n["message"]:
                make_label(card, n["message"], style="body",
                           fg=C["text_dim"], bg=C["card"],
                           wraplength=700, justify="left").pack(anchor="w", padx=14, pady=(0,10))

    def _logout(self):
        self.win.destroy()
        self.on_logout()
