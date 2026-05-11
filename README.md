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


Explain how each of your queries represents a user story. What does the query do, and how does this match all or part of a user story?
    The first query relates to the user story of a person wanting to know if a bird is increasing or declining in their population over the years. The query gets the total count if the birds in given years and shows all of them. This means that you can see how the bird count can rise and drop over time.

    The second query relates to the user story of a person who wants to know what birds are most popular in a given year. This query gets the total count of all the birds and ranks it by the largest amount to the lowest amount. This way, the user can see what are the most popular birds are as they can do something like top 10 most popular birds.