from flask import Flask, request
from datasource import DataSource

app = Flask(__name__)

@app.route('/')
def homepage():
    return "Welcome to the Carleton Bird Tracker!"

@app.route('/sightings/<bird_name>/<int:stop>/<int:year>')
def get_sightings(bird_name, stop, year):
    if stop < 1 or stop > 17:
        return "Stop must be between 1 and 17.", 400
    
    db = DataSource()
    count = db.get_sightings_by_location(bird_name, stop, year)
    db.close()

    if count is not None:
        return f"{bird_name} was sighted {count} times at stop {stop} in {year}."
    return "No records found."

@app.route('/popular/<int:year>')
def get_popular_stop(year):
    db = DataSource()
    stop = db.get_most_popular_stop(year)
    db.close()

    if stop:
        return f"The most popular stop in {year} was stop {stop}."
    return f"No data found for {year}."

if __name__ == '__main__':
    app.run(debug=False) # Set to False for production/Stearns