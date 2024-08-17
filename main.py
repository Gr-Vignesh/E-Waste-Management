import datetime
import json

class EWasteItem:
    def __init__(self, name, purchase_date, expected_lifetime):
        self.name = name
        self.purchase_date = datetime.datetime.strptime(purchase_date, "%Y-%m-%d")
        self.expected_lifetime = expected_lifetime 
        self.replacement_date = self.calculate_replacement_date()

    def calculate_replacement_date(self):
        return self.purchase_date + datetime.timedelta(days=self.expected_lifetime * 365)

    def is_due_for_replacement(self):
        return datetime.datetime.now() >= self.replacement_date

    def days_until_replacement(self):
        return (self.replacement_date - datetime.datetime.now()).days

    def to_dict(self):
        return {
            "name": self.name,
            "purchase_date": self.purchase_date.strftime("%Y-%m-%d"),
            "expected_lifetime": self.expected_lifetime,
            "replacement_date": self.replacement_date.strftime("%Y-%m-%d"),
            "due_for_replacement": self.is_due_for_replacement()
        }


class EWasteManagementSystem:
    def __init__(self):
        self.items = []

    def add_item(self, name, purchase_date, expected_lifetime):
        item = EWasteItem(name, purchase_date, expected_lifetime)
        self.items.append(item)
        print(f"Item '{name}' added successfully.")

    def monitor_items(self):
        due_for_replacement = [item for item in self.items if item.is_due_for_replacement()]
        return due_for_replacement

    def recycle_item(self, name):
        self.items = [item for item in self.items if item.name != name]
        print(f"Item '{name}' recycled successfully.")

    def save_data(self, filename="ewaste_data.json"):
        data = [item.to_dict() for item in self.items]
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {filename}.")

    def load_data(self, filename="ewaste_data.json"):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            self.items = [EWasteItem(**item) for item in data]
            print(f"Data loaded from {filename}.")
        except FileNotFoundError:
            print(f"File {filename} not found. Starting with an empty system.")


if __name__ == "__main__":
    system = EWasteManagementSystem()
    system.load_data()


    system.add_item("Laptop", "2022-01-01", 3)
    system.add_item("Smartphone", "2023-06-15", 2)

    due_items = system.monitor_items()
    if due_items:
        print("\nItems due for replacement:")
        for item in due_items:
            print(f"- {item.name}, replace by {item.replacement_date.strftime('%Y-%m-%d')}")
    else:
        print("\nNo items due for replacement.")

    system.recycle_item("Laptop")
    system.save_data()
