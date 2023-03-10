from flask import flash
from app.models import Movie, Customer

##################################################
# Utility function to search for movies by title, director, or genre.
# Returns a list of movies that match the search criteria (case insensitive)
##################################################
def find_movie(search_queries):
    if not search_queries:
        flash("Please provide at least one search term.")

    query = Movie.query
    for term in search_queries:
        if term == "title":
            query = query.filter(Movie.title.ilike("%" + search_queries[term] + "%"))
        elif term == "director":
            query = query.filter(Movie.director.ilike("%" + search_queries[term] + "%"))
        elif term == "genre":
            query = query.filter(Movie.genre.ilike("%" + search_queries[term] + "%"))
    query_value = query.all()

    if not query_value:
        flash("No results found.")
    else:
        # I had to find a way to get the key and value from the dictionary and return them as a string in the flash message.
        # https://stackoverflow.com/questions/26660654/how-do-i-print-the-key-value-pairs-of-a-dictionary-in-python
        # https://stackoverflow.com/questions/58626415/turning-key-value-pairs-from-a-dictionary-into-strings

        search_strings = [
            f"{key.replace('_', ' ').title()}: {value}"
            for key, value in search_queries.items()
            if value and value.strip()
        ]
        if search_strings:
            search_message = ", ".join(search_strings)
            flash(f"Search results for: {search_message}.")
    return query.all()


##################################################
# Utility function to search for customer by first_name, last_name, or email.
# Returns a list of customers that match the search criteria (case insensitive)
##################################################
def find_customer(search_queries):
    if not search_queries:
        flash("Please provide at least one search term.")

    query = Customer.query
    for term in search_queries:
        if term == "first_name":
            query = query.filter(
                Customer.first_name.ilike("%" + search_queries[term] + "%")
            )
        elif term == "last_name":
            query = query.filter(
                Customer.last_name.ilike("%" + search_queries[term] + "%")
            )
        elif term == "email":
            query = query.filter(Customer.email.ilike("%" + search_queries[term] + "%"))
    query_value = query.all()

    if not query_value:
        flash("No results found.")
    else:
        # I had to find a way to get the key and value from the dictionary and return them as a string in the flash message.
        # https://stackoverflow.com/questions/26660654/how-do-i-print-the-key-value-pairs-of-a-dictionary-in-python
        # https://stackoverflow.com/questions/58626415/turning-key-value-pairs-from-a-dictionary-into-strings

        search_strings = [
            f"{key.replace('_', ' ').title()}: {value}"
            for key, value in search_queries.items()
            if value and value.strip()
        ]
        if search_strings:
            search_message = ", ".join(search_strings)
            flash(f"Search results for: {search_message}.")
    return query_value
