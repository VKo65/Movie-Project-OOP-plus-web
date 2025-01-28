from matplotlib.pyplot import title

import movie_storage
from random import randint
from statistics import median
import matplotlib.pyplot as plt
from fuzzywuzzy import process
from colorama import Fore, Style

from movie_storage import get_movies

print(Fore.LIGHTBLUE_EX + "********** My Movies Database **********\n" + Style.RESET_ALL)


def input_of_user():
    """ Displays a menu and prompts the user for their choice.
        With try I check, that the input is an integer.
        With if, elif I check the range between 0 - 9
        Returns: int: The user's chosen option.
    """
    print(Fore.LIGHTBLUE_EX + "Menu:\n 0. Exit\n 1. List movies\n 2. Add movie\n 3. Delete movie\n 4. Update movie\n 5. Stats\n 6. Random movie\n 7. Search movie\n 8. Movies sorted by rating\n 9. Create Rating Histogram\n" + Style.RESET_ALL)
    try:
        choice_of_user = int(input(Fore.LIGHTBLUE_EX + "Enter choice (0-9): " + Style.RESET_ALL))
    except ValueError as e:
        print(Fore.RED + f"\nInvalid choice: {e}\n" + Style.RESET_ALL)
        return
    print("")
    if choice_of_user > 9:
        print(Fore.RED + "Invalid choice! Enter choice (0-9)\n" + Style.RESET_ALL)
        return
    elif choice_of_user < 0:
        print(Fore.RED + "Invalid choice! Enter choice (0-9)\n" + Style.RESET_ALL)
        return
    return choice_of_user


def lead_to_function(input_of_user, movies):
    """ Executes the function corresponding to the user's choice.

    Parameters:
    input_of_user (int): The user's selected menu option.
    """

    if input_of_user == 1:
        list_movies()
    elif input_of_user == 2:
        while True:
            try:
                title = str(input(Fore.LIGHTYELLOW_EX + "Enter new movie name: " + Style.RESET_ALL))
                if not title.strip():
                    raise ValueError("Title cannot be empty!")
                year = int(input(Fore.LIGHTYELLOW_EX + "Enter year of release: " + Style.RESET_ALL))
                if year < 1920 or year > 2100:
                    raise ValueError("Please enter a valid year (between 1888 and 2100).")
                rating = float(input(Fore.LIGHTYELLOW_EX + "Enter new movie rating: " + Style.RESET_ALL))
                if rating < 0 or rating > 10:
                    raise ValueError("Rating must be between 0 and 10")
                movie_storage.save_movies( movie_storage.add_movie(title,year,rating))
                print("")
                break
            except ValueError as e:
                print(Fore.RED + f"Invalid input: {e}" + Style.RESET_ALL)
    elif input_of_user == 3:
        while True:
            try:
                title = str(input(Fore.LIGHTYELLOW_EX + "Enter movie name to delete: " + Style.RESET_ALL))
                if not title.strip():
                    raise ValueError("Title cannot be empty!")
                movie_storage.save_movies(movie_storage.delete_movie(title))
                print("")
                break
            except ValueError as e:
                print(Fore.RED + f"Invalid input: {e}" + Style.RESET_ALL)
    elif input_of_user == 4:
        while True:
            try:
                title = str(input(Fore.LIGHTYELLOW_EX + "Enter movie name: " + Style.RESET_ALL))
                if not title.strip():
                    raise ValueError("Title cannot be empty!")
                rating = float(input(Fore.LIGHTYELLOW_EX + "Enter new movie rating (0-10): " + Style.RESET_ALL))
                if rating < 0 or rating > 10:
                    raise ValueError("Rating must be between 0 and 10")
                movie_storage.update_movie(title, rating)
                print("")
                break
            except ValueError as e:
                print(Fore.RED + f"Invalid input: {e}" + Style.RESET_ALL)
    elif input_of_user == 5:
        movies = statistics_of_movies()
    elif input_of_user == 6:
        random_movie()
    elif input_of_user == 7:
        search_movie(movie_storage.get_movies())
    elif input_of_user == 8:
        sorted_movie(movie_storage.get_movies())
    elif input_of_user == 9:
        create_histogram(movie_storage.get_movies())
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


def list_movies():
    """
    Prints the list of all movies and their ratings.
    Load the data from json-file
    """
    print("")
    movies = movie_storage.get_movies()
    print(f"{Fore.LIGHTBLUE_EX}{len(movies)} movies in total{Style.RESET_ALL}")

    for movie, details in movies.items():
        print(f"{Fore.LIGHTBLUE_EX}{movie} ({details['year']}), Rating: {details['rating']}{Style.RESET_ALL}")
        print("")


def statistics_of_movies():
    """ Calculates and displays statistics: average rating, median rating,
    best and worst ratings.
    Function is aligned to the increased dictionary with year
    Load the data from json-file
    """
    movies = movie_storage.get_movies()
    if not movies:
        print(Fore.RED + "No movies in the database." + Style.RESET_ALL)
        return
    calculation_list = [details["rating"] for details in movies.values()]
    average = "{:.1f}".format(sum(calculation_list) / len(calculation_list))
    rating_median = "{:.1f}".format(median(calculation_list))
    best_rating = max(calculation_list)
    worst_rating = min(calculation_list)
    best_movies = [movie for movie, details in movies.items() if details["rating"] == best_rating]
    worst_movies = [movie for movie, details in movies.items() if details["rating"] == worst_rating]

    print(f"{Fore.LIGHTBLUE_EX}Average rating: {average}")
    print(f"Median rating: {rating_median}")
    print(f"Best movie: {', '.join(best_movies)}, {best_rating}")
    print(f"Worst movie: {', '.join(worst_movies)}, {worst_rating}\n")


def random_movie():
    """ Selects and displays a random movie from the list.
    Load the data from json-file
    """
    movies = movie_storage.get_movies()
    random_number = randint(0, len(movies))
    check_number = 0
    for randomly_name, randomly_rating in movies.items():
        check_number += 1
        if check_number == random_number:
            print(f"{Fore.LIGHTBLUE_EX}Your movie for tonight: {randomly_name}, it's rated {randomly_rating}\n{Style.RESET_ALL}")


def search_movie(movies):
    """ Searches for a movie by a partial name and displays matching results
    or suggests close matches.
    Load the data from json-file
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
    loop_of_input_and_action(movie_storage.get_movies())

if __name__ == "__main__":
    main()



















































