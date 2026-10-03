import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
import os

DATA_FILE = "student_data.json"

class AssignmentManager:

    def __init__(self, root):
        self.root = root
        self.root.title("Student Assignment Manager")
        self.root.geometry("950x600")

        self.students = {}
        self.submissions = []

        self.load_data()
        self.create_widgets()
        self.show_records()

    # Load saved data
    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as file:
                    data = json.load(file)
                    self.students = data.get("students", {})
                    self.submissions = data.get("submissions", [])
            except (json.JSONDecodeError, OSError):
                messagebox.showwarning(
                    "Warning", "Could not load saved data."
                )

    # Save data to JSON
    def save_data(self):
        with open(DATA_FILE, "w") as file:
            json.dump({
                "students": self.students,
                "submissions": self.submissions
            }, file, indent=4)

    # Create GUI
    def create_widgets(self):

        form = ttk.LabelFrame(
            self.root, text="Student and Assignment Details"
        )
        form.pack(fill="x", padx=10, pady=10)

        ttk.Label(form, text="Enrollment:").grid(
            row=0, column=0, padx=5, pady=5
        )
        self.enrollment = ttk.Entry(form)
        self.enrollment.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Student Name:").grid(
            row=0, column=2, padx=5, pady=5
        )
        self.name = ttk.Entry(form)
        self.name.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form, text="Assignment:").grid(
            row=1, column=0, padx=5, pady=5
        )
        self.assignment = ttk.Entry(form)
        self.assignment.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form, text="Marks:").grid(
            row=1, column=2, padx=5, pady=5
        )
        self.marks = ttk.Entry(form)
        self.marks.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(form, text="Status:").grid(
            row=2, column=0, padx=5, pady=5
        )
        self.status = ttk.Combobox(
            form,
            values=["Pending", "Completed"],
            state="readonly"
        )
        self.status.set("Pending")
        self.status.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form, text="Remarks:").grid(
            row=2, column=2, padx=5, pady=5
        )
        self.remarks = ttk.Entry(form)
        self.remarks.grid(row=2, column=3, padx=5, pady=5)

        # Buttons
        buttons = ttk.Frame(self.root)
        buttons.pack(pady=5)

        ttk.Button(
            buttons, text="Add Student",
            command=self.add_student
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            buttons, text="Add Submission",
            command=self.add_submission
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            buttons, text="Update Marks",
            command=self.update_marks
        ).grid(row=0, column=2, padx=5)

        ttk.Button(
            buttons, text="Export CSV",
            command=self.export_csv
        ).grid(row=0, column=3, padx=5)

        # Filter
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="Filter:").pack(side="left")

        self.filter_status = ttk.Combobox(
            filter_frame,
            values=["All", "Pending", "Completed"],
            state="readonly"
        )
        self.filter_status.set("All")
        self.filter_status.pack(side="left", padx=5)
        self.filter_status.bind(
            "<<ComboboxSelected>>",
            lambda event: self.show_records()
        )

        # Table
        columns = (
            "Enrollment", "Name", "Assignment",
            "Status", "Marks", "Remarks"
        )

        self.table = ttk.Treeview(
            self.root, columns=columns, show="headings"
        )

        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=140)

        self.table.pack(
            fill="both", expand=True, padx=10, pady=10
        )

    # Validate student details
    def validate_student(self):
        enrollment = self.enrollment.get().strip()
        name = self.name.get().strip()

        if not enrollment or not name:
            raise ValueError("Enter enrollment and student name.")

        return enrollment, name

    # Add a student
    def add_student(self):
        try:
            enrollment, name = self.validate_student()

            if enrollment in self.students:
                raise ValueError("Student already exists.")

            self.students[enrollment] = name
            self.save_data()

            messagebox.showinfo(
                "Success", "Student added successfully."
            )

        except ValueError as error:
            messagebox.showerror("Input Error", str(error))

    # Add assignment submission
    def add_submission(self):
        try:
            enrollment, name = self.validate_student()
            assignment = self.assignment.get().strip()
            marks_text = self.marks.get().strip()
            status = self.status.get()
            remarks = self.remarks.get().strip()

            if not assignment:
                raise ValueError("Enter assignment name.")

            if not marks_text:
                raise ValueError("Enter marks.")

            marks = float(marks_text)

            if marks < 0:
                raise ValueError("Marks cannot be negative.")

            if status not in ["Pending", "Completed"]:
                raise ValueError("Select a valid status.")

            # Add student automatically if not present
            if enrollment not in self.students:
                self.students[enrollment] = name
            elif self.students[enrollment] != name:
                raise ValueError(
                    "Enrollment belongs to another student."
                )

            record = {
                "enrollment": enrollment,
                "name": self.students[enrollment],
                "assignment": assignment,
                "status": status,
                "marks": marks,
                "remarks": remarks
            }

            self.submissions.append(record)
            self.save_data()
            self.show_records()

            messagebox.showinfo(
                "Success", "Submission added successfully."
            )

        except ValueError as error:
            messagebox.showerror("Input Error", str(error))

    # Update marks of selected submission
    def update_marks(self):
        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "Warning", "Select a submission first."
            )
            return

        try:
            new_marks = float(self.marks.get().strip())

            if new_marks < 0:
                raise ValueError("Marks cannot be negative.")

            index = int(selected[0])
            record = self.submissions[index]

            record["marks"] = new_marks
            record["status"] = self.status.get()
            record["remarks"] = self.remarks.get().strip()

            self.save_data()
            self.show_records()

            messagebox.showinfo(
                "Success", "Submission updated successfully."
            )

        except ValueError as error:
            messagebox.showerror("Input Error", str(error))

    # Display records with filtering
    def show_records(self):
        for item in self.table.get_children():
            self.table.delete(item)

        selected_filter = self.filter_status.get()

        for index, record in enumerate(self.submissions):
            if (selected_filter == "All" or
                    record["status"] == selected_filter):

                self.table.insert(
                    "",
                    "end",
                    iid=str(index),
                    values=(
                        record["enrollment"],
                        record["name"],
                        record["assignment"],
                        record["status"],
                        record["marks"],
                        record["remarks"]
                    )
                )

    # Export CSV report
    def export_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="assignment_report.csv"
        )

        if not file_path:
            return

        try:
            with open(
                file_path, "w", newline="", encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow([
                    "enrollment", "name", "assignment",
                    "status", "marks", "remarks"
                ])

                for record in self.submissions:
                    writer.writerow([
                        record["enrollment"],
                        record["name"],
                        record["assignment"],
                        record["status"],
                        record["marks"],
                        record["remarks"]
                    ])

            messagebox.showinfo(
                "Success", "CSV report exported successfully."
            )

        except OSError as error:
            messagebox.showerror("File Error", str(error))


# Run application
root = tk.Tk()
app = AssignmentManager(root)
root.mainloop()
