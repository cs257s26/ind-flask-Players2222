import psycopg2 as ps
import psqlConfig as config

class DataSource:
    def __init__(self):
        """Initializes the connection to the Stearns PostgreSQL server."""
        self.connection = self.connect()

    def connect(self):
        """
        Establishes a connection to the database using credentials from psqlConfig.
        Note: This is set to localhost for use on the Stearns terminal.
        """
        try:
            connection = ps.connect(
                database=config.database, 
                user=config.user, 
                password=config.password, 
                host="localhost"
            )
            return connection
        except Exception as e:
            print("Connection error: ", e)
            exit()

    def get_species_trend(self, species_name):
        """
        User Story: As a conservationist, I want to track how the population of a specific bird species has changed over time.
        """
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT observation_year, total_count 
                FROM birds 
                WHERE common_name ILIKE %s 
                ORDER BY observation_year;
            """
            cursor.execute(query, (species_name,))
            return cursor.fetchall()
        except Exception as e:
            print("Something went wrong with the trend query: ", e)
            return None

    def get_top_birds_by_year(self, year, limit=10):
        """
        User Story: As a casual birdwatcher, I want to know which birds were most commonly sighted in a specific year.
        """
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT common_name, total_count 
                FROM birds 
                WHERE observation_year = %s 
                ORDER BY total_count DESC 
                LIMIT %s;
            """
            cursor.execute(query, (year, limit))
            return cursor.fetchall()
        except Exception as e:
            print("Something went wrong with the ranking query: ", e)
            return None

    def close(self):
        """Closes the database connection."""
        if self.connection:
            self.connection.close()

def main():
    ds = DataSource()

    # Test Q1: Population trend for American Crows
    print("--- 25-Year Trend: American Crow ---")
    crow_results = ds.get_species_trend("American Crow")
    if crow_results:
        for row in crow_results:
            print(f"Year: {row[0]} | Count: {row[1]}")
    else:
        print("No data found or query failed.")

    # Test Q2: Top 5 birds sighted in 2024
    print("\n--- Top 5 Bird Sightings in 2024 ---")
    top_2024 = ds.get_top_birds_by_year(2024, 5)
    if top_2024:
        for row in top_2024:
            print(f"Species: {row[0]:<25} | Total: {row[1]}")
    else:
        print("No data found or query failed.")
    ds.close()

if __name__ == "__main__":
    main()