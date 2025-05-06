import mysql.connector
import getpass

def connect_to_mysql():
    host = "localhost"
    user = "root"
    password = getpass.getpass("Enter MySQL root password: ")

    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database="BSelvarajLogins"
        )
        print("Connected to MySQL.")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def add_user(cursor):
    fname = input("First name: ")
    lname = input("Last name: ")
    email = input("Email: ")
    access = input("Access level (basic/admin): ")

    cursor.callproc("AddUser", [fname, lname, email, access])
    print("User added.")

def add_login(cursor):
    user_id = int(input("User ID (must exist): "))
    username = input("Username: ")
    password = input("Password: ").encode("utf-8")

    cursor.callproc("AddLogin", [user_id, username, password])
    print("Login added.")

def view_users(cursor):
    cursor.callproc("GetAllUsers")
    for result in cursor.stored_results():
        for row in result.fetchall():
            print(row)

def view_logins(cursor):
    cursor.callproc("GetAllLogins")
    for result in cursor.stored_results():
        for row in result.fetchall():
            print(row)

def update_user_email(cursor):
    user_id = int(input("User ID: "))
    new_email = input("New Email: ")
    cursor.callproc("UpdateUserEmail", [user_id, new_email])
    print("Email updated.")

def delete_user(cursor):
    user_id = int(input("User ID to delete: "))
    cursor.callproc("DeleteUser", [user_id])
    print("User deleted.")

def delete_login(cursor):
    login_id = int(input("Login ID to delete: "))
    cursor.callproc("DeleteLogin", [login_id])
    print("Login deleted.")

def main():
    conn = connect_to_mysql()
    if not conn:
        return
    cursor = conn.cursor()

    while True:
        print("\n--- Menu ---")
        print("1. Add User")
        print("2. Add Login")
        print("3. View Users")
        print("4. View Logins")
        print("5. Update User Email")
        print("6. Delete User")
        print("7. Delete Login")
        print("8. Exit")

        choice = input("Choose an option: ")
        try:
            if choice == "1":
                add_user(cursor)
            elif choice == "2":
                add_login(cursor)
            elif choice == "3":
                view_users(cursor)
            elif choice == "4":
                view_logins(cursor)
            elif choice == "5":
                update_user_email(cursor)
            elif choice == "6":
                delete_user(cursor)
            elif choice == "7":
                delete_login(cursor)
            elif choice == "8":
                break
            else:
                print("Invalid choice.")
            conn.commit()
        except mysql.connector.Error as err:
            print(f"MySQL Error: {err}")
            conn.rollback()

    cursor.close()
    conn.close()
    print("Connection closed.")

if __name__ == "__main__":
    main()
