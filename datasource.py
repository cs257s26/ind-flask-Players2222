import psycopg2 as ps
import psqlConfig as config

class DataSource:
    def __init__(self):
        self.connection = self.connect()

    def connect(self):
        try:
            connection = ps.connect(
                database=config.database, 
                user=config.user, 
                password=config.password, 
                host='localhost'
            )
            return connection
        except Exception as e:
            print("Connection error: ", e)
            exit()

    def get_sightings_by_location(self, bird_name, stop, year):
        """
        User Story: Find sightings for a bird at a specific stop.
        """
        try:
            stop_num = int(stop)
            if not (1 <= stop_num <= 17):
                print(f"Validation error: Stop {stop} is out of bounds (Must be 1-17).")
                return None
        except (ValueError, TypeError):
            print(f"Validation error: Stop '{stop}' is not a valid integer.")
            return None
        
        try:
            cursor = self.connection.cursor()
            column_name = f"stop{stop_num}"
            query = f"SELECT {column_name} FROM birds WHERE common_name ILIKE %s AND observation_year = %s;"
            
            cursor.execute(query, (f"%{bird_name}%", year))
            result = cursor.fetchone()
            if result is None:
                return None
            return result[0]
        except Exception as e:
            print(f"Location query error: {e}")
            return None

    def get_most_popular_stop(self, year):
        """
        User Story: As a researcher, I want to identify which stop had the highest bird activity in a given year.
        """
        try:
            cursor = self.connection.cursor()
            stops = [f"SUM(stop{i})" for i in range(1, 18)]
            query = f"SELECT {', '.join(stops)} FROM birds WHERE observation_year = %s;"
            
            cursor.execute(query, (year,))
            row = cursor.fetchone()
            
            if row:
                if all(val is None for val in row):
                    return None
                max_val = max([val for val in row if val is not None])
                return row.index(max_val) + 1
            return None
        except Exception as e:
            print(f"Popular stop query error: {e}")
            return None

    def close(self):
        if self.connection:
            self.connection.close()

if __name__ == '__main__':
    print("Initializing DataSource and testing")
    ds = DataSource()
    
    #Test user story 1
    test_bird = "Robin"
    test_stop = 3
    test_year = 2023
    print(f"\n--- Testing US 1: Sightings for '{test_bird}' at Stop {test_stop} in {test_year} ---")
    sightings = ds.get_sightings_by_location(test_bird, test_stop, test_year)
    print(f"Result: {sightings} sightings found.")

    print(f"\nTesting edgecase (Stop 99):")
    bad_stop_sightings = ds.get_sightings_by_location(test_bird, 99, test_year)
    print(f"Result for stop 99: {bad_stop_sightings} (Expected: None)")
    
    #Test user story 1 when bird doesn't exist
    print(f"Testing corner case (Fake Bird Name):")
    fake_sightings = ds.get_sightings_by_location("NotABorealBird123", test_stop, test_year)
    print(f"Result for fake bird: {fake_sightings} (Expected: None)")

    #Test user story 2
    print(f"\n--- Testing US 2: Most popular stop in {test_year} ---")
    popular_stop = ds.get_most_popular_stop(test_year)
    print(f"Result: Stop {popular_stop} was the most popular.")
    
    #Test user story 2 when year has no data
    print(f"Testing edgecase (Year 1776):")
    fake_year_stop = ds.get_most_popular_stop(1776)
    print(f"Result for year 1776: {fake_year_stop} (Expected: None)")

    #close
    ds.close()
    print("\nDatabase closed. Test complete!")