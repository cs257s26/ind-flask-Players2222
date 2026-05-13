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
                host = 'localhost'
            )
            return connection
        except Exception as e:
            print("Connection error: ", e)
            exit()

    def get_sightings_by_location(self, bird_name, stop, year):
        """
        User Story: Find sightings for a bird at a specific stop. This now queries the 'stop#' columns directly.
        """
        try:
            cursor = self.connection.cursor()
            column_name = f"stop{stop}"
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
                max_val = max(row)
                return row.index(max_val) + 1
            return None
        except Exception as e:
            print(f"Popular stop query error: {e}")
            return None

    def close(self):
        if self.connection:
            self.connection.close()