
import datetime  

# Named constants 
HIGH_RISK_THRESHOLD:   int = 70
MEDIUM_RISK_THRESHOLD: int = 50
INPUT_FILE:            str = "locations.txt"   # file we READ from
LOG_FILE:              str = "safety_log.txt"  # file we WRITE to
SEPARATOR:             str = "─" * 52

#Global database 
LOCATIONS: dict = {
    "Buea":       40,
    "Bamenda":    70,
    "Douala":     60,
    "Bafoussam":  35,
    "Ngoaundere": 78,
    "Bertoua":    90,
    "Ebolowa":    24,
    "Yaounde":    10,
    "Maroua":     56,
    "Garoua":     67,
}


def get_score(location: str) -> int:
    """Return the risk score for a location, or -1 if unknown."""
    return LOCATIONS.get(location, -1)  # -1 = not found sentinel



def get_safety_status(score: int) -> str:
    """
    Return a three-tier risk label based on the crime score.
      >= 70  →  High Risk
      >= 50  →  Medium Risk
      <  50  →  Low Risk
    """
    if score >= HIGH_RISK_THRESHOLD:
        return "High Risk"
    elif score >= MEDIUM_RISK_THRESHOLD:   # between 50 and 69
        return "Medium Risk"
    else:                                  # below 50
        return "Low Risk"



def calculate_risk(location: str) -> dict:
    """
    Clean the location name, look it up, and return a result
    dictionary with keys: location, score, status, found.
    """
    location = location.strip().title()        # "buea" → "Buea"
    score    = get_score(location)             # -1 if not in database
    found    = score != -1                     # True if city was found
    status   = get_safety_status(score) if found else "Unknown"

    return {
        "location": location,
        "score":    score,
        "status":   status,
        "found":    found,
    }



def read_locations_from_file(filename: str) -> list:
    """
    Read location names from a .txt file (one city per line).
    Returns a list of location strings.
    Raises a clear error message if the file cannot be read.

    Exceptions handled:
      FileNotFoundError — file does not exist
      PermissionError   — file exists but cannot be opened
      Exception         — any other unexpected error
    """
    try:
        # 'with open' automatically closes the file when done
        # 'r' means read mode
        with open(filename, "r") as file:
            # Read all lines, strip whitespace, skip blank lines
            locations = [
                line.strip()
                for line in file.readlines()
                if line.strip()             # skip empty lines
            ]

        # It extra check if the file was opened but had no valid content
        if not locations:
            raise ValueError(f"'{filename}' is empty. Add city names.")

        print(f"  Loaded {len(locations)} location(s) from '{filename}'")
        return locations

    except FileNotFoundError:
        # If file does not exist at all
        print(f"\n  ERROR: '{filename}' not found.")
        print(f"  Fix  : Create a file named '{filename}' in the same")
        print(f"         folder as this script, one city name per line.")
        return []   # return empty list so program can exit cleanly

    except PermissionError:
        # File exists but the OS blocked access
        print(f"\n  ERROR: No permission to read '{filename}'.")
        print(f"  Fix  : Check the file is not locked or read-only.")
        return []

    except ValueError as e:
        #triggered empty files
        print(f"\n  ERROR: {e}")
        return []

    except Exception as e:
        # Catch-all for anything unexpected
        print(f"\n  UNEXPECTED ERROR reading '{filename}': {e}")
        return []



def log_results(results: list, filename: str) -> None:
    """
    Append each result with a timestamp to the log file.
    Creates the file if it does not exist.
    Uses 'a' (append) mode so previous runs are never overwritten.

    Exceptions handled:
      PermissionError — cannot write to the file
      Exception       — any other unexpected error
    """
    # Get current date and time as a formatted string
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # 'a' = append mode ie add at the end of a file -> never overwrite
        with open(filename, "a") as log:
            log.write(f"\n{'='*52}\n")
            log.write(f"Run timestamp : {timestamp}\n")
            log.write(f"{'='*52}\n")

            for r in results:
                if r["found"]:
                    # Write one line per location found
                    log.write(
                        f"  {r['location']:<14} │ "
                        f"Score: {r['score']:>3}/100 │ "
                        f"{r['status']}\n"
                    )
                else:
                    # Write a line not found
                    log.write(
                        f"  {r['location']:<14} │ Not in database\n"
                    )

            log.write(f"{'='*52}\n")

        print(f"\n  Results saved to '{filename}'")

    except PermissionError:
        print(f"\n  ERROR: Cannot write to '{filename}'.")
        print(f"  Fix  : Check the file is not open in another program.")

    except Exception as e:
        print(f"\n  UNEXPECTED ERROR writing to '{filename}': {e}")



def print_report(results: list) -> None:
    """
    Print a formatted safety report from a list of result
    dictionaries. Includes per-city breakdown and summary.
    """
    # Count each risk using list comprehensions
    high   = sum(1 for r in results if r["status"] == "High Risk")
    medium = sum(1 for r in results if r["status"] == "Medium Risk")
    low    = sum(1 for r in results if r["status"] == "Low Risk")

    print(f"\n{SEPARATOR}")
    print(f"{'SAFETY REPORT — CAMEROON LOCATIONS':^52}")
    print(SEPARATOR)

    for r in results:
        if r["found"]:
            # :<14 left-aligns name | :>3 right-aligns score
            print(
                f"  {r['location']:<14} │ "
                f"Score: {r['score']:>3}/100 │ "
                f"{r['status']}"
            )
        else:
            print(f"  {r['location']:<14} │ Not in database")

    print(SEPARATOR)
    print(
        f"  Summary  →  "
        f"High Risk: {high}  │  "
        f"Medium Risk: {medium}  │  "
        f"Low Risk: {low}"
    )
    print(SEPARATOR)



def main() -> None:
    """
    Main entry point — coordinates all functions in order.
    Exits early and cleanly if the input file cannot be read.
    """
    print(SEPARATOR)
    print(f"{'WEATHER & SAFETY TOOL':^52}")
    print(SEPARATOR)

    #  read locations from file -> with error handling
    raw_locations = read_locations_from_file(INPUT_FILE)

    #  exit early if file reading failed
    if not raw_locations:
        print(f"\n  Program stopped. Fix the issue above and try again.")
        return

    #  process each location into a result dictionary
    results = [calculate_risk(loc) for loc in raw_locations]

    #  print the report to the terminal
    print_report(results)

    #  append results + timestamp to the log file
    log_results(results, LOG_FILE)


if __name__ == "__main__":
    main()
