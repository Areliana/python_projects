class Location:
    def __init__(self, name, risk_factor, status):
        self.name = name
        self.risk_factor = risk_factor
        self.status = status

    def __str__(self):
        return f"Location: {self.name} | Risk Factor: {self.risk_factor} | Status: {self.status}"


class SafetyMonitor:
    def __init__(self):
        self.locations = []

    def add_location(self, location):
        self.locations.append(location)

    def display_locations(self):
        print("\n===== Safety Monitoring Report =====")
        for location in self.locations:
            print(location)


# Create the SafetyMonitor object
monitor = SafetyMonitor()

# Create Location objects
location1 = Location("Yaounde", 40, "Safe")
location2 = Location("Douala", 55, "Warning")
location3 = Location("Bamenda", 85, "Danger")
location3 = Location("Buea", 90, "Danger")
location3 = Location("Bafoussam", 65, "Danger")
location3 = Location("Kribi", 75, "Danger")

# Add locations to the monitor
monitor.add_location(location1)
monitor.add_location(location2)
monitor.add_location(location3)

# Display all locations
monitor.display_locations()