import os
import csv
import json

employees = []

def validate_date(date):
    try:
        parts = date.split("-")
        if len(parts) != 3:
            return False
        year, month, day = map(int, parts)
        if not (1900 <= year <= 2025):
            return False
        if not (1 <= month <= 12):
            return False
        if not (1 <= day <= 31):
            return False
        if month in [4, 6, 9, 11] and day > 30:
            return False
        if month == 2:
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0): 
                return day <= 29
            else:
                return day <= 28
        return True
    except ValueError:
        return False

#1.adding an employee
def add_employee():
    try:
        emp_id = int(input("Enter employee ID: "))
        if any(i["id"] == emp_id for i in employees):
            print("ID already exists!")
            return
        name = input("Enter employee name: ")
        position = input("Enter employee position: ")
        salary = int(input("Enter employee salary: "))
        skills = set(input("Enter skills (comma-separated): ").split(","))
        date = input("Enter employment date (YYYY-MM-DD): ")
        if not validate_date(date):
            print("Invalid date format or value. Please try again.")
            return
        employees.append({
            "id": emp_id,
            "name": name,
            "position": position,
            "salary": salary,
            "skills": skills,
            "employment_date": date
        })
        print("Employee added successfully!")
    except ValueError:
        print("Invalid input. Please try again.")

#2.Searching employees
def search_employees():
    search_type = input("Search by (id/name/skills): ").lower().strip()
    if search_type == "id":
        emp_id = int(input("Enter employee ID: "))
        results = [i for i in employees if i["id"] == emp_id]
    elif search_type == "name":
        name = input("Enter name: ").lower().strip()
        results = [i for i in employees if name in i["name"].lower()]
    elif search_type == "skills":
        skill = input("Enter skill: ").lower().strip()
        results = [i for i in employees if skill in (s.lower() for s in i["skills"])]
    else:
        print("Invalid search type!")
        return
    for i in results:
        print(i)

#4.Updating employee
def update_employee():
    emp_id = int(input("Enter employee ID to update: "))
    for i in employees:
        if i["id"] == emp_id:
            pole = input("Update (salary/skills): ").lower().strip()
            if pole == "salary":
                i["salary"] = int(input("Enter new salary: "))
            elif pole == "skills":
                action = input("Add or Remove skills? (add/remove): ").lower().strip()
                skill = input("Enter skill: ")
                if action == "add":
                    i["skills"].add(skill)
                elif action == "remove":
                    i["skills"].discard(skill)
                else:
                    print("Invalid action!")
            print("Employee updated successfully!")
            return
    print("No any employee")


#5.Display employees
def display_employees():
    filter_position = input("Filter by position (leave blank for all): ").lower().strip()
    sort_by = input("Sort by (salary/employment_date/none): ").lower().strip()
    filtered_employees = [i for i in employees if filter_position in i["position"].lower()] if filter_position else employees
    if sort_by == "salary":
        filtered_employees = sorted(filtered_employees, key=lambda x: x["salary"])
    elif sort_by == "employment_date":
        filtered_employees = sorted(filtered_employees, key=lambda x: x["employment_date"], reverse=True)
    for c in filtered_employees:
        print(c)

#6.Generate analytics
def generate_analytics():
    if not employees:
        print("No any employees")
        return
    total = sum(i["salary"] for i in employees)
    aver = round((total / len(employees)), 2)
    highest_salary = employees[0]
    for i in employees:
        if i["salary"] > highest_salary["salary"]:
            highest_salary = i

    lowest_salary = employees[0]
    for i in employees:
        if i["salary"] < lowest_salary["salary"]:
            lowest_salary = i

    print(f'''
    Total Payroll: {total}$")
    Average Salary: {aver}$")
    Highest Salary: {highest_salary['name']} ({highest_salary['salary']}$)")
    Lowest Salary: {lowest_salary['name']} ({lowest_salary['salary']}$)
    ''')

#Load data from CSV
def load_data_from_csv(file_path):
    try:
        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if not validate_date(row["Employment Date"]):
                    print(f"Skipping invalid date: {row['Employment Date']}")
                    continue
                employees.append({
                    "id": int(row["ID"]),
                    "name": row["Name"],
                    "position": row["Position"],
                    "salary": int(row["Salary"]),
                    "skills": set(row["Skills"].split(",")),
                    "employment_date": row["Employment Date"]
                })
    except FileNotFoundError:
        print("File not found. Please provide a valid CSV file.")
    except Exception:
        print(f"Error loading data: {Exception}")
#7Save data to JSON
def save_data_to_json(file_path):
    try:
        data_to_save = [
            {
                "id": i["id"],
                "name": i["name"],
                "position": i["position"],
                "salary": i["salary"],
                "skills": list(i["skills"]),
                "employment_date": i["employment_date"],
            }
            for i in employees
        ]

        with open(file_path, 'w') as json_file:
            json.dump(data_to_save, json_file, indent=4)
        print("Data saved to JSON successfully!")
    except Exception:
        print(f"Error saving to JSON: {Exception}")

#8Save data to CSV
def export_data_to_csv(test):
    try:
        with open(test, 'w', newline='') as csv_file:
            fieldnames = ["ID", "Name", "Position", "Salary", "Skills", "Employment Date"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for emp in employees:
                writer.writerow({
                    "ID": emp["id"],
                    "Name": emp["name"],
                    "Position": emp["position"],
                    "Salary": emp["salary"],
                    "Skills": ','.join(emp["skills"]),
                    "Employment Date": emp["employment_date"]
                })
        print("Data exported to CSV successfully!")
    except Exception as e:
        print(f"Error exporting to CSV: {e}")

#9Delete a file
def delete_file(test):
    try:
        if os.path.exists(test):
            os.remove(test)
            print(f"File {test} deleted successfully!")
        else:
            print("File not found.")
    except Exception as e:
        print(f"Error deleting file: {e}")


load_data_from_csv('D:/downloads/employees.csv')

print('Welcome to the Advanced Employee Management System! ')
while True:
    print(f'''
    Menu: 
    1. Add an employee 
    2. Search for employees 
    3. Remove an employee 
    4. Update employee information 
    5. Display all employees 
    6. Generate analytics 
    7. Save data to JSON
    8. Export data to CSV
    9. Delete a file 
    10. Exit 
        ''')
    menuchoser = input("Your choice: ").strip()
    if  menuchoser == "1":
        add_employee()
    elif menuchoser == "2":
        search_employees()
    elif menuchoser == "3":
        emp_id = int(input("Enter employee ID to remove: "))
        employees[:] = [i for i in employees if i["id"] != emp_id]
        print("Employee removed successfully!")
    elif menuchoser == "4":
        update_employee()
    elif menuchoser == "5":
        display_employees()
    elif menuchoser == "6":
        generate_analytics()
    elif menuchoser == "7":
        test = input("Enter JSON file path to save: ")
        save_data_to_json(test)
    elif menuchoser == "8":
        test = input("Enter CSV file path to export: ")
        export_data_to_csv(test)
    elif menuchoser == "9":
        test = input("Enter file path to delete: ")
        delete_file(test)
    elif menuchoser == "10":
        print("Thank you for using the Employee Management System. Goodbye!")
        break
    else:
        if menuchoser.isdigit():
            print("Please, write a number between 1 and 10")
        else:
            print("Invalid choose! please enter a number")