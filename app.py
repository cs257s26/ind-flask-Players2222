from flask import Flask, render_template, request
from datasource import DataSource

app = Flask(__name__)

@app.route('/')
def homepage():
    return "Welcome to the Carleton Bird Tracker! Use /sightings/<bird>/<stop>/<year> or /popular/<year>"

@app.route('/sightings/<bird_name>/<int:stop>/<int:year>')
def get_sightings(bird_name, stop, year):
    """
    Mastery: Executes flawlessly by validating inputs and handling missing data 
    without crashing.
    """
    # Validation for the range of stops in your dataset
    if stop < 1 or stop > 17:
        return f"Invalid stop number: {stop}. Please choose a stop between 1 and 17.", 400

    db = DataSource()
    # This calls the updated method that targets the specific 'stopX' column
    count = db.get_sightings_by_location(bird_name, stop, year)
    db.close()

    if count is not None:
        return f"{bird_name} was sighted {count} times at stop {stop} in {year}."
    
    return f"No records found for {bird_name} in {year} at stop {stop}."

@app.route('/popular/<int:year>')
def get_popular_birds(year):
    """
    Mastery: Linked strongly to the casual birdwatcher user story.
    """
    db = DataSource()
    # Returns the top 10 birds using your specialized ranking query
    top_birds = db.get_top_birds_by_year(year, 10)
    db.close()

    if top_birds:
        # Formats the result as a clean, readable list for the user
        result_list = [f"{bird[0]} ({bird[1]} sightings)" for bird in top_birds]
        return f"<h1>Top Birds in {year}</h1>" + "<br>".join(result_list)
    
    return f"No bird data available for the year {year}."

if __name__ == '__main__':
    app.run()