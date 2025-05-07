import mysql.connector
import bcrypt
import re
import os
import sys
from getpass import getpass
from typing import Dict, List, Optional, Tuple, Union

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.db_name = None
    
    def connect_to_mysql(self, password: str) -> bool:
        """Connect to MySQL server with root user and provided password."""
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password=password
            )
            self.cursor = self.connection.cursor()
            print("Connected to MySQL server successfully!")
            return True
        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL server: {err}")
            return False
    
    def create_database(self, first_initial: str, last_name: str, purpose: str) -> bool:
        """Create a database with naming convention of first initial + last name + purpose."""
        try:
            # Format database name
            self.db_name = f"{first_initial}{last_name}{purpose}"
            # Sanitize database name (remove special characters)
            self.db_name = re.sub(r'[^\w]', '', self.db_name)
            
            # Create database
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
            self.cursor.execute(f"USE {self.db_name}")
            print(f"Database '{self.db_name}' created and selected successfully!")
            return True
        except mysql.connector.Error as err:
            print(f"Error creating database: {err}")
            return False
    
    def create_tables(self) -> bool:
        """Create User and Login tables."""
        try:
            # Create User table
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS User (
                userId INT AUTO_INCREMENT PRIMARY KEY,
                firstName VARCHAR(50) NOT NULL,
                lastName VARCHAR(50) NOT NULL,
                email VARCHAR(100) NOT NULL,
                accessLevel ENUM('basic', 'admin') DEFAULT 'basic'
            )
            """)
            
            # Create Login table
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Login (
                loginId INT AUTO_INCREMENT PRIMARY KEY,
                userId INT UNIQUE,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                FOREIGN KEY (userId) REFERENCES User(userId) ON DELETE CASCADE
            )
            """)
            
            print("Tables created successfully!")
            return True
        except mysql.connector.Error as err:
            print(f"Error creating tables: {err}")
            return False
    
    def insert_user(self, first_name: str, last_name: str, email: str, access_level: str) -> Optional[int]:
        """Insert a new user and return the user ID."""
        try:
            query = """
            INSERT INTO User (firstName, lastName, email, accessLevel)
            VALUES (%s, %s, %s, %s)
            """
            values = (first_name, last_name, email, access_level)
            self.cursor.execute(query, values)
            self.connection.commit()
            
            user_id = self.cursor.lastrowid
            print(f"User added successfully with ID: {user_id}")
            return user_id
        except mysql.connector.Error as err:
            print(f"Error inserting user: {err}")
            return None
    
    def insert_login(self, user_id: int, username: str, password: str) -> bool:
        """Insert login credentials with encrypted password."""
        try:
            # Hash the password
            hashed_password = self._encrypt_password(password)
            
            query = """
            INSERT INTO Login (userId, username, password)
            VALUES (%s, %s, %s)
            """
            values = (user_id, username, hashed_password)
            self.cursor.execute(query, values)
            self.connection.commit()
            
            print(f"Login credentials added successfully for user ID: {user_id}")
            return True
        except mysql.connector.Error as err:
            print(f"Error inserting login: {err}")
            return False
    
    def _encrypt_password(self, password: str) -> str:
        """Encrypt password using bcrypt."""
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        return hashed_password.decode('utf-8')
    
    def verify_password(self, entered_password: str, stored_password: str) -> bool:
        """Verify password against stored hash."""
        return bcrypt.checkpw(entered_password.encode('utf-8'), stored_password.encode('utf-8'))
    
    def select_all_users(self) -> List[Dict]:
        """Retrieve all users from the User table."""
        try:
            self.cursor.execute("SELECT userId, firstName, lastName, email, accessLevel FROM User")
            users = []
            for (user_id, first_name, last_name, email, access_level) in self.cursor:
                users.append({
                    'userId': user_id,
                    'firstName': first_name,
                    'lastName': last_name,
                    'email': email,
                    'accessLevel': access_level
                })
            return users
        except mysql.connector.Error as err:
            print(f"Error selecting users: {err}")
            return []
    
    def select_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Retrieve a specific user by ID."""
        try:
            query = "SELECT userId, firstName, lastName, email, accessLevel FROM User WHERE userId = %s"
            self.cursor.execute(query, (user_id,))
            result = self.cursor.fetchone()
            
            if result:
                user_id, first_name, last_name, email, access_level = result
                return {
                    'userId': user_id,
                    'firstName': first_name,
                    'lastName': last_name,
                    'email': email,
                    'accessLevel': access_level
                }
            else:
                print(f"No user found with ID: {user_id}")
                return None
        except mysql.connector.Error as err:
            print(f"Error selecting user: {err}")
            return None
    
    def select_login_by_username(self, username: str) -> Optional[Dict]:
        """Retrieve login information by username."""
        try:
            query = """
            SELECT l.loginId, l.userId, l.username, l.password, u.firstName, u.lastName, u.email, u.accessLevel
            FROM Login l
            JOIN User u ON l.userId = u.userId
            WHERE l.username = %s
            """
            self.cursor.execute(query, (username,))
            result = self.cursor.fetchone()
            
            if result:
                login_id, user_id, username, password, first_name, last_name, email, access_level = result
                return {
                    'loginId': login_id,
                    'userId': user_id,
                    'username': username,
                    'password': password,
                    'firstName': first_name,
                    'lastName': last_name,
                    'email': email,
                    'accessLevel': access_level
                }
            else:
                print(f"No login found with username: {username}")
                return None
        except mysql.connector.Error as err:
            print(f"Error selecting login: {err}")
            return None
    
    def update_user(self, user_id: int, first_name: str = None, last_name: str = None, 
                    email: str = None, access_level: str = None) -> bool:
        """Update user information."""
        try:
            # Get current user data
            current_user = self.select_user_by_id(user_id)
            if not current_user:
                return False
            
            # Update with new values or keep current ones
            first_name = first_name if first_name is not None else current_user['firstName']
            last_name = last_name if last_name is not None else current_user['lastName']
            email = email if email is not None else current_user['email']
            access_level = access_level if access_level is not None else current_user['accessLevel']
            
            query = """
            UPDATE User 
            SET firstName = %s, lastName = %s, email = %s, accessLevel = %s
            WHERE userId = %s
            """
            values = (first_name, last_name, email, access_level, user_id)
            self.cursor.execute(query, values)
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                print(f"User with ID {user_id} updated successfully!")
                return True
            else:
                print(f"No changes made to user with ID {user_id}")
                return False
        except mysql.connector.Error as err:
            print(f"Error updating user: {err}")
            return False
    
    def update_login(self, user_id: int, username: str = None, password: str = None) -> bool:
        """Update login information."""
        try:
            # Build the query dynamically based on what's being updated
            query_parts = []
            values = []
            
            if username is not None:
                query_parts.append("username = %s")
                values.append(username)
            
            if password is not None:
                query_parts.append("password = %s")
                hashed_password = self._encrypt_password(password)
                values.append(hashed_password)
            
            if not query_parts:
                print("No updates specified for login")
                return False
            
            # Complete the query
            query = f"UPDATE Login SET {', '.join(query_parts)} WHERE userId = %s"
            values.append(user_id)
            
            self.cursor.execute(query, values)
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                print(f"Login information for user ID {user_id} updated successfully!")
                return True
            else:
                print(f"No changes made to login for user ID {user_id}")
                return False
        except mysql.connector.Error as err:
            print(f"Error updating login: {err}")
            return False
    
    def delete_user(self, user_id: int) -> bool:
        """Delete a user (will cascade delete their login due to constraints)."""
        try:
            query = "DELETE FROM User WHERE userId = %s"
            self.cursor.execute(query, (user_id,))
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                print(f"User with ID {user_id} deleted successfully!")
                return True
            else:
                print(f"No user found with ID {user_id}")
                return False
        except mysql.connector.Error as err:
            print(f"Error deleting user: {err}")
            return False
    
    def delete_login(self, login_id: int) -> bool:
        """Delete a login record by login ID."""
        try:
            query = "DELETE FROM Login WHERE loginId = %s"
            self.cursor.execute(query, (login_id,))
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                print(f"Login with ID {login_id} deleted successfully!")
                return True
            else:
                print(f"No login found with ID {login_id}")
                return False
        except mysql.connector.Error as err:
            print(f"Error deleting login: {err}")
            return False
    
    def close_connection(self):
        """Close database connection."""
        if self.connection:
            if self.cursor:
                self.cursor.close()
            self.connection.close()
            print("Database connection closed.")


def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_menu():
    """Display the main menu."""
    print("\n===== User and Login Management System =====")
    print("1. Add new user and login")
    print("2. View all users")
    print("3. Find user by ID")
    print("4. Find login by username")
    print("5. Update user information")
    print("6. Update login information")
    print("7. Delete user")
    print("8. Delete login")
    print("9. Exit")
    return input("Enter your choice (1-9): ")


def get_user_input() -> Dict:
    """Get user information from command line."""
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    email = input("Enter email address: ")
    
    while True:
        access_level = input("Enter access level (basic/admin): ").lower()
        if access_level in ['basic', 'admin']:
            break
        print("Invalid access level. Please enter 'basic' or 'admin'.")
    
    return {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'access_level': access_level
    }


def get_login_input() -> Dict:
    """Get login information from command line."""
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    return {
        'username': username,
        'password': password
    }


def main():
    """Main function to run the database management system."""
    # Get MySQL password
    mysql_password = getpass("Enter your MySQL root password: ")
    
    # Initialize database manager
    db_manager = DatabaseManager()
    
    # Connect to MySQL
    if not db_manager.connect_to_mysql(mysql_password):
        print("Failed to connect to MySQL. Exiting...")
        return
    
    # Get database name components
    first_initial = input("Enter your first initial: ")
    last_name = input("Enter your last name: ")
    purpose = input("Enter database purpose (e.g., 'Logins'): ")
    
    # Create database
    if not db_manager.create_database(first_initial, last_name, purpose):
        print("Failed to create database. Exiting...")
        db_manager.close_connection()
        return
    
    # Create tables
    if not db_manager.create_tables():
        print("Failed to create tables. Exiting...")
        db_manager.close_connection()
        return
    
    # Main program loop
    while True:
        choice = display_menu()
        
        if choice == '1':  # Add new user and login
            clear_screen()
            print("\n=== Add New User and Login ===")
            user_data = get_user_input()
            user_id = db_manager.insert_user(
                user_data['first_name'],
                user_data['last_name'],
                user_data['email'],
                user_data['access_level']
            )
            
            if user_id:
                login_data = get_login_input()
                db_manager.insert_login(
                    user_id,
                    login_data['username'],
                    login_data['password']
                )
        
        elif choice == '2':  # View all users
            clear_screen()
            print("\n=== All Users ===")
            users = db_manager.select_all_users()
            if users:
                print(f"{'ID':<5} {'First Name':<15} {'Last Name':<15} {'Email':<30} {'Access Level':<10}")
                print("-" * 75)
                for user in users:
                    print(f"{user['userId']:<5} {user['firstName']:<15} {user['lastName']:<15} {user['email']:<30} {user['accessLevel']:<10}")
            else:
                print("No users found.")
            input("\nPress Enter to continue...")
        
        elif choice == '3':  # Find user by ID
            clear_screen()
            print("\n=== Find User by ID ===")
            try:
                user_id = int(input("Enter user ID: "))
                user = db_manager.select_user_by_id(user_id)
                if user:
                    print(f"\nUser ID: {user['userId']}")
                    print(f"Name: {user['firstName']} {user['lastName']}")
                    print(f"Email: {user['email']}")
                    print(f"Access Level: {user['accessLevel']}")
            except ValueError:
                print("Invalid ID. Please enter a number.")
            input("\nPress Enter to continue...")
        
        elif choice == '4':  # Find login by username
            clear_screen()
            print("\n=== Find Login by Username ===")
            username = input("Enter username: ")
            login = db_manager.select_login_by_username(username)
            if login:
                print(f"\nLogin ID: {login['loginId']}")
                print(f"User ID: {login['userId']}")
                print(f"Username: {login['username']}")
                print(f"Name: {login['firstName']} {login['lastName']}")
                print(f"Email: {login['email']}")
                print(f"Access Level: {login['accessLevel']}")
                # Password is not displayed for security reasons
            input("\nPress Enter to continue...")
        
        elif choice == '5':  # Update user information
            clear_screen()
            print("\n=== Update User Information ===")
            try:
                user_id = int(input("Enter user ID to update: "))
                user = db_manager.select_user_by_id(user_id)
                if user:
                    print("\nLeave field empty to keep current value.")
                    first_name = input(f"First name [{user['firstName']}]: ") or None
                    last_name = input(f"Last name [{user['lastName']}]: ") or None
                    email = input(f"Email [{user['email']}]: ") or None
                    
                    access_level = None
                    access_input = input(f"Access level (basic/admin) [{user['accessLevel']}]: ")
                    if access_input and access_input.lower() in ['basic', 'admin']:
                        access_level = access_input.lower()
                    
                    db_manager.update_user(
                        user_id, first_name, last_name, email, access_level
                    )
            except ValueError:
                print("Invalid ID. Please enter a number.")
            input("\nPress Enter to continue...")
        
        elif choice == '6':  # Update login information
            clear_screen()
            print("\n=== Update Login Information ===")
            try:
                user_id = int(input("Enter user ID for login update: "))
                username = input("New username (leave empty to keep current): ") or None
                password = None
                if input("Change password? (y/n): ").lower() == 'y':
                    password = getpass("New password: ")
                
                db_manager.update_login(user_id, username, password)
            except ValueError:
                print("Invalid ID. Please enter a number.")
            input("\nPress Enter to continue...")
        
        elif choice == '7':  # Delete user
            clear_screen()
            print("\n=== Delete User ===")
            try:
                user_id = int(input("Enter user ID to delete: "))
                if input(f"Are you sure you want to delete user ID {user_id}? This will also delete login info (y/n): ").lower() == 'y':
                    db_manager.delete_user(user_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
            input("\nPress Enter to continue...")
        
        elif choice == '8':  # Delete login
            clear_screen()
            print("\n=== Delete Login ===")
            try:
                login_id = int(input("Enter login ID to delete: "))
                if input(f"Are you sure you want to delete login ID {login_id}? (y/n): ").lower() == 'y':
                    db_manager.delete_login(login_id)
            except ValueError:
                print("Invalid ID. Please enter a number.")
            input("\nPress Enter to continue...")
        
        elif choice == '9':  # Exit
            db_manager.close_connection()
            print("Thank you for using the User Management System. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()