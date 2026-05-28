
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
            cur.execute("SELECT * FROM ujc ORDER BY id")
            rows = cur.fetchall()
            if rows:
                for id, name, department, position, salary, status in rows:
                    print(f"{id} | {name.title():<22} | {department.title():<12} | {position.title():<22} | {salary:<6} | {status.title()}")
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
            cur.execute("SELECT * FROM ujc ORDER BY id")
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
    
    except OSError as e:
        print(f"File error: {e}")
        return None
   
def employee_exists(path, employee_id):
    try:
        with sqlite3.connect(path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM ujc WHERE id = ?", (employee_id, ))
            row = cur.fetchone()
            if row is not None:
                return True
            return False
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False


def bulk_import_folder(path, folder_path):
    try:
        with sqlite3.connect(path) as conn:
            cur = conn.cursor()
            
            files = folder_path.rglob("*.csv")
            successfully_imported = 0
            processed_files = 0
            
            skipped = 0
            skipped_report = []
            
            required_fields = {"name", "department", "position", "salary", "status"}

            for f in files:
                with open(f, "r", encoding="utf-8", newline="") as infile:
                    reader = csv.DictReader(infile)
                    csv_fields = set(reader.fieldnames or [])

                    if not required_fields.issubset(csv_fields):
                        skipped_report.append(f"Skipped file {f.name} | Reason: missing required columns")
                        continue
                
                    for row in reader:
                        name = (row["name"] or "").strip().lower()
                        department = (row["department"] or "").strip().lower()
                        position = (row["position"] or "").strip().lower()
                        salary = row["salary"]
                        status = (row["status"] or "").strip().lower()
                        
                        if not name:
                            skipped_report.append(f"Skipped row in {f.name} | Reason: 'name' missing: {row}")
                            skipped += 1
                            continue
                        
                        if not department:
                            skipped_report.append(f"Skipped row in {f.name} | Reason: 'department' missing: {row}")
                            skipped += 1
                            continue
                        
                        if not position:
                            skipped_report.append(f"Skipped row in {f.name} | Reason: 'position' missing: {row}")
                            skipped += 1
                            continue
                        
                        try:
                            salary = int(salary)
                        except (ValueError, TypeError):
                            skipped_report.append(f"Skipped row in {f.name} | Reason: 'salary' missing or invalid number: {row}")
                            skipped += 1
                            continue
                        
                        if not status:
                            skipped_report.append(f"Skipped row in {f.name} | Reason: 'status' missing: {row}")
                            skipped += 1
                            continue
                        
                        if status not in {"full-time", "part-time", "contract"}:
                            skipped_report.append(f"Skipped row in {f.name} | Reason: 'status' must be 'full-time', 'part-time,' 'contract': {row}")
                            skipped += 1
                            continue
                        
                        successfully_imported += 1
                        
                        print(name, department, position, salary, status)
                        
                        cur.execute("INSERT INTO ujc (name, department, position, salary, status) VALUES (?,?,?,?,?)", 
                                    (name, department, position, salary, status))

                processed_files += 1
                
            return skipped_report, skipped, successfully_imported, processed_files
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    

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
        print("7. Import CSVs")
        print("8. Exit")
        
        try:
            user_choice = int(input("Please enter a number: "))
        except ValueError:
            print("User must enter a number (1-8)")
            continue
        
        if user_choice == 8:
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
                
                if not status:
                    print("You cannot leave the status field empty.")
                    continue
                    
                if status not in {"full-time", "part-time", "contract"}:
                    print("'Status' must be 'full-time', 'part-time,' or 'contract'")
                    continue
                
                break
                        
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
                result = employee_exists(ujc_database, employee_id)
                if result:
                    search_employees(ujc_database, employee_id)
                    choice = input("Confirm deletion (y/n)? ").strip().lower()
                    if choice not in ("y", "yes"):
                        print("Returning to main menu...")
                        continue
                else:
                    print("Employee not found.")
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
                
        elif user_choice == 7:
            while True:
                fp = BASE_DIR / Path(input("Please enter a folder path: "))
                if fp.exists() and fp.is_dir():
                    skipped_report, skipped, successfully_imported, processed_files = bulk_import_folder(ujc_database, fp)
                    print("\nDatabase has been updated.\n")
                    print(f"Processed {processed_files} csv files.")
                    print(f"Successfully imported {successfully_imported} rows.")
                    print(f"Skipped {skipped} rows.\n")
                    for line in skipped_report:
                        print(line)
                        
                    break
                else:
                    print("Please enter a valid path.")
                    continue
            
# 1. Ask user for folder path
# 2. Validate folder exists
# 3. Find CSV files with rglob()
# 4. Open SQLite connection once
# 5. Loop through CSV files
# 6. Loop through rows
# 7. Clean/validate rows
# 8. Insert valid rows
# 9. Track imported/skipped counts
# 10. Print summary
                
        else:
            print("Not a valid entry.")
            
