from __future__ import annotations
import tkinter as tk
from PIL import Image, ImageTk

class GauntletSnapAnimation:
    """
    Lightweight Tkinter animation:
    - quick zoom pulses
    - brief white flash
    """
    def __init__(self, parent: tk.Widget, pil_image: Image.Image, bg: str):
        self.parent = parent
        self.base = pil_image.convert("RGBA")
        self.bg = bg
        self.top: tk.Toplevel | None = None
        self.label: tk.Label | None = None
        self.flash: tk.Frame | None = None
        self.frames: list[ImageTk.PhotoImage] = []

    def _build_frames(self, target_h=220):
        self.frames.clear()
        # zoom sequence
        heights = [target_h, int(target_h*1.06), int(target_h*1.12), int(target_h*1.06), target_h]
        for h in heights:
            ratio = h / self.base.height
            w = int(self.base.width * ratio)
            img = self.base.resize((w, h), Image.LANCZOS)
            self.frames.append(ImageTk.PhotoImage(img))

    def play(self, on_done):
        self.top = tk.Toplevel(self.parent)
        self.top.overrideredirect(True)
        self.top.configure(bg=self.bg)
        self.top.attributes("-topmost", True)

        # center on parent
        self.parent.update_idletasks()
        px = self.parent.winfo_rootx()
        py = self.parent.winfo_rooty()
        pw = self.parent.winfo_width()
        ph = self.parent.winfo_height()

        w, h = 460, 340
        x = px + (pw - w)//2
        y = py + (ph - h)//2
        self.top.geometry(f"{w}x{h}+{x}+{y}")

        self._build_frames(target_h=220)

        self.label = tk.Label(self.top, bg=self.bg)
        self.label.place(relx=0.5, rely=0.5, anchor="center")

        self.flash = tk.Frame(self.top, bg="white")
        self.flash.place_forget()

        def step(i=0):
            if not self.top or not self.label:
                return
            if i < len(self.frames):
                self.label.configure(image=self.frames[i])
                self.top.after(70, lambda: step(i+1))
                return

            # flash
            self.flash.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.top.after(90, self.flash.place_forget)
            self.top.after(220, finish)

        def finish():
            if self.top:
                self.top.destroy()
            on_done()

        step(0)
