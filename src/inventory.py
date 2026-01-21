class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, prize):
        self.items.append(prize)

    def list_items(self):
        return self.items
