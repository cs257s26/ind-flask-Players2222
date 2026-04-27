'''Replace me with your flask app'''
from flask import Flask
from ProductionCode.command_line import find_sightings_at_location, find_most_popular_stop

app = Flask(__name__)

@app.route('/')
def homepage():
    return "Welcome to the Carleton Bird Tracker Website!"

@app.route('/sightings/<bird_name>/<int:stop>/<int:year>')
def get_sightings(bird_name, stop, year):
    """
    Returns the number of sightings for a specific bird at a specific stop/year.
    Example s
    """
    bird_count = find_sightings_at_location(bird_name, stop, year)
    if bird_count < 9999:
        return f"{bird_name} was sighted {bird_count} times at stop {stop} in {year}."
    return f"The url is wrong"

@app.route('/popular/<int:year>')
def get_popular_stop(year):
    """
    Returns the most popular stop for a given year.
    Example /popular/2000
    """
    Popular_stop = find_most_popular_stop(year)
    if Popular_stop != 0 :
        return f"The most popular stop in {year} was stop {Popular_stop}."
    return f"The url is wrong"

if __name__ == '__main__':
    app.run()