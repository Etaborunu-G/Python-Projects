from __future__ import annotations
import tkinter as tk
from tkinter import ttk

class MultiSelectList(ttk.Frame):
    """
    Simple multi-select list built from a Listbox with scrollbar.
    """
    def __init__(self, parent, height=6):
        super().__init__(parent)
        self.listbox = tk.Listbox(self, selectmode="multiple", height=height)
        self.scroll = ttk.Scrollbar(self, orient="vertical", command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=self.scroll.set)

        self.listbox.pack(side="left", fill="both", expand=True)
        self.scroll.pack(side="right", fill="y")

    def set_items(self, items: list[str]):
        self.listbox.delete(0, "end")
        for it in items:
            self.listbox.insert("end", it)

    def select_all(self):
        self.listbox.select_set(0, "end")

    def clear_selection(self):
        self.listbox.select_clear(0, "end")

    def get_selected(self) -> list[str]:
        idxs = self.listbox.curselection()
        return [self.listbox.get(i) for i in idxs]
