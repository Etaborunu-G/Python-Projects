from __future__ import annotations

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

from PIL import Image, ImageTk

from ui.theme import apply_dark_theme
from ui.animation import GauntletSnapAnimation
from ui.widgets import MultiSelectList

from core.quotes import random_quote
from core.utils import confirm_phrase_ok, normalize_exts
from core.backup import backup_file, backup_folder_files
from core import snap_folder, snap_file


APP_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = APP_DIR / "assets"
GAUNTLET_PATH = ASSETS_DIR / "gauntlet.png"


class ThanosSnapApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Thanos Snap — Perfectly Balanced")
        self.geometry("1040x720")
        self.minsize(980, 680)

        self.style = ttk.Style(self)
        self.colors = apply_dark_theme(self.style)
        self.configure(bg=self.colors["bg"])

        self.quote_var = tk.StringVar(value=random_quote())
        self.status_var = tk.StringVar(value="Awaiting your command…")

        # selections
        self.snap_strength = tk.IntVar(value=50)

        # menu choices (multi)
        self.do_folder_snap = tk.BooleanVar(value=True)
        self.do_doc_lines = tk.BooleanVar(value=False)
        self.do_doc_chars = tk.BooleanVar(value=False)

        # targets
        self.folder_path = tk.StringVar()
        self.file_path = tk.StringVar()

        # backups
        self.backup_enabled = tk.BooleanVar(value=True)
        self.backup_dir = tk.StringVar(value=str((Path.home() / "ThanosSnapBackups").resolve()))

        # confirmation
        self.confirm_phrase = tk.StringVar()

        self._load_gauntlet()
        self._build_ui()

    def _load_gauntlet(self):
        try:
            self.gauntlet_img = Image.open(GAUNTLET_PATH).convert("RGBA")
        except Exception:
            self.gauntlet_img = None

    def _build_ui(self):
        top = ttk.Frame(self)
        top.pack(fill="x", padx=22, pady=(18, 10))

        left = ttk.Frame(top)
        left.pack(side="left", fill="both", expand=True)

        ttk.Label(left, text="Thanos Snap", style="Title.TLabel").pack(anchor="w")
        ttk.Label(left, text="Choose your fate. Perfectly balanced… as all things should be.",
                  style="Muted.TLabel").pack(anchor="w", pady=(6, 0))
        ttk.Label(left, textvariable=self.quote_var, style="Quote.TLabel").pack(anchor="w", pady=(10, 0))

        right = ttk.Frame(top)
        right.pack(side="right")

        self.gauntlet_label = ttk.Label(right)
        self.gauntlet_label.pack()

        if self.gauntlet_img:
            img = self.gauntlet_img.copy()
            h = 150
            ratio = h / img.height
            w = int(img.width * ratio)
            img = img.resize((w, h), Image.LANCZOS)
            self.gauntlet_photo = ImageTk.PhotoImage(img)
            self.gauntlet_label.configure(image=self.gauntlet_photo)
        else:
            self.gauntlet_label.configure(text="(gauntlet.png missing)")

        main = ttk.Frame(self)
        main.pack(fill="both", expand=True, padx=22, pady=(0, 12))

        # Left: Mode menu + global options
        modes = ttk.Frame(main, style="Panel.TFrame")
        modes.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=6)

        # Right: Target pickers + logs
        targets = ttk.Frame(main, style="Panel.TFrame")
        targets.pack(side="right", fill="both", expand=True, padx=(10, 0), pady=6)

        self._build_mode_panel(modes)
        self._build_target_panel(targets)

        bottom = ttk.Frame(self)
        bottom.pack(fill="x", padx=22, pady=(0, 18))
        ttk.Label(bottom, textvariable=self.status_var, style="Muted.TLabel").pack(anchor="w")

    def _build_mode_panel(self, parent):
        wrap = ttk.Frame(parent, style="Panel.TFrame")
        wrap.pack(fill="both", expand=True, padx=16, pady=16)

        ttk.Label(wrap, text="Snap Menu", background=self.colors["panel"], foreground=self.colors["text"],
                  font=("Segoe UI Semibold", 14)).pack(anchor="w")
        ttk.Label(wrap, text="Select one or more snap types. (You can select all.)",
                  background=self.colors["panel"], foreground=self.colors["muted"],
                  font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 12))

        # Snap types
        box = ttk.Frame(wrap, style="Panel.TFrame")
        box.pack(fill="x", pady=(0, 10))

        ttk.Checkbutton(box, text="Folder Snap (delete % of files to Recycle Bin/Trash)",
                        variable=self.do_folder_snap).pack(anchor="w", pady=2)
        ttk.Checkbutton(box, text="Document Snap — Lines (permanent: remove % of lines)",
                        variable=self.do_doc_lines).pack(anchor="w", pady=2)
        ttk.Checkbutton(box, text="Document Snap — Characters (permanent: remove % of characters)",
                        variable=self.do_doc_chars).pack(anchor="w", pady=2)

        btnrow = ttk.Frame(wrap, style="Panel.TFrame")
        btnrow.pack(fill="x", pady=(4, 12))
        ttk.Button(btnrow, text="Select All", command=self._select_all_modes).pack(side="left")
        ttk.Button(btnrow, text="Clear", command=self._clear_modes).pack(side="left", padx=8)
        ttk.Button(btnrow, text="Refresh Quote", command=self._refresh_quote).pack(side="right")

        # Strength slider
        ttk.Label(wrap, text="Snap Strength (%)", background=self.colors["panel"], foreground=self.colors["muted"],
                  font=("Segoe UI", 10)).pack(anchor="w", pady=(8, 4))
        self.str_scale = ttk.Scale(wrap, from_=10, to=90, orient="horizontal",
                                   command=self._on_strength_change)
        self.str_scale.set(self.snap_strength.get())
        self.str_scale.pack(fill="x")

        self.str_label = ttk.Label(wrap, text=f"{self.snap_strength.get()}%",
                                   background=self.colors["panel"], foreground=self.colors["text"],
                                   font=("Segoe UI Semibold", 11))
        self.str_label.pack(anchor="w", pady=(6, 10))

        # Backup options (global)
        ttk.Label(wrap, text="Backup Options", background=self.colors["panel"], foreground=self.colors["text"],
                  font=("Segoe UI Semibold", 12)).pack(anchor="w", pady=(10, 6))

        ttk.Checkbutton(wrap, text="Create backups before snapping (recommended)",
                        variable=self.backup_enabled).pack(anchor="w")

        brow = ttk.Frame(wrap, style="Panel.TFrame")
        brow.pack(fill="x", pady=(8, 0))
        ttk.Entry(brow, textvariable=self.backup_dir).pack(side="left", fill="x", expand=True)
        ttk.Button(brow, text="Choose", command=self._choose_backup_dir).pack(side="left", padx=(10, 0))

        # Confirmation phrase
        ttk.Label(wrap, text='Type "I am inevitable" to enable snapping:',
                  background=self.colors["panel"], foreground=self.colors["muted"],
                  font=("Segoe UI", 10)).pack(anchor="w", pady=(14, 6))
        ttk.Entry(wrap, textvariable=self.confirm_phrase).pack(fill="x")

        # Action buttons
        act = ttk.Frame(wrap, style="Panel.TFrame")
        act.pack(fill="x", pady=(16, 0))
        ttk.Button(act, text="Preview Plan", style="Accent.TButton", command=self.preview).pack(side="left")
        ttk.Button(act, text="SNAP", style="Danger.TButton", command=self.snap).pack(side="right")

    def _build_target_panel(self, parent):
        wrap = ttk.Frame(parent, style="Panel.TFrame")
        wrap.pack(fill="both", expand=True, padx=16, pady=16)

        ttk.Label(wrap, text="Targets", background=self.colors["panel"], foreground=self.colors["text"],
                  font=("Segoe UI Semibold", 14)).pack(anchor="w")
        ttk.Label(wrap, text="Pick the folder/file targets for the snap types you selected.",
                  background=self.colors["panel"], foreground=self.colors["muted"],
                  font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 12))

        # Folder picker
        frow = ttk.Frame(wrap, style="Panel.TFrame")
        frow.pack(fill="x", pady=(0, 10))
        ttk.Label(frow, text="Folder:", background=self.colors["panel"], foreground=self.colors["muted"]).pack(side="left")
        ttk.Entry(frow, textvariable=self.folder_path).pack(side="left", fill="x", expand=True, padx=8)
        ttk.Button(frow, text="Choose", command=self._choose_folder).pack(side="left")

        # Folder file type restriction
        ttk.Label(wrap, text="Folder file types (multi-select):",
                  background=self.colors["panel"], foreground=self.colors["muted"],
                  font=("Segoe UI", 10)).pack(anchor="w")
        self.ext_list = MultiSelectList(wrap, height=6)
        self.ext_list.pack(fill="x", pady=(6, 6))

        # common extensions + "ALL"
        self.ext_items = ["ALL (no filter)", ".txt", ".md", ".pdf", ".docx", ".png", ".jpg", ".jpeg", ".gif",
                          ".mp4", ".mov", ".zip", ".csv", ".json", ".xml", ".py", ".java", ".cpp", ".c", ".h"]
        self.ext_list.set_items(self.ext_items)
        self.ext_list.listbox.select_set(0, 0)  # default ALL

        extbtn = ttk.Frame(wrap, style="Panel.TFrame")
        extbtn.pack(fill="x", pady=(0, 12))
        ttk.Button(extbtn, text="Select All Types", command=self.ext_list.select_all).pack(side="left")
        ttk.Button(extbtn, text="Only ALL", command=self._select_only_all).pack(side="left", padx=8)

        # File picker
        prow = ttk.Frame(wrap, style="Panel.TFrame")
        prow.pack(fill="x", pady=(0, 10))
        ttk.Label(prow, text="Document:", background=self.colors["panel"], foreground=self.colors["muted"]).pack(side="left")
        ttk.Entry(prow, textvariable=self.file_path).pack(side="left", fill="x", expand=True, padx=8)
        ttk.Button(prow, text="Choose", command=self._choose_file).pack(side="left")

        # Progress + log
        self.progress = ttk.Progressbar(wrap, mode="determinate")
        self.progress.pack(fill="x", pady=(10, 10))

        self.log = tk.Text(wrap, height=14, bg=self.colors["panel2"], fg=self.colors["text"],
                           insertbackground=self.colors["text"], relief="flat",
                           highlightthickness=1, highlightbackground="#1f2a38")
        self.log.pack(fill="both", expand=True)

        self._log("Select snap types, targets, and strength. Then preview or SNAP.")

    # ---------------- helpers ----------------

    def _log(self, msg: str):
        from datetime import datetime
        self.log.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        self.log.see("end")

    def _refresh_quote(self):
        self.quote_var.set(random_quote())

    def _on_strength_change(self, _val):
        v = int(float(self.str_scale.get()))
        self.snap_strength.set(v)
        self.str_label.configure(text=f"{v}%")

    def _select_all_modes(self):
        self.do_folder_snap.set(True)
        self.do_doc_lines.set(True)
        self.do_doc_chars.set(True)

    def _clear_modes(self):
        self.do_folder_snap.set(False)
        self.do_doc_lines.set(False)
        self.do_doc_chars.set(False)

    def _select_only_all(self):
        self.ext_list.clear_selection()
        self.ext_list.listbox.select_set(0, 0)

    def _choose_backup_dir(self):
        p = filedialog.askdirectory(title="Choose backup directory")
        if p:
            self.backup_dir.set(p)
            self._log(f"Backup directory set: {p}")

    def _choose_folder(self):
        p = filedialog.askdirectory(title="Choose folder to snap")
        if p:
            self.folder_path.set(p)
            self._log(f"Folder selected: {p}")

    def _choose_file(self):
        p = filedialog.askopenfilename(
            title="Choose a document/text file",
            filetypes=[
                ("Text-like files", "*.txt *.md *.csv *.log *.json *.xml *.yaml *.yml *.py *.java *.cpp *.c *.h *.hpp"),
                ("All files", "*.*")
            ],
        )
        if p:
            self.file_path.set(p)
            self._log(f"Document selected: {p}")

    def _selected_ext_filter(self):
        chosen = self.ext_list.get_selected()
        if not chosen or "ALL (no filter)" in chosen:
            return None
        return normalize_exts(chosen)

    def _validate_selection(self) -> bool:
        if not (self.do_folder_snap.get() or self.do_doc_lines.get() or self.do_doc_chars.get()):
            messagebox.showwarning("No snap type selected", "Select at least one snap type.")
            return False

        if not confirm_phrase_ok(self.confirm_phrase.get()):
            messagebox.showerror("Confirmation required", 'Type "I am inevitable" to enable snapping.')
            return False

        if self.do_folder_snap.get():
            if not self.folder_path.get().strip():
                messagebox.showwarning("Folder required", "Folder Snap selected — choose a folder.")
                return False

        if self.do_doc_lines.get() or self.do_doc_chars.get():
            if not self.file_path.get().strip():
                messagebox.showwarning("Document required", "Document Snap selected — choose a document file.")
                return False

        return True

    # ---------------- Preview / Snap ----------------

    def preview(self):
        if not (self.do_folder_snap.get() or self.do_doc_lines.get() or self.do_doc_chars.get()):
            messagebox.showwarning("No snap type selected", "Select at least one snap type.")
            return

        strength = self.snap_strength.get()
        self._log(f"Previewing snap plan at strength: {strength}%")

        # Folder preview
        if self.do_folder_snap.get():
            folder = Path(self.folder_path.get().strip())
            if folder.exists():
                allowed_exts = self._selected_ext_filter()
                plan = snap_folder.make_plan(folder, strength, allowed_exts)
                self._log(f"[Folder] Candidates: {plan.total} | Would delete: {plan.to_remove} (to Trash)")
                for name in plan.targets_preview:
                    self._log(f"  • {name}")
                if plan.to_remove > len(plan.targets_preview):
                    self._log(f"  …and {plan.to_remove - len(plan.targets_preview)} more.")
            else:
                self._log("[Folder] Invalid folder path for preview.")

        # Document previews
        if self.do_doc_lines.get():
            f = Path(self.file_path.get().strip())
            if f.exists():
                plan = snap_file.make_plan(f, strength, "lines")
                self._log(f"[Doc Lines] Total lines: {plan.total} | Would remove: {plan.to_remove} (permanent edit)")
                for t in plan.targets_preview[:10]:
                    self._log(f"  • {t}")
            else:
                self._log("[Doc Lines] Invalid file path for preview.")

        if self.do_doc_chars.get():
            f = Path(self.file_path.get().strip())
            if f.exists():
                plan = snap_file.make_plan(f, strength, "chars")
                self._log(f"[Doc Chars] Total chars: {plan.total} | Would remove: {plan.to_remove} (permanent edit)")
            else:
                self._log("[Doc Chars] Invalid file path for preview.")

        self.status_var.set("Preview complete. No changes made.")

    def snap(self):
        if not self._validate_selection():
            return

        strength = self.snap_strength.get()

        # Final warning summary
        summary = []
        if self.do_folder_snap.get():
            summary.append("• Folder Snap: delete % of files to Recycle Bin/Trash")
        if self.do_doc_lines.get():
            summary.append("• Document Snap (Lines): permanent edit")
        if self.do_doc_chars.get():
            summary.append("• Document Snap (Chars): permanent edit")

        if not messagebox.askyesno(
            "Final Warning",
            "You are about to SNAP with these actions:\n\n"
            + "\n".join(summary)
            + f"\n\nStrength: {strength}%\n\nProceed?"
        ):
            self._log("Snap canceled.")
            return

        # Play animation then run
        def run_after_anim():
            self._execute_snap()

        if self.gauntlet_img:
            anim = GauntletSnapAnimation(self, self.gauntlet_img, self.colors["bg"])
            anim.play(run_after_anim)
        else:
            run_after_anim()

    def _execute_snap(self):
        strength = self.snap_strength.get()
        backup_dir = Path(self.backup_dir.get().strip() or (Path.home() / "ThanosSnapBackups"))

        self._refresh_quote()
        self.status_var.set("Snapping…")

        # Backup + Folder snap
        if self.do_folder_snap.get():
            folder = Path(self.folder_path.get().strip())
            allowed_exts = self._selected_ext_filter()

            plan = snap_folder.make_plan(folder, strength, allowed_exts)
            self._log(f"[Folder] Plan: {plan.to_remove}/{plan.total} to Trash")

            # backup only the candidates chosen for deletion (safer & smaller)
            if self.backup_enabled.get() and plan.to_remove > 0:
                candidates = snap_folder.list_candidate_files(folder, allowed_exts)
                # choose same set again? better: run execute list internally—so we do a deterministic plan.
                # We'll rebuild the chosen list using the same function path:
                # easiest approach: run a fresh execute AFTER backing up all candidates (less ideal) —
                # Instead, create backup of ALL candidates (safe and simple).
                self._log("[Folder] Creating backup of candidate files (safe mode)…")
                bdir = backup_folder_files(candidates, backup_dir)
                self._log(f"[Folder] Backup created: {bdir}")

            # progress bar
            self.progress["value"] = 0
            self.progress["maximum"] = max(plan.to_remove, 1)

            def prog(i, total):
                self.progress["maximum"] = max(total, 1)
                self.progress["value"] = i
                self.update_idletasks()

            deleted_ok, failed = snap_folder.execute(folder, strength, allowed_exts, progress_cb=prog)
            self._log(f"[Folder] Done. Deleted to Trash: {deleted_ok} | Failed: {failed}")

        # Document snap backups + execution
        doc_path = None
        if self.do_doc_lines.get() or self.do_doc_chars.get():
            doc_path = Path(self.file_path.get().strip())

            if self.backup_enabled.get():
                b = backup_file(doc_path, backup_dir)
                self._log(f"[Doc] Backup created: {b}")

        if self.do_doc_lines.get():
            self.progress["value"] = 0
            self.progress["maximum"] = 1

            def prog(i, total):
                self.progress["maximum"] = max(total, 1)
                self.progress["value"] = i
                self.update_idletasks()

            removed, kept = snap_file.execute(Path(self.file_path.get().strip()), strength, "lines", progress_cb=prog)
            self._log(f"[Doc Lines] Removed: {removed} | Kept: {kept}")

        if self.do_doc_chars.get():
            self.progress["value"] = 0
            self.progress["maximum"] = 1

            def prog2(i, total):
                self.progress["maximum"] = max(total, 1)
                self.progress["value"] = i
                self.update_idletasks()

            removed, kept = snap_file.execute(Path(self.file_path.get().strip()), strength, "chars", progress_cb=prog2)
            self._log(f"[Doc Chars] Removed: {removed} | Kept: {kept}")

        self._refresh_quote()
        self.status_var.set("It is done.")
        messagebox.showinfo("Snap Complete", "Perfectly balanced… as all things should be.")
