def get_student_data():
    """Read and validate student records."""

    n, k, m = map(int, input("Enter n, k and m: ").split())

    if not (1 <= n <= 100000):
        raise ValueError("Number of students must be between 1 and 100000.")

    if not (1 <= k <= 50):
        raise ValueError("K must be between 1 and 50.")

    if not (1 <= m <= 12):
        raise ValueError("Number of subjects must be between 1 and 12.")

    students = []

    print("\nEnter student details:")
    print("enrollment name semester CPI mark1 mark2 ... mark_m")

    for i in range(n):
        data = input(f"Student {i + 1}: ").split()

        if len(data) != 4 + m:
            raise ValueError(
                f"Student {i + 1}: Invalid number of values."
            )

        enrollment = data[0]
        name = data[1]

        semester = int(data[2])
        cpi = float(data[3])
        marks = list(map(int, data[4:]))

        # Validate semester, CPI and marks
        if not 1 <= semester <= 8:
            raise ValueError("Semester must be between 1 and 8.")

        if not 0.0 <= cpi <= 10.0:
            raise ValueError("CPI must be between 0 and 10.")

        if any(mark < 0 or mark > 100 for mark in marks):
            raise ValueError("Marks must be between 0 and 100.")

        # Tuple containing the complete student record
        student = (enrollment, name, semester, cpi, marks)

        students.append(student)

    return n, k, m, students


def average_marks(marks):
    """Return average marks of a student."""
    return sum(marks) / len(marks)


def find_semester_toppers(students, k):
    """
    Find top K students for each semester.

    Priority:
    1. Higher CPI
    2. Higher average marks
    3. Smaller enrollment number
    """

    # Dictionary: semester -> list of students
    semester_data = {}

    for student in students:
        semester = student[2]

        if semester not in semester_data:
            semester_data[semester] = []

        semester_data[semester].append(student)

    semester_toppers = {}

    for semester, student_list in semester_data.items():

        # Sort using the required priority
        student_list.sort(
            key=lambda student: (
                -student[3],                    # Higher CPI
                -average_marks(student[4]),     # Higher average marks
                student[0]                      # Smaller enrollment
            )
        )

        # Store only the enrollment numbers of top K students
        semester_toppers[semester] = [
            student[0]
            for student in student_list[:k]
        ]

    return semester_toppers


def find_subject_toppers(students, m):
    """Find topper(s) for every subject."""

    subject_toppers = {}

    for subject_index in range(m):

        highest_mark = -1
        toppers = []

        for student in students:

            enrollment = student[0]
            mark = student[4][subject_index]

            if mark > highest_mark:
                highest_mark = mark
                toppers = [enrollment]

            elif mark == highest_mark:
                toppers.append(enrollment)

        # If multiple students have the highest mark,
        # sort their enrollment numbers.
        toppers.sort()

        subject_code = f"S{subject_index + 1}"
        subject_toppers[subject_code] = toppers

    return subject_toppers


def display_results(semester_toppers, subject_toppers):
    """Display the final result."""

    print("\n----- Result -----")

    # Semester-wise top K students
    for semester in sorted(semester_toppers):
        print(
            f"Semester {semester}: "
            f"{' '.join(semester_toppers[semester])}"
        )

    # Subject-wise toppers
    for subject in subject_toppers:
        print(
            f"{subject}: "
            f"{' '.join(subject_toppers[subject])}"
        )


def main():
    """Main program."""

    try:
        n, k, m, students = get_student_data()

        semester_toppers = find_semester_toppers(
            students, k
        )

        subject_toppers = find_subject_toppers(
            students, m
        )

        display_results(
            semester_toppers,
            subject_toppers
        )

    except ValueError as error:
        print("Input Error:", error)


if __name__ == "__main__":
    main()

