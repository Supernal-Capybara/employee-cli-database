
import sqlite3
import csv
from pathlib import Path

BASE_DIR = Path(__file__).parent
ujc_database = BASE_DIR / "united_jovian_corporation.db"
ujc_database_csv = BASE_DIR / "united_jovian_corporation_employees.csv"

def create_table(path):
    try:
        with sqlite3.connect(path) as conn:
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS ujc (
                id INTEGER PRIMARY KEY,
                name TEXT,
                department TEXT,
                position TEXT,
                salary INTEGER,
                status TEXT);
                        """)
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    
def add_employee(path, name, department, position, salary, status):
    try:
        with sqlite3.connect(path) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO ujc (name, department, position, salary, status) VALUES (?,?,?,?,?)", 
                        (name, department, position, salary, status))
            return cur.lastrowid
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    
def view_employees(path):
    try:
        with sqlite3.connect(path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM ujc")
            rows = cur.fetchall()
            if rows:
                for id, name, department, position, salary, status in rows:
                    print(f"{id} | {name.title():<22} | {department.title():<12} | {position.title():<20} | {salary:<6} | {status.title()}")
            else:
                print("No employees found.")
                
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    
def search_employees(path, employee_id):
    try:
        with sqlite3.connect(path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM ujc WHERE id = ?",
                        (employee_id, ))
            row = cur.fetchone()
            if row is not None:
                id, name, department, position, salary, status = row
                print("Employee found:")
                print(f"{id} | {name.title()} | {department.title()} | {position.title()} | {salary} | {status.title()}")
                
            else:
                print("Employee not found.")
                
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

def update_employee(path, employee_id, status):
    try:
        with sqlite3.connect(path) as conn:
            cur = conn.cursor()
            cur.execute("UPDATE ujc SET status = ? WHERE id = ?",
                        (status, employee_id))
            return cur.rowcount == 1
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    
def delete_employee(path, employee_id):
    try:
        with sqlite3.connect(path) as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM ujc WHERE id = ?",
                        (employee_id, ))
            return cur.rowcount == 1
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    
def export_to_csv(path, csv_path):
    try:
        with sqlite3.connect(path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM ujc")
            rows = cur.fetchall()
            if rows:
                with open(csv_path, "w", encoding="utf-8", newline="") as outfile:
                    writer = csv.writer(outfile)
                    writer.writerow(["id", "name", "department", "position", "salary", "status"])
                    for id, name, department, position, salary, status in rows:
                        writer.writerow([id, name, department, position, salary, status])
                    return True
            
            return False

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    
if __name__ == "__main__":
    create_table(ujc_database)
    
    while True:
        print("Welcome to the United Jovian Corporation employee database.")
        print("1. Add an employee")
        print("2. View all employees")
        print("3. Search for an employee")
        print("4. Update an employee")
        print("5. Delete an employee")
        print("6. Export all employee data to CSV")
        print("7. Exit")
        
        try:
            user_choice = int(input("Please enter a number: "))
        except ValueError:
            print("User must enter a number (1-7)")
            continue
        
        if user_choice == 7:
            print("Goodbye.")
            break
        
        elif user_choice == 1:
            
            while True:
                name = input("Please enter the employee's full name (ex: Emily Kostova): ").strip().lower()
                if name:
                    break
                print("You cannot leave the name field empty.")
                    
            while True:
                department = input("Please enter the employee's department: ").strip().lower()
                if department:
                    break
                print("You cannot leave the department field empty.")
                   
            while True:  
                position = input("Please enter the employee's position: ").strip().lower()
                if position:
                    break
                print("You cannot leave the position field empty.")
                    
            while True:
                try:
                    salary = int(input("Please enter the employee's salary (no commas or spaces): "))
                    break
                except ValueError:
                    print("Please enter valid numbers.")
                    
            while True:
                status = input("Please enter the employee's status (full-time, part-time, contract): ").strip().lower()
                if status:
                    break
                print("You cannot leave the status field empty.")
            
            
            result = add_employee(ujc_database, name, department, position, salary, status)
            if result:
                print("Employee added.")
            else:
                print("Error: employee not added.")
        
        elif user_choice == 2:
            view_employees(ujc_database)
        
        elif user_choice == 3:
            while True:
                try:
                    employee_id = int(input("Please enter the employee's id number: "))
                    search_employees(ujc_database, employee_id)
                    break
                    
                except ValueError:
                    print("Error: Please enter a digit next time.")
        
        elif user_choice == 4:
            while True:
                try:
                    employee_id = int(input("Please enter the employee's id number: "))
                    break
                except ValueError:
                    print("Please enter a number")
                    
            while True:
                status = input("Please enter the employee's status (full-time, part-time, contract): ").strip().lower()
                if status:
                    break
                print("You cannot leave the status field empty.")
                
            result = update_employee(ujc_database, employee_id, status)
            
            if result:
                print("Employee status successfully updated.")
            else:
                print("Employee not found.")
        
        elif user_choice == 5:
            
            try:
                employee_id = int(input("Please enter the employee's id number: "))
                search_employees(ujc_database, employee_id)
                choice = input("Confirm deletion (y/n)? ").strip().lower()
                
                if choice not in ("y", "yes"):
                    print("Returning to main menu...")
                    continue
                
            except ValueError:
                print("Error: Please enter a digit next time.")
                continue
            
            result = delete_employee(ujc_database, employee_id)
            
            if result:
                print("Employee successfully deleted.")
            else:
                print("Employee not found.")
                
        elif user_choice == 6:
            result = export_to_csv(ujc_database, ujc_database_csv)
            if result:
                print(f"Successfully written to path: {ujc_database_csv}")
            else:
                print("File not saved.")
                
        else:
            print("Not a valid entry.")
            
# 1 | ekaterina kosidowski | engineering | mechanical engineer | 120000 | contract

# name, department, position, salary, status
# 1. Add employee
# 2. View employees
# 3. Search employee
# 4. Update employee
# 5. Delete employee
# 6. Exit

# Fields like:
# name
# department
# position
# salary
# status