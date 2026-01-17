def apply_dark_theme(style):
    bg = "#0b0f14"
    panel = "#101824"
    panel2 = "#0f1722"
    text = "#e6edf3"
    muted = "#a9b6c4"
    accent = "#7c3aed"
    danger = "#ef4444"

    try:
        style.theme_use("clam")
    except Exception:
        pass

    style.configure("TFrame", background=bg)
    style.configure("Panel.TFrame", background=panel)
    style.configure("Panel2.TFrame", background=panel2)
    style.configure("TLabel", background=bg, foreground=text, font=("Segoe UI", 11))
    style.configure("Muted.TLabel", background=bg, foreground=muted, font=("Segoe UI", 10))
    style.configure("Title.TLabel", background=bg, foreground=text, font=("Segoe UI Semibold", 22))
    style.configure("Quote.TLabel", background=bg, foreground=accent, font=("Segoe UI Semibold", 12))

    style.configure("TEntry", fieldbackground=panel2, foreground=text, insertcolor=text)

    style.configure("TButton", font=("Segoe UI Semibold", 10), padding=(12, 10))
    style.map("TButton",
              background=[("active", panel2), ("!active", panel)],
              foreground=[("active", text), ("!active", text)])

    style.configure("Accent.TButton", font=("Segoe UI Semibold", 10), padding=(12, 10))
    style.map("Accent.TButton",
              background=[("active", "#5b21b6"), ("!active", accent)],
              foreground=[("active", "white"), ("!active", "white")])

    style.configure("Danger.TButton", font=("Segoe UI Semibold", 10), padding=(12, 10))
    style.map("Danger.TButton",
              background=[("active", "#b91c1c"), ("!active", danger)],
              foreground=[("active", "white"), ("!active", "white")])

    style.configure("TProgressbar", troughcolor=panel2, background=accent)

    return {
        "bg": bg, "panel": panel, "panel2": panel2,
        "text": text, "muted": muted,
        "accent": accent, "danger": danger,
    }
