import csv
import matplotlib.pyplot as plt

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)

    def manage_passengers(self):
        print("Admin: Manage Passengers")
        self._manage_passengers()

    def update_trip_legs(self):
        print("Admin: Update Trip Legs")
        # Add logic for updating trip legs here
        trip_legs = self._load_trip_legs()
        if not trip_legs:
            print("No trip legs available.")
            return

        print("Current trip legs:")
        self._print_trip_legs(trip_legs)

        # Update trip legs
        leg_to_update = input("Enter the index of the trip leg to update: ")
        if leg_to_update.isdigit() and 0 <= int(leg_to_update) < len(trip_legs):
            trip_leg = trip_legs[int(leg_to_update)]
            trip_leg["source"] = input("Enter source: ")
            trip_leg["destination"] = input("Enter destination: ")
            trip_leg["departure_time"] = input("Enter departure time: ")
            trip_leg["arrival_time"] = input("Enter arrival time: ")
            trip_legs[int(leg_to_update)] = trip_leg
            self._save_trip_legs(trip_legs)
            print("Trip leg updated successfully.")
        else:
            print("Invalid trip leg index.")

    def _load_trip_legs(self):
        trip_legs = []
        try:
            with open("trip_legs.csv", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    trip_legs.append(row)
        except FileNotFoundError:
            pass
        return trip_legs

    def _save_trip_legs(self, trip_legs):
        with open("trip_legs.csv", "w", newline="") as file:
            fieldnames = ["source", "destination", "departure_time", "arrival_time"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(trip_legs)

    def _print_trip_legs(self, trip_legs):
        for i, leg in enumerate(trip_legs):
            print(
                f"{i}: Source: {leg['source']}, Destination: {leg['destination']}, Departure Time: {leg['departure_time']}, Arrival Time: {leg['arrival_time']}")

    def _manage_passengers(self):
        while True:
            action = input("Choose action: create/view/update/delete (or 'exit' to return): ").lower()

            if action == "create":
                self.create_passenger()
            elif action == "view":
                self.view_passengers()
            elif action == "update":
                self.update_passenger()
            elif action == "delete":
                self.delete_passenger()
            elif action == "exit":
                break
            else:
                print("Invalid action.")

    def create_passenger(self):
        print("Creating passenger profile")
        name = input("Enter name: ")
        address = input("Enter address: ")
        dob = input("Enter date of birth (YYYY-MM-DD): ")
        contact = input("Enter contact number: ")

        with open("passengers.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, address, dob, contact])
        print("Passenger profile created successfully.")

    def view_passengers(self):
        print("Viewing passenger profiles")
        with open("passengers.csv", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                print("Name:", row[0])
                print("Address:", row[1])
                print("Date of Birth:", row[2])
                print("Contact:", row[3])
                print("")

    def update_passenger(self):
        print("Updating passenger profile")
        name = input("Enter name of the passenger to update: ")
        field_to_update = input("Enter field to update (name/address/dob/contact): ")
        new_value = input(f"Enter new value for {field_to_update}: ")

        field_index = {"name": 0, "address": 1, "dob": 2, "contact": 3}
        with open("passengers.csv", "r") as file:
            reader = csv.reader(file)
            rows = list(reader)

        found = False
        for row in rows:
            if row[0].lower() == name.lower():
                found = True
                row[field_index[field_to_update]] = new_value

        if found:
            with open("passengers.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            print("Passenger profile updated successfully.")
        else:
            print("Passenger not found.")

    def delete_passenger(self):
        print("Deleting passenger profile")
        name = input("Enter name of the passenger to delete: ")

        with open("passengers.csv", "r") as file:
            reader = csv.reader(file)
            rows = list(reader)

        found = False
        for row in rows:
            if row[0].lower() == name.lower():
                found = True
                rows.remove(row)

        if found:
            with open("passengers.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            print("Passenger profile deleted successfully.")
        else:
            print("Passenger not found.")

    def generate_trip_itinerary(self):
        print("Admin: Generate Trip Itinerary")

        # Get trip details
        destinations = input("Enter destinations (comma-separated): ").split(',')
        departure_times = input("Enter departure times (comma-separated): ").split(',')
        durations = input("Enter durations (comma-separated): ").split(',')

        # Check if the number of destinations, departure times, and durations match
        if len(destinations) != len(departure_times) or len(departure_times) != len(durations):
            print("Error: Number of destinations, departure times, and durations must match.")
            return

        # Generate itinerary
        itinerary = []
        for i in range(len(destinations)):
            itinerary.append({
                "destination": destinations[i],
                "departure_time": departure_times[i],
                "duration": durations[i]
            })
        self.save_itinerary_to_csv(itinerary)
        print("Trip itinerary generated successfully.")

    def save_itinerary_to_csv(self, itinerary):
        with open("trip_itinerary.csv", "w", newline="") as file:
            fieldnames = ["destination", "departure_time", "duration"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(itinerary)

    def handle_payments(self):
        print("Admin: Handle Payments")

        # Get payment details
        passenger_name = input("Enter passenger name: ")
        amount = float(input("Enter payment amount: "))
        payment_method = input("Enter payment method: ")
        transaction_id = input("Enter transaction ID: ")

        # Save payment receipt to CSV file
        self.save_receipt_to_csv(passenger_name, amount, payment_method, transaction_id)
        print("Payment handled successfully.")

    def save_receipt_to_csv(self, passenger_name, amount, payment_method, transaction_id):
        with open("payment_receipts.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([passenger_name, amount, payment_method, transaction_id])

    def manage_trip_coordinators(self):
        print("Manager: Manage Trip Coordinators")
        action = input("Choose action: create/view/update/delete (or 'exit' to return): ").lower()

        if action == "create":
            self.create_trip_coordinator()
        elif action == "view":
            self.view_trip_coordinators()
        elif action == "update":
            self.update_trip_coordinator()
        elif action == "delete":
            self.delete_trip_coordinator()
        elif action == "exit":
            return
        else:
            print("Invalid action.")

    def create_trip_coordinator(self):
        # Get coordinator details
        name = input("Enter coordinator name: ")
        email = input("Enter coordinator email: ")
        phone = input("Enter coordinator phone: ")

        # Save coordinator to CSV file
        with open("trip_coordinators.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, email, phone])
        print("Trip coordinator created successfully.")

    def view_trip_coordinators(self):
        try:
            with open("trip_coordinators.csv", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    print("Name:", row[0])
                    print("Email:", row[1])
                    print("Phone:", row[2])
                    print()
        except FileNotFoundError:
            print("No trip coordinators found.")

    def update_trip_coordinator(self):
        name_to_update = input("Enter the name of the coordinator to update: ")
        try:
            with open("trip_coordinators.csv", newline="") as file:
                reader = csv.reader(file)
                coordinators = list(reader)
                for i, row in enumerate(coordinators):
                    if row[0] == name_to_update:
                        # Get updated details
                        email = input("Enter coordinator email: ")
                        phone = input("Enter coordinator phone: ")

                        # Update coordinator details
                        coordinators[i][1] = email
                        coordinators[i][2] = phone

                        # Rewrite CSV file with updated details
                        with open("trip_coordinators.csv", "w", newline="") as file:
                            writer = csv.writer(file)
                            writer.writerows(coordinators)
                        print("Trip coordinator updated successfully.")
                        return
                print("Coordinator not found.")
        except FileNotFoundError:
            print("No trip coordinators found.")

    def delete_trip_coordinator(self):
        name_to_delete = input("Enter the name of the coordinator to delete: ")
        try:
            with open("trip_coordinators.csv", newline="") as file:
                reader = csv.reader(file)
                coordinators = list(reader)
                for i, row in enumerate(coordinators):
                    if row[0] == name_to_delete:
                        del coordinators[i]
                        # Rewrite CSV file without the deleted coordinator
                        with open("trip_coordinators.csv", "w", newline="") as file:
                            writer = csv.writer(file)
                            writer.writerows(coordinators)
                        print("Trip coordinator deleted successfully.")
                        return
                print("Coordinator not found.")
        except FileNotFoundError:
            print("No trip coordinators found.")

    def generate_total_invoices(self):
        print("Manager: Generate Total Invoices")

        # Read trip information from CSV
        trips = self._load_trips()

        # Calculate total invoices
        total_invoices = {}
        for trip in trips:
            trip_id = trip["trip_id"]
            price_per_passenger = float(trip["price_per_passenger"])
            num_passengers = int(trip["num_passengers"])
            total_invoice = price_per_passenger * num_passengers
            total_invoices[trip_id] = total_invoice

            # Print total invoices
            for trip_id, total_invoice in total_invoices.items():
                print(f"Trip ID: {trip_id}, Total Invoice: {total_invoice}")

    def _load_trips(self):
        trips = []
        try:
            with open("trips.csv", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    trips.append(row)
        except FileNotFoundError:
            print("No trips found.")
        return trips

    def manage_trip_managers(self):
        print("Admin: Manage Trip Managers")
        action = input("Choose action: create/view/update/delete (or 'exit' to return): ").lower()

        if action == "create":
            self.create_trip_manager()
        elif action == "view":
            self.view_trip_managers()
        elif action == "update":
            self.update_trip_manager()
        elif action == "delete":
            self.delete_trip_manager()
        elif action == "exit":
            return
        else:
            print("Invalid action.")

    def create_trip_manager(self):
        # Get manager details
        name = input("Enter manager name: ")
        email = input("Enter manager email: ")
        phone = input("Enter manager phone: ")

        # Save manager to CSV file
        with open("trip_managers.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, email, phone])
        print("Trip manager created successfully.")

    def view_trip_managers(self):
        try:
            with open("trip_managers.csv", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    print("Name:", row[0])
                    print("Email:", row[1])
                    print("Phone:", row[2])
                    print()
        except FileNotFoundError:
            print("No trip managers found.")

    def update_trip_manager(self):
        name_to_update = input("Enter the name of the manager to update: ")
        try:
            with open("trip_managers.csv", newline="") as file:
                reader = csv.reader(file)
                managers = list(reader)
                for i, row in enumerate(managers):
                    if row[0] == name_to_update:
                        # Get updated details
                        email = input("Enter manager email: ")
                        phone = input("Enter manager phone: ")

                        # Update manager details
                        managers[i][1] = email
                        managers[i][2] = phone

                        # Rewrite CSV file with updated details
                        with open("trip_managers.csv", "w", newline="") as file:
                            writer = csv.writer(file)
                            writer.writerows(managers)
                        print("Trip manager updated successfully.")
                        return
                print("Manager not found.")
        except FileNotFoundError:
            print("No trip managers found.")

    def delete_trip_manager(self):
        name_to_delete = input("Enter the name of the manager to delete: ")
        try:
            with open("trip_managers.csv", newline="") as file:
                reader = csv.reader(file)
                managers = list(reader)
                for i, row in enumerate(managers):
                    if row[0] == name_to_delete:
                        del managers[i]
                        # Rewrite CSV file without the deleted manager
                        with open("trip_managers.csv", "w", newline="") as file:
                            writer = csv.writer(file)
                            writer.writerows(managers)
                        print("Trip manager deleted successfully.")
                        return
                print("Manager not found.")
        except FileNotFoundError:
            print("No trip managers found.")

    def manage_trip_invoices_and_payments(self):
        print("Admin: Manage Trip Invoices and Payments")
        action = input("Choose action: view/update/delete (or 'exit' to return): ").lower()

        if action == "view":
            self.view_trip_invoices_and_payments()
        elif action == "update":
            self.update_trip_invoices_and_payments()
        elif action == "delete":
            self.delete_trip_invoices_and_payments()
        elif action == "exit":
            return
        else:
            print("Invalid action.")

    def view_trip_invoices_and_payments(self):
        try:
            # View trip invoices
            print("Trip Invoices:")
            with open("trip_invoices.csv", newline="") as invoice_file:
                reader = csv.reader(invoice_file)
                for row in reader:
                    print("Trip ID:", row[0])
                    print("Total Invoice:", row[1])
                    print()

            # View trip payments
            print("Trip Payments:")
            with open("trip_payments.csv", newline="") as payment_file:
                reader = csv.reader(payment_file)
                for row in reader:
                    print("Trip ID:", row[0])
                    print("Payment Amount:", row[1])
                    print("Payment Method:", row[2])
                    print("Transaction ID:", row[3])
                    print()
        except FileNotFoundError:
            print("No trip invoices or payments found.")

    def update_trip_invoices_and_payments(self):
        try:
            # Update trip invoices
            trip_id = input("Enter the trip ID to update invoice: ")
            new_invoice = input("Enter the new total invoice amount: ")
            with open("trip_invoices.csv", "r", newline="") as invoice_file:
                reader = csv.reader(invoice_file)
                invoices = list(reader)
            with open("trip_invoices.csv", "w", newline="") as invoice_file:
                writer = csv.writer(invoice_file)
                for invoice in invoices:
                    if invoice[0] == trip_id:
                        invoice[1] = new_invoice
                    writer.writerow(invoice)

            # Update trip payments
            payment_info = []
            with open("trip_payments.csv", "r", newline="") as payment_file:
                reader = csv.reader(payment_file)
                for row in reader:
                    if row[0] == trip_id:
                        payment_info.append(row)
            if payment_info:
                print("Trip Payments:")
                for payment in payment_info:
                    print("Payment Amount:", payment[1])
                    print("Payment Method:", payment[2])
                    print("Transaction ID:", payment[3])
                print("Enter new payment details:")
                new_amount = input("Enter new payment amount: ")
                new_method = input("Enter new payment method: ")
                new_transaction_id = input("Enter new transaction ID: ")
                with open("trip_payments.csv", "w", newline="") as payment_file:
                    writer = csv.writer(payment_file)
                    for payment in payment_info:
                        if payment[0] == trip_id:
                            payment[1] = new_amount
                            payment[2] = new_method
                            payment[3] = new_transaction_id
                        writer.writerow(payment)
            print("Trip invoices and payments updated successfully.")
        except FileNotFoundError:
            print("No trip invoices or payments found.")

    def delete_trip_invoices_and_payments(self):
        try:
            trip_id = input("Enter the trip ID to delete invoices and payments: ")
            with open("trip_invoices.csv", "r", newline="") as invoice_file:
                reader = csv.reader(invoice_file)
                invoices = [invoice for invoice in reader if invoice[0] != trip_id]
            with open("trip_invoices.csv", "w", newline="") as invoice_file:
                writer = csv.writer(invoice_file)
                writer.writerows(invoices)

            with open("trip_payments.csv", "r", newline="") as payment_file:
                reader = csv.reader(payment_file)
                payments = [payment for payment in reader if payment[0] != trip_id]
            with open("trip_payments.csv", "w", newline="") as payment_file:
                writer = csv.writer(payment_file)
                writer.writerows(payments)
            print("Trip invoices and payments deleted successfully.")
        except FileNotFoundError:
            print("No trip invoices or payments found.")

    def generate_reports(self):
        print("Admin: Generate Reports")
        action = input("Choose action: passenger (or 'exit' to return): ").lower()

        if action == "passenger":
            self.generate_passenger_report()
        elif action == "exit":
            return
        else:
            print("Invalid action.")

    def generate_passenger_report(self):
        try:
            # Load passenger data from CSV
            with open("passengers.csv", newline="") as file:
                reader = csv.DictReader(file)
                passenger_data = list(reader)

            # Extract relevant information
            passenger_names = [passenger["Name"] for passenger in passenger_data]
            ages = [int(passenger["Age"]) for passenger in passenger_data]

            # Generate a bar chart
            plt.bar(passenger_names, ages)
            plt.xlabel("Passenger Name")
            plt.ylabel("Age")
            plt.title("Passenger Age Distribution")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            plt.show()

        except FileNotFoundError:
            print("Passenger data not found.")



class Manager(User):
    def __init__(self, username, password):
        super().__init__(username, password)

    def manage_passengers(self):
        print("Manager: Manage Passengers")
        self._manage_passengers()

    def update_trip_legs(self):
        print("Admin: Update Trip Legs")
        # Add logic for updating trip legs here
        trip_legs = self._load_trip_legs()
        if not trip_legs:
            print("No trip legs available.")
            return

        print("Current trip legs:")
        self._print_trip_legs(trip_legs)

        # Update trip legs
        leg_to_update = input("Enter the index of the trip leg to update: ")
        if leg_to_update.isdigit() and 0 <= int(leg_to_update) < len(trip_legs):
            trip_leg = trip_legs[int(leg_to_update)]
            trip_leg["source"] = input("Enter source: ")
            trip_leg["destination"] = input("Enter destination: ")
            trip_leg["departure_time"] = input("Enter departure time: ")
            trip_leg["arrival_time"] = input("Enter arrival time: ")
            trip_legs[int(leg_to_update)] = trip_leg
            self._save_trip_legs(trip_legs)
            print("Trip leg updated successfully.")
        else:
            print("Invalid trip leg index.")

    def _load_trip_legs(self):
        trip_legs = []
        try:
            with open("trip_legs.csv", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    trip_legs.append(row)
        except FileNotFoundError:
            pass
        return trip_legs

    def _save_trip_legs(self, trip_legs):
        with open("trip_legs.csv", "w", newline="") as file:
            fieldnames = ["source", "destination", "departure_time", "arrival_time"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(trip_legs)

    def _print_trip_legs(self, trip_legs):
        for i, leg in enumerate(trip_legs):
            print(
                f"{i}: Source: {leg['source']}, Destination: {leg['destination']}, Departure Time: {leg['departure_time']}, Arrival Time: {leg['arrival_time']}")

    def _manage_passengers(self):
        while True:
            action = input("Choose action: create/view/update/delete (or 'exit' to return): ").lower()

            if action == "create":
                self.create_passenger()
            elif action == "view":
                self.view_passengers()
            elif action == "update":
                self.update_passenger()
            elif action == "delete":
                self.delete_passenger()
            elif action == "exit":
                break
            else:
                print("Invalid action.")

    def create_passenger(self):
        print("Creating passenger profile")
        name = input("Enter name: ")
        address = input("Enter address: ")
        dob = input("Enter date of birth (YYYY-MM-DD): ")
        contact = input("Enter contact number: ")

        with open("passengers.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, address, dob, contact])
        print("Passenger profile created successfully.")

    def view_passengers(self):
        print("Viewing passenger profiles")
        with open("passengers.csv", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                print("Name:", row[0])
                print("Address:", row[1])
                print("Date of Birth:", row[2])
                print("Contact:", row[3])
                print("")

    def update_passenger(self):
        print("Updating passenger profile")
        name = input("Enter name of the passenger to update: ")
        field_to_update = input("Enter field to update (name/address/dob/contact): ")
        new_value = input(f"Enter new value for {field_to_update}: ")

        field_index = {"name": 0, "address": 1, "dob": 2, "contact": 3}
        with open("passengers.csv", "r") as file:
            reader = csv.reader(file)
            rows = list(reader)

        found = False
        for row in rows:
            if row[0].lower() == name.lower():
                found = True
                row[field_index[field_to_update]] = new_value

        if found:
            with open("passengers.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            print("Passenger profile updated successfully.")
        else:
            print("Passenger not found.")

    def delete_passenger(self):
        print("Deleting passenger profile")
        name = input("Enter name of the passenger to delete: ")

        with open("passengers.csv", "r") as file:
            reader = csv.reader(file)
            rows = list(reader)

        found = False
        for row in rows:
            if row[0].lower() == name.lower():
                found = True
                rows.remove(row)

        if found:
            with open("passengers.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            print("Passenger profile deleted successfully.")
        else:
            print("Passenger not found.")

    def generate_trip_itinerary(self):
        print("Admin: Generate Trip Itinerary")

        # Get trip details
        destinations = input("Enter destinations (comma-separated): ").split(',')
        departure_times = input("Enter departure times (comma-separated): ").split(',')
        durations = input("Enter durations (comma-separated): ").split(',')

        # Check if the number of destinations, departure times, and durations match
        if len(destinations) != len(departure_times) or len(departure_times) != len(durations):
            print("Error: Number of destinations, departure times, and durations must match.")
            return

        # Generate itinerary
        itinerary = []
        for i in range(len(destinations)):
            itinerary.append({
                "destination": destinations[i],
                "departure_time": departure_times[i],
                "duration": durations[i]
            })
        self.save_itinerary_to_csv(itinerary)
        print("Trip itinerary generated successfully.")

    def save_itinerary_to_csv(self, itinerary):
        with open("trip_itinerary.csv", "w", newline="") as file:
            fieldnames = ["destination", "departure_time", "duration"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(itinerary)

    def handle_payments(self):
        print("Admin: Handle Payments")

        # Get payment details
        passenger_name = input("Enter passenger name: ")
        amount = float(input("Enter payment amount: "))
        payment_method = input("Enter payment method: ")
        transaction_id = input("Enter transaction ID: ")

        # Save payment receipt to CSV file
        self.save_receipt_to_csv(passenger_name, amount, payment_method, transaction_id)
        print("Payment handled successfully.")

    def save_receipt_to_csv(self, passenger_name, amount, payment_method, transaction_id):
        with open("payment_receipts.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([passenger_name, amount, payment_method, transaction_id])


    def manage_trip_coordinators(self):
        print("Manager: Manage Trip Coordinators")
        action = input("Choose action: create/view/update/delete (or 'exit' to return): ").lower()

        if action == "create":
            self.create_trip_coordinator()
        elif action == "view":
            self.view_trip_coordinators()
        elif action == "update":
            self.update_trip_coordinator()
        elif action == "delete":
            self.delete_trip_coordinator()
        elif action == "exit":
            return
        else:
            print("Invalid action.")

    def create_trip_coordinator(self):
        # Get coordinator details
        name = input("Enter coordinator name: ")
        email = input("Enter coordinator email: ")
        phone = input("Enter coordinator phone: ")

        # Save coordinator to CSV file
        with open("trip_coordinators.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, email, phone])
        print("Trip coordinator created successfully.")

    def view_trip_coordinators(self):
        try:
            with open("trip_coordinators.csv", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    print("Name:", row[0])
                    print("Email:", row[1])
                    print("Phone:", row[2])
                    print()
        except FileNotFoundError:
            print("No trip coordinators found.")

    def update_trip_coordinator(self):
        name_to_update = input("Enter the name of the coordinator to update: ")
        try:
            with open("trip_coordinators.csv", newline="") as file:
                reader = csv.reader(file)
                coordinators = list(reader)
                for i, row in enumerate(coordinators):
                    if row[0] == name_to_update:
                        # Get updated details
                        email = input("Enter coordinator email: ")
                        phone = input("Enter coordinator phone: ")

                        # Update coordinator details
                        coordinators[i][1] = email
                        coordinators[i][2] = phone

                        # Rewrite CSV file with updated details
                        with open("trip_coordinators.csv", "w", newline="") as file:
                            writer = csv.writer(file)
                            writer.writerows(coordinators)
                        print("Trip coordinator updated successfully.")
                        return
                print("Coordinator not found.")
        except FileNotFoundError:
            print("No trip coordinators found.")

    def delete_trip_coordinator(self):
        name_to_delete = input("Enter the name of the coordinator to delete: ")
        try:
            with open("trip_coordinators.csv", newline="") as file:
                reader = csv.reader(file)
                coordinators = list(reader)
                for i, row in enumerate(coordinators):
                    if row[0] == name_to_delete:
                        del coordinators[i]
                        # Rewrite CSV file without the deleted coordinator
                        with open("trip_coordinators.csv", "w", newline="") as file:
                            writer = csv.writer(file)
                            writer.writerows(coordinators)
                        print("Trip coordinator deleted successfully.")
                        return
                print("Coordinator not found.")
        except FileNotFoundError:
            print("No trip coordinators found.")

    def generate_total_invoices(self):
        print("Manager: Generate Total Invoices")

        # Read trip information from CSV
        trips = self._load_trips()

        # Calculate total invoices
        total_invoices = {}
        for trip in trips:
            trip_id = trip["trip_id"]
            price_per_passenger = float(trip["price_per_passenger"])
            num_passengers = int(trip["num_passengers"])
            total_invoice = price_per_passenger * num_passengers
            total_invoices[trip_id] = total_invoice

            # Print total invoices
            for trip_id, total_invoice in total_invoices.items():
                print(f"Trip ID: {trip_id}, Total Invoice: {total_invoice}")

    def _load_trips(self):
        trips = []
        try:
            with open("trips.csv", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    trips.append(row)
        except FileNotFoundError:
            print("No trips found.")
        return trips

class Coordinator(User):
    def __init__(self, username, password):
        super().__init__(username, password)

    def manage_passengers(self):
        print("Coordinator: Manage Passengers")
        self._manage_passengers()

    def update_trip_legs(self):
        print("Admin: Update Trip Legs")
        # Add logic for updating trip legs here
        trip_legs = self._load_trip_legs()
        if not trip_legs:
            print("No trip legs available.")
            return

        print("Current trip legs:")
        self._print_trip_legs(trip_legs)

        # Update trip legs
        leg_to_update = input("Enter the index of the trip leg to update: ")
        if leg_to_update.isdigit() and 0 <= int(leg_to_update) < len(trip_legs):
            trip_leg = trip_legs[int(leg_to_update)]
            trip_leg["source"] = input("Enter source: ")
            trip_leg["destination"] = input("Enter destination: ")
            trip_leg["departure_time"] = input("Enter departure time: ")
            trip_leg["arrival_time"] = input("Enter arrival time: ")
            trip_legs[int(leg_to_update)] = trip_leg
            self._save_trip_legs(trip_legs)
            print("Trip leg updated successfully.")
        else:
            print("Invalid trip leg index.")

    def _load_trip_legs(self):
        trip_legs = []
        try:
            with open("trip_legs.csv", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    trip_legs.append(row)
        except FileNotFoundError:
            pass
        return trip_legs

    def _save_trip_legs(self, trip_legs):
        with open("trip_legs.csv", "w", newline="") as file:
            fieldnames = ["source", "destination", "departure_time", "arrival_time"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(trip_legs)

    def _print_trip_legs(self, trip_legs):
        for i, leg in enumerate(trip_legs):
            print(
                f"{i}: Source: {leg['source']}, Destination: {leg['destination']}, Departure Time: {leg['departure_time']}, Arrival Time: {leg['arrival_time']}")

    def _manage_passengers(self):
        while True:
            action = input("Choose action: create/view/update/delete (or 'exit' to return): ").lower()

            if action == "create":
                self.create_passenger()
            elif action == "view":
                self.view_passengers()
            elif action == "update":
                self.update_passenger()
            elif action == "delete":
                self.delete_passenger()
            elif action == "exit":
                break
            else:
                print("Invalid action.")

    def create_passenger(self):
        print("Creating passenger profile")
        name = input("Enter name: ")
        address = input("Enter address: ")
        dob = input("Enter date of birth (YYYY-MM-DD): ")
        contact = input("Enter contact number: ")

        with open("passengers.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, address, dob, contact])
        print("Passenger profile created successfully.")

    def view_passengers(self):
        print("Viewing passenger profiles")
        with open("passengers.csv", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                print("Name:", row[0])
                print("Address:", row[1])
                print("Date of Birth:", row[2])
                print("Contact:", row[3])
                print("")

    def update_passenger(self):
        print("Updating passenger profile")
        name = input("Enter name of the passenger to update: ")
        field_to_update = input("Enter field to update (name/address/dob/contact): ")
        new_value = input(f"Enter new value for {field_to_update}: ")

        field_index = {"name": 0, "address": 1, "dob": 2, "contact": 3}
        with open("passengers.csv", "r") as file:
            reader = csv.reader(file)
            rows = list(reader)

        found = False
        for row in rows:
            if row[0].lower() == name.lower():
                found = True
                row[field_index[field_to_update]] = new_value

        if found:
            with open("passengers.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            print("Passenger profile updated successfully.")
        else:
            print("Passenger not found.")

    def delete_passenger(self):
        print("Deleting passenger profile")
        name = input("Enter name of the passenger to delete: ")

        with open("passengers.csv", "r") as file:
            reader = csv.reader(file)
            rows = list(reader)

        found = False
        for row in rows:
            if row[0].lower() == name.lower():
                found = True
                rows.remove(row)

        if found:
            with open("passengers.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)
            print("Passenger profile deleted successfully.")
        else:
            print("Passenger not found.")

    def generate_trip_itinerary(self):
        print("Admin: Generate Trip Itinerary")

        # Get trip details
        destinations = input("Enter destinations (comma-separated): ").split(',')
        departure_times = input("Enter departure times (comma-separated): ").split(',')
        durations = input("Enter durations (comma-separated): ").split(',')

        # Check if the number of destinations, departure times, and durations match
        if len(destinations) != len(departure_times) or len(departure_times) != len(durations):
            print("Error: Number of destinations, departure times, and durations must match.")
            return

        # Generate itinerary
        itinerary = []
        for i in range(len(destinations)):
            itinerary.append({
                "destination": destinations[i],
                "departure_time": departure_times[i],
                "duration": durations[i]
            })
        self.save_itinerary_to_csv(itinerary)
        print("Trip itinerary generated successfully.")

    def save_itinerary_to_csv(self, itinerary):
        with open("trip_itinerary.csv", "w", newline="") as file:
            fieldnames = ["destination", "departure_time", "duration"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(itinerary)

    def handle_payments(self):
        print("Admin: Handle Payments")

        # Get payment details
        passenger_name = input("Enter passenger name: ")
        amount = float(input("Enter payment amount: "))
        payment_method = input("Enter payment method: ")
        transaction_id = input("Enter transaction ID: ")

        # Save payment receipt to CSV file
        self.save_receipt_to_csv(passenger_name, amount, payment_method, transaction_id)
        print("Payment handled successfully.")

    def save_receipt_to_csv(self, passenger_name, amount, payment_method, transaction_id):
        with open("payment_receipts.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([passenger_name, amount, payment_method, transaction_id])


class LoginSystem:
    def __init__(self):
        self.users = {
            "admin": Admin("admin", "admin123"),
            "manager": Manager("manager", "manager123"),
            "coordinator": Coordinator("coordinator", "coordinator123")
        }

    def login(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        user = self.users.get(username)
        if user and user.password == password:
            print(f"Welcome, {username}!")
            return user
        else:
            print("Invalid username or password.")
            return None


def main():
    login_system = LoginSystem()
    user = login_system.login()
    if user:
        user.manage_passengers()
        user.update_trip_legs()
        user.generate_trip_itinerary()
        user.handle_payments()
        if isinstance(user, Admin) or isinstance(user, Manager):
            user.manage_trip_coordinators()
            user.generate_total_invoices()
        if isinstance(user, Admin):
            user.manage_trip_managers()
            user.manage_trip_invoices_and_payments()
            user.generate_reports()

if __name__ == "__main__":
    main()
