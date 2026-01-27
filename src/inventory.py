import csv
import os

class Inventory:
    FILE = "inventory.csv"

    def __init__(self):
        if not os.path.exists(self.FILE):
            try:
                with open(self.FILE, "w", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    writer.writerow(["username", "prize", "points", "rarity"])
            except Exception as e:
                print(f"Error creating inventory file: {e}")

    def add_item(self, username, prize):
        
        try:
            with open(self.FILE, "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([
                    username,
                    prize.name,
                    prize.points,
                    prize.rarity
                ])
        except Exception as e:
            print(f"Error saving item to inventory: {e}")

    
    def load_inventory(self, username):
        items = []

        try:
            with open(self.FILE, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["username"] == username:
                        items.append({
                            "prize": row["prize"],
                            "points": int(row["points"]),
                            "rarity": row["rarity"]
                        })

        except FileNotFoundError:
            print("Inventory file not found.")

        except Exception as e:
            print(f"Error loading inventory: {e}")

        return items
    
    def total_points(self, username):
        items = self.load_inventory(username)
        total = 0

        for item in items:
            total += item["points"]

        return total
    
    def total_items(self, username):
        return len(self.load_inventory(username))
