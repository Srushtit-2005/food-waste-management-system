import heapq
import datetime
from collections import defaultdict


class FoodWasteManagement:
    def __init__(self, expiration_warning_days=3):  # Custom expiration warning
        self.inventory = {}  # Dictionary to store food items, quantities, and expiration dates
        self.expired_items = []  # Min-heap to track expired food items by expiration date
        self.waste_records = []  # Stack or list to record waste entries
        self.usage_history = defaultdict(list)  # Dictionary to store food usage history
        self.expiration_warning_days = expiration_warning_days  # Default expiration warning period

    def add_food(self, food_name, quantity, expiration_date):
        # Add a food item to the inventory
        expiration_date = datetime.datetime.strptime(expiration_date, '%Y-%m-%d')
        self.inventory[food_name] = {
            'quantity': quantity,
            'expiration_date': expiration_date
        }
        heapq.heappush(self.expired_items, (expiration_date, food_name))  # Add to the heap for expiration tracking
        print(f"Added {food_name} (Quantity: {quantity}, Expiration: {expiration_date.date()}) to inventory.")

    def track_usage(self, food_name, quantity_used):
        # Track usage of a food item and update inventory
        if food_name in self.inventory and self.inventory[food_name]['quantity'] >= quantity_used:
            self.inventory[food_name]['quantity'] -= quantity_used
            self.usage_history[food_name].append({
                'date': datetime.datetime.now(),
                'quantity_used': quantity_used
            })
            print(f"Used {quantity_used} units of {food_name}.")
        else:
            print(f"Error: Not enough {food_name} in inventory.")

    def record_waste(self, food_name, quantity_wasted, reason):
        # Record food waste
        if food_name in self.inventory:
            self.inventory[food_name]['quantity'] -= quantity_wasted
            waste_entry = {
                'food_name': food_name,
                'quantity_wasted': quantity_wasted,
                'reason': reason,
                'timestamp': datetime.datetime.now()
            }
            self.waste_records.append(waste_entry)
            print(f"Recorded waste: {quantity_wasted} units of {food_name} due to {reason}.")
        else:
            print(f"Error: {food_name} not found in inventory.")

    def monitor_expirations(self):
        # Identify and notify about food items close to expiration
        current_date = datetime.datetime.now()
        warning_date = current_date + datetime.timedelta(days=self.expiration_warning_days)
        expiring_soon = []

        while self.expired_items and self.expired_items[0][0] <= warning_date:
            expiration_date, food_name = heapq.heappop(self.expired_items)
            if food_name in self.inventory and self.inventory[food_name]['expiration_date'] <= warning_date:
                expiring_soon.append((food_name, expiration_date.date()))

        if expiring_soon:
            print("Food items expiring soon:")
            for food, exp_date in expiring_soon:
                print(f"- {food} (Expiration: {exp_date})")
        else:
            print("No food items expiring soon.")

    def suggest_donation(self):
        # Suggest donating food that is close to expiration
        current_date = datetime.datetime.now()
        donation_candidates = [
            food for food, details in self.inventory.items()
            if 0 < (details['expiration_date'] - current_date).days <= self.expiration_warning_days
        ]

        if donation_candidates:
            print("Consider donating the following items nearing expiration:")
            for food in donation_candidates:
                print(f"- {food} (Expires in {(self.inventory[food]['expiration_date'] - current_date).days} days)")
        else:
            print("No items need donation at this time.")

    def generate_report(self):
        # Generate a waste report based on food wasted
        print("\nWaste Report:")
        for record in self.waste_records:
            print(f"Food: {record['food_name']}, Quantity Wasted: {record['quantity_wasted']}, Reason: {record['reason']}, Time: {record['timestamp']}")

        total_waste = defaultdict(int)
        for record in self.waste_records:
            total_waste[record['food_name']] += record['quantity_wasted']

        print("\nTotal Food Wasted by Category:")
        for food, waste in total_waste.items():
            print(f"{food}: {waste} units")
    def display_inventory(self):
        """
        Displays the current inventory with quantities and expiration dates.
        """
        print("\n--- Current Inventory ---")
        if not self.inventory:
            print("Inventory is empty.")
        else:
            for food, details in self.inventory.items():
                print(f"{food}: {details['quantity']} units (Expires on {details['expiration_date'].date()})")

# Example usage
if __name__ == "__main__":
    system = FoodWasteManagement(expiration_warning_days=5)  # Custom expiration warning

    while True:
        print("\n--- Food Waste Management System ---")
        print("1. Add Food Item")
        print("2. Track Usage")
        print("3. Record Waste")
        print("4. Monitor Expirations")
        print("5. Suggest Donation")
        print("6. Generate Report")
        print("7. Display Inventory")
        print("8.exit")
        
        choice = input("Enter your choice: ")
        if choice == "1":
            name = input("Enter food name: ")
            quantity = int(input("Enter quantity: "))
            expiration_date = input("Enter expiration date (YYYY-MM-DD): ")
            system.add_food(name, quantity, expiration_date)
        elif choice == "2":
            name = input("Enter food name: ")
            quantity_used = int(input("Enter quantity used: "))
            system.track_usage(name, quantity_used)
        elif choice == "3":
            name = input("Enter food name: ")
            quantity_wasted = int(input("Enter quantity wasted: "))
            reason = input("Enter reason for waste: ")
            system.record_waste(name, quantity_wasted, reason)
        elif choice == "4":
            system.monitor_expirations()
        elif choice == "5":
            system.suggest_donation()
        elif choice == "6":
            system.generate_report()
        elif choice == "7":
            system.display_inventory()
        elif choice == "8":
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again.")
