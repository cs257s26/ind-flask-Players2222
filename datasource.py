import psycopg2 as ps
import psqlConfig as config

class DataSource:
    def __init__(self):
        self.connection = self.connect()

    def connect(self):
        """ Connects to the database using credentials from psqlConfig."""
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

    def get_total_count_by_species(self, common_name):
        """
        Q1: User Story - As a researcher, I want to see the total observations for a specific bird across all years.
        """
        try:
            cursor = self.connection.cursor()
            # We use ILIKE for case-insensitive matching
            query = "SELECT observation_year, total_count FROM birds WHERE common_name ILIKE %s ORDER BY observation_year;"
            cursor.execute(query, (common_name,))
            return cursor.fetchall()
        except Exception as e:
            print("Query 1 error: ", e)
            return None

    def get_top_birds_in_year(self, year, limit=10):
        """
        Q2: User Story - As a birdwatcher, I want to know which birds were most commonly sighted in a specific year.
        """
        try:
            cursor = self.connection.cursor()
            query = "SELECT common_name, total_count FROM birds WHERE observation_year = %s ORDER BY total_count DESC LIMIT %s;"
            cursor.execute(query, (year, limit))
            return cursor.fetchall()
        except Exception as e:
            print("Query 2 error: ", e)
            return None

    def close(self):
        self.connection.close()

def main():
    ds = DataSource()

    # Test Q1: Trend for American Crows
    print("--- Trend for American Crow ---")
    crow_data = ds.get_total_count_by_species("American Crow")
    if crow_data:
        for row in crow_data:
            print(f"Year: {row[0]}, Count: {row[1]}")

    print("\n--- Top 5 Birds in 2024 ---")
    # Test Q2: Top birds in 2024
    top_birds = ds.get_top_birds_in_year(2024, 5)
    if top_birds:
        for row in top_birds:
            print(f"Bird: {row[0]}, Total: {row[1]}")

    ds.close()

if __name__ == "__main__":
    main()