# 🐍 SQL-Python Database Management System

A final project for CSC-225 at Bunker Hill Community College demonstrating the integration of **Python** with **MySQL** for user and login database management using SQL queries.

## 📚 Course Context

This project was developed as part of **Topic 6: SQL Database Programming** and serves as **Database Project-4** in the CSC-225: Introduction to Programming (Python) course.

## 🛠 Features

- Create and manage a MySQL database using Python
- Two tables: `User` and `Login`
- Full CRUD functionality:
  - **Create** (Insert new records)
  - **Read** (Select records)
  - **Update** (Modify existing records)
  - **Delete** (Remove records)
- Encrypted password storage
- Root password entry prompt for dynamic setup
- Modular, reusable Python code

## 🗃️ Database Design

### `User` Table

| Field        | Type     | Description                  |
|--------------|----------|------------------------------|
| `userId`     | INT      | Primary key (unique)         |
| `firstName`  | VARCHAR  | User's first name            |
| `lastName`   | VARCHAR  | User's last name             |
| `email`      | VARCHAR  | User's email address         |
| `accessLevel`| VARCHAR  | Access level (admin/basic)   |

### `Login` Table

| Field        | Type     | Description                           |
|--------------|----------|---------------------------------------|
| `loginId`    | INT      | Primary key (unique)                  |
| `userId`     | INT      | Foreign key (references `User.userId`)|
| `username`   | VARCHAR  | Login username                        |
| `password`   | VARCHAR  | Encrypted login password              |

## 🧑‍💻 Technologies Used

- **Python 3.x**
- **MySQL**
- **MySQL Connector (Python module)**
- **Hashlib** for password encryption

## 🚀 How to Run

1. Ensure you have **MySQL Server** and **MySQL Workbench** installed.
2. Install the required Python package:
   ```bash
   pip install mysql-connector-python
   ```
3. Clone this repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   ```
4. Run the main Python script:
   ```bash
   python main.py
   ```
5. Enter your **MySQL root password** when prompted.

## 📦 Folder Contents

```
SQL_PY/
├── main.py                # Main Python program
├── db_setup.sql           # Optional SQL script to review
├── README.md              # This file
└── ...
```

## ✅ Requirements

- Python 3.8+
- MySQL Server
- mysql-connector-python
- Basic terminal usage

## 🔐 Security Notes

- Passwords are stored encrypted using SHA-256.
- Never upload your real root credentials or `.env` files publicly.

## 👤 Author

**[Your Name]**  
Computer Science Student  
Bunker Hill Community College  
Spring 2025

## 📅 Submission Info

- **Course:** CSC-225 Introduction to Programming
- **Instructor:** [Instructor Name]
- **Due Date:** May 2, 2025
- **Submitted:** April 29, 2025

## 📝 License

This project is for educational purposes only. Redistribution is permitted under the MIT License. See [LICENSE](LICENSE) file for details.
