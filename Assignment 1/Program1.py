students = [
    {"id": 101, "name": "Hetvi", "marks": (85, 90, 88)},
    {"id": 102, "name": "Riya", "marks": (78, 82, 80)},
    {"id": 103, "name": "Neha", "marks": (92, 89, 95)},
    {"id": 104, "name": "Amit", "marks": (75, 80, 78)}
]

# Calculate total and percentage
for student in students:
    total = sum(student["marks"])
    percentage = total / len(student["marks"])
    
    student["total"] = total
    student["percentage"] = percentage

# Sort students according to percentage
students.sort(key=lambda x: x["percentage"], reverse=True)

# Display merit list
print("----- CAMPUS MERIT LIST -----")

for rank, student in enumerate(students, start=1):
    print("Rank:", rank)
    print("ID:", student["id"])
    print("Name:", student["name"])
    print("Marks:", student["marks"])
    print("Total:", student["total"])
    print("Percentage:", student["percentage"])
    print("-----------------------------")

# Find students eligible for merit
eligible = {student["name"] for student in students
            if student["percentage"] >= 80}

print("Students with 80% or above:")
print(eligible)
