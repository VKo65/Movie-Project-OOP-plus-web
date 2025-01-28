from statistics import median
from random import randint
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from colorama import Fore, Style


movies = {
    "The Shawshank Redemption": 9.5,
    "Pulp Fiction": 8.8,
    "The Room": 3.6,
    "The Godfather": 9.2,
    "The Godfather: Part II": 9.0,
    "The Dark Knight": 9.0,
    "12 Angry Men": 8.9,
    "Everything Everywhere All At Once": 8.9,
    "Forrest Gump": 8.8,
    "Star Wars: Episode V": 8.7
}

operand = True

print("********** My Movies Database **********\n")


def input_of_user():
    #Users input in main menu
    choice_of_user = 0
    print(Fore.GREEN + "Menu:\n 1. List movies\n 2. Add movie\n 3. Delete movie\n 4. Update movie\n 5. Stats\n 6. Random movie\n 7. Search movie\n 8. Movies sorted by rating\n 9. Create Rating Histogram\n" + Style.RESET_ALL)
    choice_of_user = int(input(Fore.LIGHTYELLOW_EX + "Enter choice (1-8): " + Style.RESET_ALL))
    print("")
    if choice_of_user > 9:
        print(Fore.RED + "Invalid choice\n" + Style.RESET_ALL)
    return choice_of_user


def lead_to_function(input_of_user):

    if input_of_user == 1:
        list_movies()
    elif input_of_user == 2:
        movies = add_movie()
    elif input_of_user == 3:
        movies = del_movie()
        print("")
    elif input_of_user == 4:
        movies = update_movie()
        print("")
    elif input_of_user == 5:
        movies = statistics_of_movies()
    elif input_of_user == 6:
        random_movie()
    elif input_of_user == 7:
        search_movie()
    elif input_of_user == 8:
        sorted_movie()
    elif input_of_user == 0:
        #Exit, is not required, but comfortable
        print("Number 0")
    elif input_of_user == 9:
        create_histogram()
        print("Check")
    #else:
        #print("Invalid choice")

    input(Fore.LIGHTYELLOW_EX + "Press enter to continue\n" + Style.RESET_ALL)

def loop_of_input_and_action():
    while operand == True:
        choice_of_user = input_of_user()
        if choice_of_user == 0:
            break
        #print(f"choice = {choice_of_user}")
        lead_to_function(choice_of_user)

def list_movies():
    print("")
    print(f"{Fore.LIGHTBLUE_EX}{len(movies)} movies in total{Style.RESET_ALL}")
    for movie, rate in movies.items():
        print(Fore.LIGHTBLUE_EX + movie, str(rate) + Style.RESET_ALL)
    print("")

def add_movie():
    copy_of_movies_to_store = movies
    additional_movie = str(input(Fore.LIGHTYELLOW_EX + "Enter new movie name: " + Style.RESET_ALL))
    additional_rate = float(input(Fore.LIGHTYELLOW_EX + "Enter new movie rating: " + Style.RESET_ALL))
    copy_of_movies_to_store[additional_movie] = additional_rate
    print("")
    return copy_of_movies_to_store

def del_movie():
    copy_of_movies_to_store = movies
    to_delete_movie = str(input(Fore.LIGHTYELLOW_EX + "Enter movie name to delete: " + Style.RESET_ALL))

    if to_delete_movie in movies:
        del copy_of_movies_to_store[to_delete_movie]
        return copy_of_movies_to_store
    else:
        to_checked_list = []
        for checked_movie in movies.keys():
            to_checked_list.append(checked_movie)
        to_delete_movie = fuzzy_string_matching_for_delete(to_delete_movie, to_checked_list)
        del copy_of_movies_to_store[to_delete_movie]
        return copy_of_movies_to_store

def update_movie():
    copy_of_movies_to_store = movies
    to_update_movie = str(input(Fore.LIGHTYELLOW_EX + "Enter movie name: " + Style.RESET_ALL))

    if to_update_movie in movies:
        new_rating = input(Fore.LIGHTYELLOW_EX + "Enter new movie rating (0-10) " + Style.RESET_ALL)
        copy_of_movies_to_store[to_update_movie] = new_rating
        return copy_of_movies_to_store
    else:
        to_checked_list = []
        for checked_movie in movies.keys():
            to_checked_list.append(checked_movie)
        to_update_movie = fuzzy_string_matching_for_universal(to_update_movie, to_checked_list)
        if to_update_movie == 0:
            return copy_of_movies_to_store
        new_rating = input(Fore.LIGHTYELLOW_EX + "Enter new movie rating (0-10) " + Style.RESET_ALL)
        copy_of_movies_to_store[to_update_movie] = new_rating
        return copy_of_movies_to_store

def statistics_of_movies():

    calculation_list = list()
    best = 0
    worst = 10
    for rating_of_movie in movies.values():
        calculation_list.append(float(rating_of_movie))
    average = "{:.2f}".format(sum(calculation_list) / len(calculation_list))
    rating_median = "{:.2f}".format(median(calculation_list))
    for best_worst in calculation_list:
        if best_worst < worst:
            worst = best_worst
        elif best_worst > best:
            best = best_worst
    print(f"{Fore.LIGHTYELLOW_EX}Average rating: {average}\nMedian rating: {rating_median}\nBest movie: {best}\nWorst movie: {worst}\n{Style.RESET_ALL}")

def random_movie():
    random_number = randint(0, len(movies))
    check_number = 0
    for randomly_name, randomly_rating in movies.items():
        check_number += 1
        if check_number == random_number:
            print(f"{Fore.LIGHTYELLOW_EX}Your movie for tonight: {randomly_name}, it's rated {randomly_rating}{Style.RESET_ALL}\n")

def search_movie():
    searched_movie = str(input(Fore.LIGHTYELLOW_EX + "Enter part of movie name: " + Style.RESET_ALL))
    to_checked_list = []
    it_was_in = False
    for checked_movie in movies.keys():
        to_checked_list.append(checked_movie)
        if searched_movie in checked_movie:
            print(f"{checked_movie}, {movies[checked_movie]}")
            it_was_in = True

    if it_was_in == False:
        fuzzy_string_matching_for_search(searched_movie,to_checked_list)
    print("")

def sorted_movie():

    sorted_list = list(movies.items())
    final_sorted = list()
    rating_value = 0
    for outer_loop in range(len(movies)):
        for first_loop in range(len(sorted_list)):
            new_list = sorted_list[first_loop]
            if new_list[1] > rating_value:
                rating_value = new_list[1]
                high_score_movie = (sorted_list[first_loop])
                high_loop = first_loop
            adding_ratting = rating_value
        rating_value = 0
        del sorted_list[high_loop]
        adding_movie = str(high_score_movie[0])
        final_sorted.append(adding_movie)
        final_sorted.append(adding_ratting)
    for placeholder in range(len(final_sorted)):
        if isinstance(final_sorted[placeholder], str):
            print(Fore.LIGHTBLUE_EX, final_sorted[placeholder], end=Style.RESET_ALL)
            print(" ", end="")
        elif isinstance(final_sorted[placeholder], float):
            print(Fore.LIGHTBLUE_EX1, final_sorted[placeholder], Style.RESET_ALL)

    print("")

def create_histogram():
    #20 Bins with the ratings
    histogram_data = []
    for rating_values in movies.values():
        histogram_data.append(rating_values)

    plt.hist(histogram_data, bins = 20, edgecolor = "blue")
    plt.title("Distribution of ratings!")
    plt.xlabel("Rating")
    plt.ylabel("Frequency of rating")
    plt.draw()
    plt.pause(0.5)  #time delay to show histogram
    plt.clf()

def fuzzy_string_matching_for_search(input_of_user, to_checked_list):
    #Take the input and a generated list from the function "search_movie"
    best_match = process.extractOne(input_of_user, to_checked_list)
    if best_match[1] < 100:
        print("")
        yes_or_no = input(f"{Fore.LIGHTYELLOW_EX}{input_of_user} doesn't exist! Do you mean {best_match[0]}? (y = yes; n = no): {Style.RESET_ALL}")
        if yes_or_no == "y":
            print("")
            print(f"{Fore.LIGHTBLUE_EX}{best_match[0]}, {movies[best_match[0]]}{Style.RESET_ALL}")

def fuzzy_string_matching_for_delete(input_of_user, to_checked_list):
    #Take the input and a generated list from the function "delete_movie"
    copy_of_movies_to_store = movies
    best_match = process.extractOne(input_of_user, to_checked_list)
    if best_match[1] < 100:
        print("")
        yes_or_no = input(f"{Fore.LIGHTYELLOW_EX}{input_of_user} doesn't exist! Do you mean {best_match[0]}? (y = yes; n = no): {Style.RESET_ALL}")
        if yes_or_no == "y":
            return best_match[0]






def main():

    loop_of_input_and_action()

if __name__ == "__main__":
    main()



















































