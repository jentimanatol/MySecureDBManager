# 🔐 MySecureDBManager

A sleek and secure command-line database manager built with Python and MySQL. Originally developed for academic excellence at Bunker Hill Community College, now made open-source for everyone to learn, modify, and deploy.

## ✨ What is MySecureDBManager?

**MySecureDBManager** is a Python-based CLI application that allows you to interact with a MySQL database by performing full **CRUD** operations on `User` and `Login` tables. It's ideal for beginner developers learning about SQL, Python database connections, and encryption practices.

## 🎓 Academic Origin

This project was born in the classroom of CSC-225 (Intro to Programming - Python) at BHCC and fulfilled the **Database Project-4** requirements with clean, modular code and real-world concepts.

## 🚀 Features

- 🔒 Encrypted password storage using SHA-256
- 🧠 Fully interactive command-line interface
- 🗃️ Two-table relational database:
  - Users
  - Logins (linked via foreign key)
- 🛠️ Full CRUD:
  - Create, Read, Update, Delete Users and Logins
- 🔑 Secure MySQL root password prompt
- 🧩 Modular design for easy upgrades

## 📐 Database Schema

### `User` Table

| Column       | Type     | Description                  |
|--------------|----------|------------------------------|
| `userId`     | INT      | Primary key, auto-increment  |
| `firstName`  | VARCHAR  | User's first name            |
| `lastName`   | VARCHAR  | User's last name             |
| `email`      | VARCHAR  | User's email address         |
| `accessLevel`| VARCHAR  | 'basic' or 'admin'           |

### `Login` Table

| Column       | Type     | Description                           |
|--------------|----------|---------------------------------------|
| `loginId`    | INT      | Primary key, auto-increment           |
| `userId`     | INT      | Foreign key to `User.userId`          |
| `username`   | VARCHAR  | Login username                        |
| `password`   | VARCHAR  | Encrypted password                    |

## 💻 Getting Started

### 🧰 Prerequisites

- Python 3.8+
- MySQL Server + MySQL Workbench
- mysql-connector-python

### 📦 Installation

```bash
pip install mysql-connector-python
```

### ▶️ Running the App

```bash
python main.py
```

When prompted, enter your MySQL root password to establish the connection and create the database automatically.

## 🗂️ Project Structure

```
MySecureDBManager/
├── main.py                # Main application
├── BSelvarajLogins.sql    # Optional SQL script
├── README.md              # Project documentation
└── ...
```

## 🧠 Educational Value

- Learn Python-MySQL interaction
- Understand stored procedures and encryption
- Practice secure data handling
- Expand on a real-world CRUD project

## 👤 Author

**B. Selvaraj**  
Computer Science Student  
Bunker Hill Community College  
Spring 2025

## 📅 Submission Info

- **Course:** CSC-225 Introduction to Programming
- **Instructor:** [Instructor Name]
- **Project Tag:** Final Submission
- **Submitted:** April 29, 2025

## 🛡 License

This project is released under the MIT License. Feel free to use, fork, and improve it!

---
> 💬 _"Simple, secure, and built for students — that's MySecureDBManager!"_
