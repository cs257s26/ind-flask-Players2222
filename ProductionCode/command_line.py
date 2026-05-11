import argparse
from datasource import DataSource

def print_sightings(bird_name, stop, year):
    db = DataSource()
    count = db.get_sightings_by_location(bird_name, stop, year)
    db.close()

    if count is not None:
        print(f"Result: {bird_name} was sighted {count} times at stop {stop} in {year}.")
    else:
        print(f"Error: No data found for {bird_name} at stop {stop} in {year}.")

def print_popular_stop(year):
    db = DataSource()
    stop = db.get_most_popular_stop(year)
    db.close()

    if stop:
        print(f"The most popular stop in {year} was stop {stop}.")
    else:
        print(f"No data available for the year {year}.")

def main():
    parser = argparse.ArgumentParser(description="Bird Database CLI")
    parser.add_argument("--bird", help="Bird common name")
    parser.add_argument("--stop", type=int, help="Stop number (1-17)")
    parser.add_argument("--year", type=int, required=True, help="Year")
    parser.add_argument("--mode", choices=["sightings", "popular"], required=True)

    args = parser.parse_args()

    if args.mode == "sightings" and args.bird and args.stop:
        print_sightings(args.bird, args.stop, args.year)
    elif args.mode == "popular":
        print_popular_stop(args.year)
    else:
        print("Missing arguments for the selected mode.")

if __name__ == "__main__":
    main()