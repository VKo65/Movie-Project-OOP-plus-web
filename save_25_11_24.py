import movie_storage
from random import randint
from statistics import median
import matplotlib.pyplot as plt
from fuzzywuzzy import process
from colorama import Fore, Style



print(Fore.LIGHTBLUE_EX + "********** My Movies Database **********\n" + Style.RESET_ALL)


def input_of_user():
    """ Displays a menu and prompts the user for their choice.
        Returns:
        int: The user's chosen option.
    """
    choice_of_user = 0
    print(Fore.LIGHTBLUE_EX + "Menu:\n 0. Exit\n 1. List movies\n 2. Add movie\n 3. Delete movie\n 4. Update movie\n 5. Stats\n 6. Random movie\n 7. Search movie\n 8. Movies sorted by rating\n 9. Create Rating Histogram\n" + Style.RESET_ALL)
    choice_of_user = int(input(Fore.LIGHTBLUE_EX + "Enter choice (0-9): " + Style.RESET_ALL))
    print("")
    if choice_of_user > 9:
        print(Fore.RED + "Invalid choice" + Style.RESET_ALL)
    return choice_of_user


def lead_to_function(input_of_user, movies):
    """ Executes the function corresponding to the user's choice.

    Parameters:
    input_of_user (int): The user's selected menu option.
    """

    if input_of_user == 1:
        list_movies(movies)
    elif input_of_user == 2:
        movies = add_movie(movies)
    elif input_of_user == 3:
        movies = del_movie(movies)
        print("")
    elif input_of_user == 4:
        movies = update_movie(movies)
        print("")
    elif input_of_user == 5:
        movies = statistics_of_movies(movies)
    elif input_of_user == 6:
        random_movie(movies)
    elif input_of_user == 7:
        search_movie(movies)
    elif input_of_user == 8:
        sorted_movie(movies)
    elif input_of_user == 9:
        create_histogram(movies)
    input(Fore.LIGHTYELLOW_EX + "Press enter to continue\n" + Style.RESET_ALL)
    return movies

def loop_of_input_and_action(movies):
    """
    Continuously prompts the user for a choice and executes corresponding
    actions until the user exits.
    """
    while True:
        choice_of_user = input_of_user()
        if choice_of_user == 0:
            print(Fore.LIGHTBLUE_EX + "Bye!" + Style.RESET_ALL)
            break
        lead_to_function(choice_of_user, movies)


def list_movies(movies):
    """
    Prints the list of all movies and their ratings.
    """
    print("")
    print(f"{Fore.LIGHTBLUE_EX}{len(movies)} movies in total{Style.RESET_ALL}")
    for movie, details in movies.items():
        print(f"{Fore.LIGHTBLUE_EX}{movie} ({details['year']}), Rating: {details['rating']}{Style.RESET_ALL}")
        print("")


def add_movie(movies):
    """ Prompts the user to add a new movie with a rating.

    Returns:
    dict: The updated dictionary of movies.
    """
    additional_movie = str(input(Fore.LIGHTYELLOW_EX + "Enter new movie name: " + Style.RESET_ALL))
    additional_rate = float(input(Fore.LIGHTYELLOW_EX + "Enter new movie rating: " + Style.RESET_ALL))
    additional_year = int(input(Fore.LIGHTYELLOW_EX + "Enter year of release: " + Style.RESET_ALL))
    movies[additional_movie] = {"rating": additional_rate, "year": additional_year}
    print("")
    return movies


def del_movie(movies):
    """ Prompts the user to delete a movie by name, with fuzzy matching
     for close matches.

    Returns:
    dict: The updated dictionary of movies.
    """

    to_delete_movie = str(input(Fore.LIGHTYELLOW_EX + "Enter movie name to delete: " + Style.RESET_ALL))
    to_checked_list = list(movies.keys())

    if to_delete_movie in movies:
        del movies[to_delete_movie]
        print(Fore.LIGHTGREEN_EX + "Movie deleted!" + Style.RESET_ALL)
    else:
        matched_movie = fuzzy_string_matching_for_universal(to_delete_movie, to_checked_list)
        if matched_movie != 0:
            del movies[matched_movie]
            print(Fore.LIGHTGREEN_EX + f"Movie '{matched_movie}' deleted!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "No movie deleted!" + Style.RESET_ALL)

    return movies


def update_movie(movies):
    """ Prompts the user to update the rating of an existing movie,
    with fuzzy matching for close matches.
    The year is unchangeable

    Returns:
    dict: The updated dictionary of movies.
    """
    to_update_movie = str(input(Fore.LIGHTYELLOW_EX + "Enter movie name: " + Style.RESET_ALL))
    to_checked_list = list(movies.keys())  # List of movie titles for matching
    if to_update_movie in movies:
        new_rating = float(input(Fore.LIGHTYELLOW_EX + "Enter new movie rating (0-10): " + Style.RESET_ALL))
        movies[to_update_movie]["rating"] = new_rating
        print(Fore.LIGHTGREEN_EX + "Rating updated!" + Style.RESET_ALL)
        return copy_of_movies_to_store


def statistics_of_movies(movies):
    """ Calculates and displays statistics: average rating, median rating,
    best and worst ratings.
    Function is aligned to the increased dictionary with year
    """
    if not movies:
        print(Fore.RED + "No movies in the database." + Style.RESET_ALL)
        return
    calculation_list = [details["rating"] for details in movies.values()]
    average = "{:.2f}".format(sum(calculation_list) / len(calculation_list))
    rating_median = "{:.2f}".format(median(calculation_list))
    best_rating = max(calculation_list)
    worst_rating = min(calculation_list)
    best_movies = [movie for movie, details in movies.items() if details["rating"] == best_rating]
    worst_movies = [movie for movie, details in movies.items() if details["rating"] == worst_rating]

    print(f"{Fore.LIGHTBLUE_EX}Average rating: {average}")
    print(f"Median rating: {rating_median}")
    print(f"Best movies ({best_rating}): {', '.join(best_movies)}")
    print(f"Worst movies ({worst_rating}): {', '.join(worst_movies)}\n")


def random_movie(movies):
    """ Selects and displays a random movie from the list.
    """
    random_number = randint(0, len(movies))
    check_number = 0
    for randomly_name, randomly_rating in movies.items():
        check_number += 1
        if check_number == random_number:
            print(f"{Fore.LIGHTBLUE_EX}Your movie for tonight: {randomly_name}, it's rated {randomly_rating}\n{Style.RESET_ALL}")


def search_movie(movies):
    """ Searches for a movie by a partial name and displays matching results
    or suggests close matches.
    """
    searched_movie = str(input(Fore.LIGHTYELLOW_EX + "Enter part of movie name: " + Style.RESET_ALL))
    to_checked_list = []
    it_was_in = False
    for checked_movie in movies.keys():
        to_checked_list.append(checked_movie)
        if searched_movie in checked_movie:
            print(f"{Fore.LIGHTBLUE_EX}{checked_movie}, {movies[checked_movie]}{Style.RESET_ALL}")
            it_was_in = True
    if it_was_in == False:
        fuzzy_string_matching_for_search(searched_movie, to_checked_list, movies)
    print("")


def sorted_movie(movies):
    """use movies.item to get all pairs of the dictionary as list of tuples.
    item[0] is the name of the movie
    item[1] is the dictiobary of this movie
    with item[1] and the argument [“rating"] and each value, the sorting is defined 0 rating value
     """
    sorted_movies = sorted(movies.items(), key=lambda item: item[1]["rating"], reverse=True)

    for sequent_movie in sorted_movies:
        year = sequent_movie[1]["year"]
        rating = sequent_movie[1]["rating"]
        print(f"{Fore.LIGHTBLUE_EX}{sequent_movie[0]} ({year}), Rating: {rating}{Style.RESET_ALL}")
    print("")


def create_histogram(movies):
    #20 Bins with the ratings
    histogram_data = []
    for rating_values in movies.values():
        histogram_data.append(rating_values["rating"])

    plt.hist(histogram_data, bins = 20, edgecolor = "blue")
    plt.title("Distribution of ratings!")
    plt.xlabel("Rating")
    plt.ylabel("Frequency of rating")
    plt.draw()
    plt.pause(0.5)  #time delay to show histogram
    plt.clf()


def fuzzy_string_matching_for_search(input_of_user, to_checked_list, movies):
    #Take the input and a generated list from the function "search_movie"
    '''This is individual function for "search_movies" to have a start.
        A generalized function follows for the other two menu items'''
    best_match = process.extractOne(input_of_user, to_checked_list)
    if best_match[1] < 100:
        print("")
        yes_or_no = input(f"{Fore.LIGHTYELLOW_EX}{input_of_user} doesn't exist! Do you mean {best_match[0]}? (y = yes; n = no): {Style.RESET_ALL}")
        if yes_or_no == "y":
            print("")
            print(f"{Fore.LIGHTBLUE_EX}{best_match[0]}, {movies[best_match[0]]}{Style.RESET_ALL}")


def fuzzy_string_matching_for_universal(input_of_user, to_checked_list):
    """Take the input and a generated list from the functions "delete_movie" and "update_movies""
    It's universal and works with the updated movies dictionary.

         Parameters:
         input_of_user (str): The movie name entered by the user.
         to_checked_list (list): List of movie titles for fuzzy matching.

         Returns:
         str: The best match for the movie title, or 0 if no match is accepted."""
    best_match = process.extractOne(input_of_user, to_checked_list)
    if best_match and best_match[1] < 100:
        print("")
        yes_or_no = input(f"{Fore.LIGHTYELLOW_EX}{input_of_user} doesn't exist! Do you mean {best_match[0]}? (y = yes; n = no): {Style.RESET_ALL}")
        if yes_or_no == "y":
            return best_match[0]
        else:
            return 0


def main():
    """ Main function to start the program.
    """
    movies = movie_storage.get_movies()

    # Prüfe, ob die Daten korrekt geladen wurden
    if movies:
        print("Movies loaded successfully:")
        for title, details in movies.items():
            print(f"{title} ({details['year']}), Rating: {details['rating']}")
    else:
        print("No movies found in the database.")

    """{
        "The Shawshank Redemption": {"rating":9.5, "year": 1994},
        "Pulp Fiction": {"rating": 8.8, "year": 1994},
        "The Room": {"rating": 3.6, "year": 1994},
        "The Godfather": {"rating": 9.2, "year": 1994},
        "The Godfather: Part II": {"rating": 9.0, "year": 1994},
        "The Dark Knight": {"rating": 9.0, "year": 1994},
        "12 Angry Men": {"rating": 8.9, "year": 1994},
        "Everything Everywhere All At Once": {"rating": 8.9, "year": 1994},
        "Forrest Gump": {"rating": 8.8, "year": 1994},
        "Star Wars: Episode V": {"rating": 8.7, "year": 1994}
    }"""
    loop_of_input_and_action(movies)

if __name__ == "__main__":
    main()



















































