# README

Individual Flask project.
How to enter url

URL/popular/<year>
EX: URL/popular/2000   
for year: 2000 to 2025, 2005-2007 does not exist csv error :(
-----------------------------------------------------------------
URL/sightings/<bird_name>/<stop>/<year>  
EX: URL/sightings/American Crow (Corvus brachyrhynchos) /1/2003
for bird_names check the csv for the exact name (cap sensitive) and space sentivity (like the end space)
    Ex of bird Names:
    Alder Flycatcher (Empidonax alnorum) 
    American Crow (Corvus brachyrhynchos) 
    American Goldfinch (Carduelis tristis) 
    American Robin (Turdus migratorius) 
    Great Crested Flycatcher (Myiarchus crinitus) 
    Mourning Dove (Zenaida macroura) 
    Yellow-throated Vireo (Vireo flavifrons) 
for stop: 1-17
for year: 2000-2025
-----------------------------------------------------------------
Describe the process by which you decided how to represent your data in your database. Include why you selected the number of tables you did, how you decided what data to include and exclude, why you selected the datatypes you did, and what the primary keys are.
    The data set I included just cleaned the sata a bit more, I wanted all the stops and what birds landed in those spots. The main things I did were combining all of the data years into one large csv so that the sql can store the entire table. Additionally, I cleaned the name with it used to have scientific and common in the same line into just common and just scientific as that way I think is easier to search for. I chose the datatypes that I did because that is what the example create_table had so I just expanded on it.

    Copy command :\copy birds FROM 'Data/combined_bird_observations.csv' DELIMITER ',' CSV HEADER;


Explain how each of your queries represents a user story. What does the query do, and how does this match all or part of a user story?
    The first query relates to the user story of a person wanting to know how many specific birds there are at a specific stop given a specific year. This makes it simiar to the get_sigitings in the app.py. This query intakes the birdname, stop, and year and gives a numeric output

    The second query relates to the user story of a person who wants to know what the most popular stop in a given year is. It is similar to get_popular_stop in app.py. This query intakes the year option and outputs the most popular stop in the year. 