# Employee Database (CLI Tool for HR and Managers)

This is a full CRUD-style SQLite tool with a command-line interface.
It is designed as a simple internal tool that can replace a hard-to-manage spreadsheet for tracking employee data.

Features
* Add employees with relevant information (name, department, position, salary, status)
* Delete employees from the database
* Update employee status (e.g., full-time, part-time, contract)
* Search for an employee by ID and display their full employee record
* View all employees in a formatted, readable format
* Export all employee data to a CSV file

Technologies Used
* Python
* SQLite (via sqlite3)
* CSV (via csv)
* Path handling (via pathlib)


How to Run
* Run the file: `employee_cli_database.py`
* Follow the on-screen menu to select an option

Requirements:
* Python installed (standard library modules are used; no external packages required)

Notes:
* The SQLite database and CSV export file are automatically created in the same directory as the script

Skills Demonstrated
* SQLite CRUD operations (create, read, update, delete)
* Building a CLI-based interface with input validation and error handling
* Exporting structured data to CSV format
* Working with Python standard library modules (sqlite3, csv, pathlib)
* Input validation and basic data integrity checks

Upcoming Features: 
* Bulk CSV Import to allow rapid migration of legacy spreadsheet data.
* Improved status validation