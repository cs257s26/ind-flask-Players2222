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
                host="localhost"
            )
            return connection
        except Exception as e:
            print("Connection error: ", e)
            exit()

    def get_species_trend(self, species_name):
        """User Story: Track population change over time."""
        if not species_name: return []
        try:
            cursor = self.connection.cursor()
            query = "SELECT observation_year, total_count FROM birds WHERE common_name ILIKE %s ORDER BY observation_year;"
            cursor.execute(query, (f"%{species_name}%",))
            return cursor.fetchall()
        except Exception as e:
            print(f"Trend query error: {e}")
            return None

    def get_top_birds_by_year(self, year, limit=10):
        """User Story: Find most popular birds in a year."""
        try:
            cursor = self.connection.cursor()
            query = "SELECT common_name, total_count FROM birds WHERE observation_year = %s ORDER BY total_count DESC LIMIT %s;"
            cursor.execute(query, (year, limit))
            return cursor.fetchall()
        except Exception as e:
            print(f"Ranking query error: {e}")
            return None

    def get_sightings_by_location(self, bird_name, stop, year):
        """
        User Story: Find sightings for a bird at a specific stop.
        This now queries the numeric 'stopX' columns directly.
        """
        try:
            cursor = self.connection.cursor()
            column_name = f"stop{stop}"
            query = f"SELECT {column_name} FROM birds WHERE common_name ILIKE %s AND observation_year = %s;"
            
            cursor.execute(query, (f"%{bird_name}%", year))
            result = cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            print(f"Location query error: {e}")
            return None

    def get_most_popular_stop(self, year):
        """
        User Story: As a researcher, I want to identify which geographic 
        location (stop) had the highest bird activity in a given year.
        """
        try:
            cursor = self.connection.cursor()
            # We construct a query that sums each stop column for the given year
            stops = [f"SUM(stop{i})" for i in range(1, 18)]
            query = f"SELECT {', '.join(stops)} FROM birds WHERE observation_year = %s;"
            
            cursor.execute(query, (year,))
            row = cursor.fetchone()
            
            if row:
                # Find the index of the maximum sum
                max_val = max(row)
                # The stop number is index + 1
                return row.index(max_val) + 1
            return None
        except Exception as e:
            print(f"Popular stop query error: {e}")
            return None

    def close(self):
        if self.connection:
            self.connection.close()