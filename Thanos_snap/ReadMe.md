# Thanos Snap (Python Desktop App)

A dark-themed Python desktop application inspired by Marvel’s **Thanos** that randomly “snaps” data in a *perfectly balanced* way. Users can select one or multiple snap modes, choose snap strength, preview the snap plan, and confirm execution by typing **“I am inevitable”**.

Folder snaps safely send files to the **Recycle Bin / Trash**, while document snaps permanently modify file contents (with optional backups).

> ⚠️ **IMPORTANT WARNING**  
> This application can delete or permanently modify your data.  
> Always use **Preview** first and keep **Backups enabled** unless you fully understand the consequences.

---

## Features

- **Dark-themed GUI (Tkinter)** inspired by the Infinity Gauntlet  
- **Infinity Gauntlet snap animation** before execution  
- **Random Thanos quotes** displayed throughout the app  
- **Multi-mode snapping (select one, many, or all):**
  - **Folder Snap** – deletes a percentage of files at random → *Recycle Bin / Trash*
  - **Document Snap (Lines)** – permanently removes a percentage of lines
  - **Document Snap (Characters)** – permanently removes a percentage of characters
- **Snap Strength Slider:** 10% – 90% (default 50%)  
- **File-type filtering for Folder Snap**
- **Preview Mode**
- **Confirmation phrase required:** `I am inevitable`
- **Backup system enabled by default**
- **Unbiased randomness**

---

## Project Structure

```
thanos_snap/
  main.py
  requirements.txt
  assets/
    gauntlet.png
  ui/
    app.py
    theme.py
    animation.py
    widgets.py
  core/
    quotes.py
    utils.py
    backup.py
    snap_folder.py
    snap_file.py
```

---

## Requirements

- Python **3.10+**
- Pillow
- send2trash

Install dependencies:
```
pip install -r requirements.txt
```

---

## Running

```
python main.py
```

---

## Disclaimer

This project is a **fan-made, non-commercial application** inspired by the character **Thanos** from Marvel.

- Not affiliated with Marvel or Disney or any other parties
- Provided for educational purposes only
- The developer assumes no responsibility for data loss

Use at your own risk.
