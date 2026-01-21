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

    # def user_exists(self, name):
    #     try:
    #         with open(self.FILE, "r", newline="", encoding="utf-8") as file:
    #             reader = csv.DictReader(file)
    #             return any(row["name"] == name for row in reader)

    #     except FileNotFoundError:
    #         return False

    #     except Exception as e:
    #         print(f"Error checking user: {e}")
    #         return False

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

            return None  # USER NOT FOUND

        except FileNotFoundError:
            return None

        except ValueError:
            print("Error converting points to int")
            return None

        except Exception as e:
            print(f"Error loading user: {e}")
            return None