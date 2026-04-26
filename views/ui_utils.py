# views/ui_utils.py
"""
Shared UI theme, colors, fonts, and reusable widget helpers.
All views import from here to keep the design consistent.
"""

import tkinter as tk
from tkinter import ttk, font as tkfont
import platform

# ── Colour palette ──────────────────────────────────────────────
C = {
    "bg":           "#0D1117",   # page background (deep dark)
    "sidebar":      "#161B22",   # sidebar panel
    "card":         "#1C2230",   # card background
    "card_hover":   "#232D3F",   # card on hover
    "border":       "#30363D",   # subtle border
    "accent":       "#2196F3",   # primary blue
    "accent2":      "#00BCD4",   # teal highlight
    "success":      "#4CAF50",   # green
    "warning":      "#FF9800",   # orange
    "danger":       "#F44336",   # red
    "gold":         "#FFD700",   # gold for top performers
    "text":         "#E6EDF3",   # primary text
    "text_dim":     "#8B949E",   # secondary / muted text
    "white":        "#FFFFFF",
    "selected":     "#1F3A5F",   # sidebar selected item
    "input_bg":     "#0D1117",
    "input_border": "#388E3C",
}

# ── Font definitions ────────────────────────────────────────────
FONT = {
    "title":     ("Segoe UI", 22, "bold"),
    "subtitle":  ("Segoe UI", 14, "bold"),
    "heading":   ("Segoe UI", 12, "bold"),
    "body":      ("Segoe UI", 11),
    "small":     ("Segoe UI", 9),
    "mono":      ("Consolas", 11),
    "big_num":   ("Segoe UI", 32, "bold"),
    "nav":       ("Segoe UI", 11, "bold"),
    "btn":       ("Segoe UI", 11, "bold"),
    "label":     ("Segoe UI", 10),
}

# ── Status colour mapping ───────────────────────────────────────
STATUS_COLORS = {
    "Applied":    C["accent"],
    "Aptitude":   C["warning"],
    "Technical":  C["accent2"],
    "HR":         "#AB47BC",
    "Selected":   C["success"],
    "Rejected":   C["danger"],
    "Waitlisted": C["warning"],
    "Active":     C["success"],
    "Upcoming":   C["accent"],
    "Completed":  C["text_dim"],
    "Cancelled":  C["danger"],
}

BRANCHES = [
    "Computer Science & Engineering",
    "Information Technology",
    "Electronics & Communication",
    "Mechanical Engineering",
    "Civil Engineering",
    "Electrical Engineering",
    "Chemical Engineering",
]

JOB_TYPES  = ["Full-Time", "Internship", "Contract"]
DRIVE_STATUSES = ["Upcoming", "Active", "Completed", "Cancelled"]


# ════════════════════════════════════════════════════════════════
#  ROOT WINDOW SETUP
# ════════════════════════════════════════════════════════════════
def setup_window(win: tk.Toplevel | tk.Tk, title: str,
                 width=1280, height=780, center=True):
    win.title(title)
    win.configure(bg=C["bg"])
    win.resizable(True, True)
    win.minsize(900, 600)
    if center:
        sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
        x = (sw - width) // 2
        y = (sh - height) // 2
        win.geometry(f"{width}x{height}+{x}+{y}")
    else:
        win.geometry(f"{width}x{height}")


# ════════════════════════════════════════════════════════════════
#  REUSABLE WIDGETS
# ════════════════════════════════════════════════════════════════
def make_frame(parent, bg=None, **kwargs) -> tk.Frame:
    return tk.Frame(parent, bg=bg or C["bg"], **kwargs)


def make_card(parent, padx=16, pady=14, bg=None, **kwargs) -> tk.Frame:
    card = tk.Frame(parent, bg=bg or C["card"],
                    highlightbackground=C["border"],
                    highlightthickness=1, **kwargs)
    return card


def make_label(parent, text, style="body", fg=None, bg=None, **kwargs) -> tk.Label:
    return tk.Label(parent, text=text,
                    font=FONT.get(style, FONT["body"]),
                    fg=fg or C["text"],
                    bg=bg or parent.cget("bg"), **kwargs)


def make_button(parent, text, command, style="primary",
                width=None, height=None, **kwargs) -> tk.Button:
    styles = {
        "primary":  (C["accent"],   C["white"],   C["accent2"]),
        "success":  (C["success"],  C["white"],   "#66BB6A"),
        "danger":   (C["danger"],   C["white"],   "#EF5350"),
        "warning":  (C["warning"],  C["bg"],      "#FFB74D"),
        "outline":  (C["card"],     C["accent"],  C["selected"]),
        "ghost":    (C["bg"],       C["text_dim"],C["card"]),
    }
    bg, fg, hov = styles.get(style, styles["primary"])
    btn = tk.Button(parent, text=text, command=command,
                    font=FONT["btn"], bg=bg, fg=fg,
                    activebackground=hov, activeforeground=fg,
                    relief="flat", cursor="hand2",
                    padx=18, pady=8, **kwargs)
    if width: btn.config(width=width)
    return btn


def make_entry(parent, textvariable=None, show=None,
               placeholder="", width=30, **kwargs) -> tk.Entry:
    e = tk.Entry(parent, textvariable=textvariable,
                 font=FONT["body"], bg=C["input_bg"], fg=C["text"],
                 insertbackground=C["text"],
                 relief="flat",
                 highlightbackground=C["border"],
                 highlightthickness=1,
                 highlightcolor=C["accent"],
                 width=width, show=show or "", **kwargs)
    return e


def make_badge(parent, text, color=None) -> tk.Label:
    color = color or C["accent"]
    lbl = tk.Label(parent, text=f"  {text}  ",
                   font=FONT["small"], fg=C["white"], bg=color,
                   padx=4, pady=2, relief="flat")
    return lbl


def make_separator(parent, orient="horizontal", color=None) -> tk.Frame:
    c = color or C["border"]
    if orient == "horizontal":
        return tk.Frame(parent, bg=c, height=1)
    return tk.Frame(parent, bg=c, width=1)


def make_scrollable(parent, bg=None) -> tuple[tk.Frame, tk.Canvas]:
    """Returns (scrollable_inner_frame, canvas)."""
    bg = bg or C["bg"]
    canvas = tk.Canvas(parent, bg=bg, highlightthickness=0, borderwidth=0)
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    inner = tk.Frame(canvas, bg=bg)
    inner_win = canvas.create_window((0, 0), window=inner, anchor="nw")

    def on_configure(e):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(inner_win, width=canvas.winfo_width())

    inner.bind("<Configure>", on_configure)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(inner_win, width=e.width))
    canvas.configure(yscrollcommand=scrollbar.set)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    return inner, canvas


# ── Themed ttk Treeview ─────────────────────────────────────────
def apply_treeview_style(style_name="Custom.Treeview"):
    style = ttk.Style()
    style.theme_use("default")
    style.configure(style_name,
        background=C["card"],
        foreground=C["text"],
        fieldbackground=C["card"],
        rowheight=30,
        font=FONT["body"],
        borderwidth=0,
    )
    style.configure(f"{style_name}.Heading",
        background=C["sidebar"],
        foreground=C["accent"],
        font=FONT["heading"],
        borderwidth=0,
        relief="flat",
    )
    style.map(style_name,
        background=[("selected", C["selected"])],
        foreground=[("selected", C["white"])],
    )
    return style_name


def make_treeview(parent, columns: list[tuple], height=14, style_name="Custom.Treeview") -> ttk.Treeview:
    """
    columns = [(col_id, heading_text, width), ...]
    """
    apply_treeview_style(style_name)
    col_ids = [c[0] for c in columns]
    tree = ttk.Treeview(parent, columns=col_ids, show="headings",
                        height=height, style=style_name,
                        selectmode="browse")
    for col_id, heading, width in columns:
        tree.heading(col_id, text=heading)
        tree.column(col_id, width=width, anchor="w", stretch=False)
    # Alternating row colours
    tree.tag_configure("odd",  background=C["card"])
    tree.tag_configure("even", background=C["bg"])
    return tree


def stat_card(parent, label, value, accent=None, row=0, col=0):
    """Mini KPI card."""
    accent = accent or C["accent"]
    card = make_card(parent)
    card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
    card.configure(width=180)
    tk.Label(card, text=str(value), font=FONT["big_num"],
             fg=accent, bg=C["card"]).pack(pady=(16, 4))
    tk.Label(card, text=label, font=FONT["label"],
             fg=C["text_dim"], bg=C["card"]).pack(pady=(0, 16))
    return card
