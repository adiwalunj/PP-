
import tkinter as tk
from tkinter import messagebox
import random

SUBJECTS = ["DLM", "Python", "DSA"]
MAX_MARKS = 100

BG = "#0b1020"
CARD = "#151d35"
BLUE = "#38bdf8"
WHITE = "#ffffff"
GREEN = "#4ade80"
PURPLE = "#a78bfa"
YELLOW = "#facc15"
RED = "#fb7185"

def calculate_total(marks):
    return sum(marks)

def calculate_average(marks):
    return sum(marks) / len(marks)

def calculate_percentage(marks):
    return calculate_total(marks) / (len(marks) * MAX_MARKS) * 100

def get_grade(p):
    if p >= 90:
        return "A"
    elif p >= 80:
        return "B"
    elif p >= 70:
        return "C"
    elif p >= 60:
        return "D"
    elif p >= 40:
        return "E"
    return "F"

root = tk.Tk()
root.title("GradeX - Student Dashboard")
root.geometry("850x650")
root.resizable(False, False)
root.configure(bg=BG)

# Animated background
canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
canvas.place(x=0, y=0, width=850, height=650)

particles = []
for _ in range(40):
    x = random.randint(0, 850)
    y = random.randint(0, 650)
    size = random.randint(2, 4)
    item = canvas.create_oval(
        x, y, x + size, y + size,
        fill="#263653", outline=""
    )
    particles.append([item, x, y, size])

def animate_background():
    for particle in particles:
        item, x, y, size = particle
        y += 1
        if y > 650:
            y = 0
            x = random.randint(0, 850)
        particle[1] = x
        particle[2] = y
        canvas.coords(item, x, y, x + size, y + size)
    root.after(40, animate_background)

# Header
tk.Label(
    root, text="GradeX 🎓",
    font=("Arial", 27, "bold"),
    fg=WHITE, bg=BG
).place(x=35, y=20)

tk.Label(
    root, text="STUDENT PERFORMANCE DASHBOARD",
    font=("Arial", 10, "bold"),
    fg=BLUE, bg=BG
).place(x=38, y=65)

# Input card
input_card = tk.Frame(root, bg=CARD)
input_card.place(x=35, y=110, width=350, height=500)

tk.Label(
    input_card, text="Enter Your Marks",
    font=("Arial", 19, "bold"),
    fg=WHITE, bg=CARD
).pack(pady=(25, 5))

tk.Label(
    input_card, text="Marks must be between 0 and 100",
    font=("Arial", 9), fg="#94a3b8", bg=CARD
).pack(pady=(0, 20))

entries = []

for i, subject in enumerate(SUBJECTS):
    row = tk.Frame(input_card, bg="#1d2945")
    row.pack(fill="x", padx=22, pady=9)

    tk.Label(
        row, text=f"0{i+1}",
        font=("Arial", 11, "bold"),
        fg=BLUE, bg="#1d2945"
    ).pack(side="left", padx=14, pady=12)

    tk.Label(
        row, text=subject, width=9, anchor="w",
        font=("Arial", 12, "bold"),
        fg=WHITE, bg="#1d2945"
    ).pack(side="left")

    entry = tk.Entry(
        row, width=7, justify="center",
        font=("Arial", 13, "bold"),
        bg="#0b1222", fg=WHITE,
        insertbackground=WHITE, relief="flat"
    )
    entry.pack(side="right", padx=12, pady=10)
    entries.append(entry)

# Result card
result_card = tk.Frame(root, bg=CARD)
result_card.place(x=410, y=110, width=405, height=500)

tk.Label(
    result_card, text="YOUR PERFORMANCE",
    font=("Arial", 11, "bold"),
    fg=BLUE, bg=CARD
).pack(pady=(22, 4))

tk.Label(
    result_card, text="Overall Result",
    font=("Arial", 20, "bold"),
    fg=WHITE, bg=CARD
).pack()

# Circular percentage meter
circle = tk.Canvas(
    result_card, width=155, height=155,
    bg=CARD, highlightthickness=0
)
circle.pack(pady=5)

circle.create_oval(
    12, 12, 143, 143,
    outline="#263653", width=11
)

arc = circle.create_arc(
    12, 12, 143, 143,
    start=90, extent=0,
    outline=BLUE, width=11, style="arc"
)

percent_text = circle.create_text(
    77, 70, text="0%",
    fill=WHITE, font=("Arial", 24, "bold")
)

circle.create_text(
    77, 100, text="PERCENTAGE",
    fill="#94a3b8", font=("Arial", 8, "bold")
)

grade_label = tk.Label(
    result_card, text="—",
    font=("Arial", 28, "bold"),
    fg=BLUE, bg=CARD
)
grade_label.pack()

status_label = tk.Label(
    result_card, text="Enter marks to begin",
    font=("Arial", 9), fg="#94a3b8", bg=CARD
)
status_label.pack(pady=3)

info = tk.Frame(result_card, bg=CARD)
info.pack(fill="x", padx=35, pady=10)

total_label = tk.Label(
    info, text="Total\n0 / 300",
    font=("Arial", 10, "bold"), fg=WHITE, bg=CARD
)
total_label.pack(side="left", expand=True)

average_label = tk.Label(
    info, text="Average\n0.00",
    font=("Arial", 10, "bold"), fg=WHITE, bg=CARD
)
average_label.pack(side="right", expand=True)

# Subject progress bars
bars = {}

for subject in SUBJECTS:
    row = tk.Frame(result_card, bg=CARD)
    row.pack(fill="x", padx=30, pady=4)

    tk.Label(
        row, text=subject, width=8, anchor="w",
        font=("Arial", 9, "bold"), fg=WHITE, bg=CARD
    ).pack(side="left")

    bar_bg = tk.Frame(row, bg="#263653", height=8)
    bar_bg.pack(side="left", fill="x", expand=True)

    bar = tk.Frame(bar_bg, bg=BLUE, height=8)
    bar.place(x=0, y=0, width=0, height=8)
    bars[subject] = bar

def animate_percentage(target, current=0):
    circle.itemconfig(arc, extent=-(current * 3.6))
    circle.itemconfig(percent_text, text=f"{current}%")

    if current < target:
        root.after(12, lambda: animate_percentage(target, current + 1))

def animate_bar(subject, target, current=0):
    bars[subject].place(x=0, y=0, width=current, height=8)

    if current < target:
        root.after(
            8,
            lambda: animate_bar(
                subject, target, min(current + 5, target)
            )
        )

def calculate_result():
    marks = []

    for subject, entry in zip(SUBJECTS, entries):
        raw = entry.get().strip()

        try:
            value = float(raw)
        except ValueError:
            messagebox.showerror(
                "Invalid Input", f"Enter valid marks for {subject}."
            )
            return

        if not 0 <= value <= MAX_MARKS:
            messagebox.showerror(
                "Invalid Marks", f"{subject} must be between 0 and 100."
            )
            return

        marks.append(value)

    total = calculate_total(marks)
    average = calculate_average(marks)
    percentage = calculate_percentage(marks)
    grade = get_grade(percentage)

    total_label.config(text=f"Total\n{total:g} / 300")
    average_label.config(text=f"Average\n{average:.2f}")
    grade_label.config(text=grade)

    if percentage >= 90:
        color, status = GREEN, "🏆 Outstanding Performance!"
    elif percentage >= 80:
        color, status = BLUE, "🌟 Excellent Work!"
    elif percentage >= 70:
        color, status = PURPLE, "👍 Very Good!"
    elif percentage >= 40:
        color, status = YELLOW, "📚 Keep Practicing!"
    else:
        color, status = RED, "💪 Keep Learning!"

    grade_label.config(fg=color)
    status_label.config(text=status, fg=color)
    circle.itemconfig(arc, outline=color, extent=0)

    for subject in SUBJECTS:
        bars[subject].place(x=0, y=0, width=0, height=8)

    animate_percentage(round(percentage))

    for subject, mark in zip(SUBJECTS, marks):
        animate_bar(subject, int(mark * 2.6))

def clear_all():
    for entry in entries:
        entry.delete(0, tk.END)

    total_label.config(text="Total\n0 / 300")
    average_label.config(text="Average\n0.00")
    grade_label.config(text="—", fg=BLUE)
    status_label.config(text="Enter marks to begin", fg="#94a3b8")
    circle.itemconfig(arc, extent=0, outline=BLUE)
    circle.itemconfig(percent_text, text="0%")

    for subject in SUBJECTS:
        bars[subject].place(x=0, y=0, width=0, height=8)

    entries[0].focus()

# Buttons
tk.Button(
    input_card, text="⚡  CALCULATE RESULT",
    font=("Arial", 11, "bold"),
    bg="#2563eb", fg=WHITE,
    activebackground="#3b82f6", relief="flat",
    cursor="hand2", command=calculate_result
).pack(fill="x", padx=22, pady=(22, 9), ipady=9)

tk.Button(
    input_card, text="↻  CLEAR",
    font=("Arial", 10, "bold"),
    bg="#27344f", fg=WHITE,
    activebackground="#374866", relief="flat",
    cursor="hand2", command=clear_all
).pack(fill="x", padx=22, ipady=6)

root.bind("<Return>", lambda event: calculate_result())
root.bind("<Escape>", lambda event: clear_all())

entries[0].focus()
animate_background()
root.mainloop()
