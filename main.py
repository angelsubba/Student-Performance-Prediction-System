import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from tkinter import filedialog
import joblib

# ---------- COLORS ----------
BG = "#F2F5FC"
BLUE = "#3157D5"
DARK = "#1E293B"
WHITE = "#FFFFFF"
GREEN = "#15803D"

# ---------- MAIN WINDOW ----------
# Load trained machine learning model
model = joblib.load("student_model.joblib")
root = tk.Tk()
root.title("Student Performance Prediction System")
root.geometry("850x650")
root.minsize(750, 600)
root.configure(bg=BG)

style = ttk.Style()
style.theme_use("clam")
style.configure("TEntry", padding=8, font=("Segoe UI", 11))

# ---------- HEADER ----------
header = tk.Frame(root, bg=BLUE, height=110)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="STUDENT PERFORMANCE",
    font=("Segoe UI", 23, "bold"),
    bg=BLUE,
    fg=WHITE
).pack(anchor="w", padx=28, pady=(18, 0))

tk.Label(
    header,
    text="PREDICTION SYSTEM  |  Academic Analytics",
    font=("Segoe UI", 10),
    bg=BLUE,
    fg=WHITE
).pack(anchor="w", padx=30, pady=5)

# ---------- MAIN CONTENT ----------
content = tk.Frame(root, bg=BG)
content.pack(fill="both", expand=True, padx=30, pady=22)

tk.Label(
    content,
    text="Enter Student Information",
    font=("Segoe UI", 17, "bold"),
    bg=BG,
    fg=DARK
).pack(anchor="w", pady=(0, 15))

form = tk.Frame(content, bg=WHITE)
form.pack(fill="x")

def create_field(label, row, default=""):
    tk.Label(
        form,
        text=label,
        font=("Segoe UI", 11, "bold"),
        bg=WHITE,
        fg=DARK
    ).grid(row=row, column=0, sticky="w", padx=20, pady=12)

    entry = ttk.Entry(form, width=35)
    entry.grid(row=row, column=1, sticky="ew", padx=20, pady=12)

    if default:
        entry.insert(0, default)

    return entry

form.columnconfigure(1, weight=1)

name_entry = create_field("Student Name", 0)
marks_entry = create_field("Previous Exam Marks (%)", 1)
attendance_entry = create_field("Attendance (%)", 2)
hours_entry = create_field("Daily Study Hours", 3)

# ---------- PREDICTION ----------
result_box = tk.Frame(
    content,
    bg=WHITE,
    highlightbackground="#D9E2F2",
    highlightthickness=1
)
result_box.pack(fill="x", pady=18)

tk.Label(
    result_box,
    text="PREDICTED PERFORMANCE",
    font=("Segoe UI", 10, "bold"),
    bg=WHITE,
    fg="#64748B"
).pack(pady=(15, 5))

result_label = tk.Label(
    result_box,
    text="Enter details to begin",
    font=("Segoe UI", 20, "bold"),
    bg=WHITE,
    fg=BLUE
)
result_label.pack(pady=(0, 5))

details_label = tk.Label(
    result_box,
    text="Your prediction will appear here.",
    font=("Segoe UI", 10),
    bg=WHITE,
    fg="#64748B"
)
details_label.pack(pady=(0, 15))

def predict_performance():
    name = name_entry.get().strip()

    try:
        marks = float(marks_entry.get())
        attendance = float(attendance_entry.get())
        hours = float(hours_entry.get())
    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter valid numbers for marks, attendance, and study hours."
        )
        return

    if not name:
        messagebox.showwarning(
            "Missing Name",
            "Please enter the student's name."
        )
        return

    if not 0 <= marks <= 100:
        messagebox.showerror("Invalid Marks", "Marks must be between 0 and 100.")
        return

    if not 0 <= attendance <= 100:
        messagebox.showerror("Invalid Attendance", "Attendance must be between 0 and 100.")
        return

    if not 0 <= hours <= 24:
        messagebox.showerror("Invalid Study Hours", "Study hours must be between 0 and 24.")
        return

    # Machine Learning Prediction
    prediction = model.predict([[marks, attendance, hours]])[0]
    # Passing Marks Validation
    if marks < 35:
        prediction = "Needs Improvement"

    if prediction == "Good":
        display_prediction = "Good Performance"
        color = GREEN
        advice = "Maintain your study routine and keep practising."

    elif prediction == "Average":
        display_prediction = "Average Performance"
        color = "#B7791F"
        advice = "Review difficult topics and practise regularly."

    else:
        display_prediction = "Needs Improvement"
        color = "#DC2626"
        advice = "Try a study timetable and seek help when needed."

    # Open Separate Result Dashboard
    dashboard = tk.Toplevel(root)
    dashboard.title("Student Performance - Result Dashboard")
    dashboard.geometry("1000x700")
    dashboard.resizable(True, True)
    dashboard.minsize(800, 600)

    # Header
    header = tk.Frame(dashboard, bg="#3157D5", height=100)
    header.pack(fill="x")

    tk.Label(
        header,
        text="STUDENT PERFORMANCE REPORT",
        font=("Arial", 19, "bold"),
        bg="#3157D5",
        fg="white"
    ).pack(pady=30)

    # Result Card
    card = tk.Frame(
        dashboard,
        bg="white",
        highlightbackground="#DCE3F0",
        highlightthickness=1
    )
    card.pack(padx=40, pady=25, fill="both", expand=True)

    tk.Label(
        card,
        text="Analysis Complete!",
        font=("Arial", 20, "bold"),
        bg="white",
        fg="#1E293B"
    ).pack(pady=(25, 10))

    tk.Label(
        card,
        text=f"Student Name: {name}",
        font=("Arial", 14),
        bg="white",
        fg="#475569"
    ).pack(pady=10)
    # Student Information Cards
    info_frame = tk.Frame(card, bg="white")
    info_frame.pack(pady=12)

    student_info = [
        ("MARKS", f"{marks:g}/100"),
        ("ATTENDANCE", f"{attendance:g}%"),
        ("STUDY HOURS", f"{hours:g} hrs")
    ]

    for column, (label, value) in enumerate(student_info):
        info_card = tk.Frame(
            info_frame,
            bg="#EAF0FF",
            width=150,
            height=75
        )
        info_card.grid(row=0, column=column, padx=7)
        info_card.grid_propagate(False)

        tk.Label(
            info_card,
            text=label,
            font=("Arial", 9, "bold"),
            bg="#EAF0FF",
            fg="#64748B"
        ).pack(pady=(10, 3))

        tk.Label(
            info_card,
            text=value,
            font=("Arial", 14, "bold"),
            bg="#EAF0FF",
            fg="#3157D5"
        ).pack()

    tk.Label(
        card,
        text="PREDICTED PERFORMANCE",
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#64748B"
    ).pack(pady=(15, 5))

    tk.Label(
        card,
        text=display_prediction,
        font=("Arial", 25, "bold"),
        bg="white",
        fg=color
    ).pack(pady=10)

    tk.Label(
        card,
        text=f"Machine Learning Result: {prediction}",
        font=("Arial", 12),
        bg="white",
        fg="#475569"
    ).pack(side="bottom", pady=8)
    # Visual Performance Indicator
    indicator_frame = tk.Frame(card, bg="white")
    indicator_frame.pack(pady=8)

    tk.Label(
        indicator_frame,
        text="PERFORMANCE STATUS",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#64748B"
    ).pack(pady=3)

    status_badge = tk.Label(
        indicator_frame,
        text=f"●  {display_prediction.upper()}",
        font=("Arial", 13, "bold"),
        bg=color,
        fg="white",
        padx=20,
        pady=8
    )
    status_badge.pack(pady=5)
    # Download PDF Report Button
    tk.Button(
        card,
        text="Download Result Report (PDF)",
        font=("Arial", 11, "bold"),
        bg="#15803D",
        fg="white",
        relief="flat",
        cursor="hand2",
        command=lambda: download_report(),
        padx=15,
        pady=10
    ).pack(pady=8)

        # Download PDF Result Report Button
    tk.Button(
        card,
        text="Download Result Report (PDF)",
        font=("Arial", 11, "bold"),
        bg="#15803D",
        fg="white",
        relief="flat",
        cursor="hand2",
        command=lambda: download_report(),
        padx=15,
        pady=10
    ).pack(pady=8)

tk.Label(
        card,
        text="Personalized Recommendation",
        font=("Arial", 13, "bold"),
        bg="white",
        fg="#3157D5"
    ).pack(pady=(15, 5))

tk.Label(
        card,
        text=advice,
        font=("Arial", 11),
        bg="white",
        fg="#475569",
        wraplength=480,
        justify="center"
    ).pack(pady=5)

    # Download PDF Result Report
    def download_report():
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile=f"{name}_Performance_Report.pdf"
        )

        if not file_path:
            return

        pdf = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4

        pdf.setFillColorRGB(0.19, 0.34, 0.84)
        pdf.rect(0, height - 100, width, 100, fill=1)

        pdf.setFillColorRGB(1, 1, 1)
        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawCentredString(
            width / 2, height - 60,
            "STUDENT PERFORMANCE REPORT"
        )

        pdf.setFillColorRGB(0.1, 0.15, 0.25)
        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawString(60, height - 155, "Student Information")

        pdf.setFont("Helvetica", 12)
        pdf.drawString(60, height - 190, f"Student Name: {name}")
        pdf.drawString(60, height - 220, f"Marks: {marks:g}/100")
        pdf.drawString(60, height - 250, f"Attendance: {attendance:g}%")
        pdf.drawString(60, height - 280, f"Study Hours: {hours:g}")

        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawString(60, height - 335, "Prediction Result")

        pdf.setFont("Helvetica-Bold", 17)
        pdf.drawString(60, height - 370, display_prediction)

        pdf.setFont("Helvetica", 12)
        pdf.drawString(60, height - 405, f"ML Prediction: {prediction}")

        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(60, height - 455, "Personalized Recommendation")

        pdf.setFont("Helvetica", 11)
        pdf.drawString(60, height - 480, advice)

        pdf.save()

        messagebox.showinfo(
            "Report Downloaded",
            "Student performance report saved successfully!"
        )
    
    
    # Close Button
        tk.Button(
        card,
        text="Close Dashboard",
        font=("Arial", 12, "bold"),
        bg="#3157D5",
        fg="white",
        activebackground="#2445B0",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        command=dashboard.destroy,
        padx=20,
        pady=10
    ).pack(side="bottom", pady=8)

button = tk.Button(
    content,
    text="  Analyze Student Performance  ",
    command=predict_performance,
    font=("Segoe UI", 12, "bold"),
    bg=BLUE,
    fg=WHITE,
    activebackground="#2445B5",
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    padx=15,
    pady=12
)
button.pack(pady=2)

tk.Label(
    content,
    text="Educational demo only — results are estimates, not guarantees.",
    font=("Segoe UI", 9),
    bg=BG,
    fg="#64748B"
).pack(pady=10)

root.mainloop()