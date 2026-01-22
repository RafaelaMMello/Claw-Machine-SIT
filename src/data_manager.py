import csv
import os
from user import User

class DataManager:
    FILE = "users.csv"

    def __init__(self):
        try:
            if not os.path.exists(self.FILE):
                with open(self.FILE, "w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(["name", "password", "points"])

        except Exception as e:
            print(f"Error initializing file: {e}")

    def check_login(self, username, password):
        
        with open(self.FILE, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["name"] == username and row["password"] == password:
                    return User(username)
        return None
    
    def save_user(self, username, password):
        try:
            with open(self.FILE, "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([username, password, 0])

            return True

        except Exception as e:
            print(f"Error saving user: {e}")
            return False

    def load_user(self, name):
        try:
            with open(self.FILE, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["name"] == name:
                        return User(
                            row["name"],
                            int(row["points"])
                        )

            return None  # usuário não encontrado

        except FileNotFoundError:
            return None

        except ValueError:
            print("Error converting points to int")
            return None

        except Exception as e:
            print(f"Error loading user: {e}")
            return None
        
    def update_user_points(self, username, new_points):
        rows = []

        try:
            with open(self.FILE, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["name"] == username:
                        row["points"] = str(new_points)
                    rows.append(row)

            with open(self.FILE, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["name", "password", "points"])
                writer.writeheader()
                writer.writerows(rows)

        except Exception as e:
            print(f"Error updating points: {e}")
