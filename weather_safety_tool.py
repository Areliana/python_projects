#Global data (visible to all functions) 
RISK_DATA: dict = {
    "yaounde":   45,
    "douala":    52,
    "bafoussam": 28,
    "bertoua":   18,
    "garoua":    39,
    "limbe":     22,
}
RISK_THRESHOLD: int = 40


#Function 1: get the score for a city
def get_score(location: str) -> int:
    """Return crime index for a city, or -1 if unknown."""
    return RISK_DATA.get(location, -1)


#Function 2: Calculate risk for each location 
def get_safety_status(location: str) -> str:
    """Return 'SAFE', 'HIGH RISK', or 'UNKNOWN' for a city."""
    score = get_score(location)
    if score == -1:
        return "UNKNOWN"
    return "HIGH RISK" if score > RISK_THRESHOLD else "SAFE"


#Function 3: collect 5 cities from the user 
def collect_cities() -> list:
    """Ask the user for 5 city names and return them as a list."""
    cities = []
    print("Enter 5 city names:")
    for i in range(5):
        city = input(f"  City #{i + 1}: ").strip().lower()
        cities.append(city)
    return cities


#Function 4: print the risk report
def print_report(cities: list) -> None:
    """Loop through cities and print a formatted risk report."""
    print("\n--- Risk Report ---")
    high_risk_count = 0

    for city in cities:
        status = get_safety_status(city)
        score  = get_score(city)
        score_str = f"({score}/100)" if score != -1 else ""
        print(f"  {city.title()}: {status} {score_str}")
        if status == "HIGH RISK":
            high_risk_count += 1

    print(f"\nConclusion: {high_risk_count} of {len(cities)} cities are HIGH RISK")


#Entry point
def main() -> None:
    """Main entry point — coordinates all functions."""
    cities = collect_cities()
    print_report(cities)


if __name__ == "__main__":
    main()
