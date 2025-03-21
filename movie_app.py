import os
import requests
from dotenv import load_dotenv


load_dotenv()  # Lädt die .env-Datei
api_key = os.getenv("API_KEY")

class MovieApp:
    """
    A movie management application that allows users to store, list,
    analyze, and generate an HTML page for their movie collection.

    Attributes:
        storage (IStorage): An instance of a storage backend (e.g., StorageJson).
    """

    def __init__(self, storage):
        """
        Initializes the MovieApp with a storage backend.

        :param storage: An instance of a storage class (e.g., StorageJson).
        """
        self._storage = storage

    def _command_list_movies(self):
        """
        Retrieves and displays all stored movies from the storage backend.

        If no movies are stored, it informs the user accordingly.
        """
        movies = self._storage.list_movies()
        if movies:
            for title, details in movies.items():
                print(
                    f"{title} ({details.get('year', 'unknown')}) - rating: {details.get('rating', 'No rating')}")
        else:
            print("No movie available.")

    def _command_add_movie(self):
        """
        Fetches movie data from an external API and saves it to the storage.

        Prompts the user to enter a movie title, retrieves its details (year, rating, poster)
        from the OMDB API, and stores it in the selected storage backend.
        """

        title = input("Enter movie title: ")
        api_url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"

        try:
            response = requests.get(api_url)  # API-request
            response.raise_for_status()  # Check status (e.g. 404, 500)
            movie_data = response.json()  # Transform to JSON-data

            if movie_data.get("Response") == "True":  # Check existing of movie
                year = movie_data.get("Year", "Unknown")
                rating = movie_data.get("imdbRating", "No Rating")  #IMDb-Rating
                if rating == "N/A":
                    rating = "No Rating"
                poster = movie_data.get("Poster", "")

                try:
                    self._storage.add_movie(title, {"year": year, "rating": rating, "poster": poster})
                    print(f"✅ Movie '{title}' was added successfully!")
                except ValueError as e:
                    print(f"⚠️ {e}")

            else:
                print(f"⚠️ Movie '{title}' not found in API.")


        except requests.ConnectionError:
            print("Connection error: Unable to reach the API. Check your internet connection.")
        except requests.Timeout:
            print("Timeout error: The API took too long to respond.")
        except requests.RequestException as error:
            print(f"Error fetching movie data: {error}")


    def _command_del_movie(self):
        """
        Deletes a movie from the storage backend.

        Prompts the user for a movie title and removes it from storage if it exists.
        """
        movie_delete = str(input("Please enter movie to delete: "))

        try:
            self._storage.delete_movie(movie_delete)
            print(f"✅ Movie '{movie_delete}' was deleted successfully!")
        except ValueError as e:
            print(f"⚠️ {e}")


    def _command_movie_stats(self):
        """
        Calculates and displays statistics based on stored movies.

        Computes and prints:
        - The average rating of all stored movies.
        - The highest-rated movie.
        - The lowest-rated movie.

        If no ratings exist, informs the user.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("No movie available for statistics.")
            return
        ratings = []
        for details in movies.values():
            if 'rating' in details:
                try:
                    ratings.append(float(details['rating']))
                except ValueError:
                    pass
        #ratings = [float(details['rating']) for details in movies.values() if 'rating' in details]
        if ratings:
            print(f"Average rating: {sum(ratings) / len(ratings):.2f}")
            print(f"Best rating: {max(ratings)}")
            print(f"Worst rating: {min(ratings)}")
        else:
            print("No rating.")

    def _generate_website(self):
        """
        Generates an HTML file that displays the user's movie collection.

        Reads an HTML template, inserts movie data dynamically, and saves
        the output as an `index.html` file in the current directory.
        """
        movies = self._storage.list_movies()

        if not movies:
            print("No movie available. HTML-file can't be generated.")
            return

        template_path = os.path.join(os.getcwd(), "index_template.html")

        try:
            with open(template_path, "r", encoding="utf-8") as file:
                template_content = file.read()
        except FileNotFoundError:
            print("Template file not found! Make sure `_static/index_template.html` exists.")
            return

        movie_grid = ""

        for title, details in movies.items():
                year = details.get('year', 'unknown')
                rating = details.get('rating', 'unknown')
                poster = details.get('poster', '')

                movie_grid += f"""
                    <li>
                        <div class="movie">
                            <img src="{poster}" alt="{title}" class="movie-poster">
                            <div class="movie-title">{title}</div>
                            <div class="movie-year">({year}) ⭐ {rating}</div>
                        </div>
                    </li>
                    """
        final_html = template_content.replace("__TEMPLATE_TITLE__", "My Movie Collection")
        final_html = final_html.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)


        output_path = os.path.join(os.getcwd(), "index.html")
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(final_html)

        print(f"✅ Website was generated successfully: {output_path}")




    def run(self):
        """Runs the main application loop."""
        while True:
            print("\nMovie administration:")
            print("1. List Movies")
            print("2. Add Movie")
            print("3. Delete Movie")
            print("4. Show statistic")
            print("5. Generate HTML-Site")
            print("6. Exit")

            choice = input("Please chose a option: ")

            if choice == "1":
                self._command_list_movies()
            elif choice == "2":
                self._command_add_movie()
            elif choice == ("3"):
                self._command_del_movie()
            elif choice == "4":
                self._command_movie_stats()
            elif choice == "5":
                self._generate_website()
            elif choice == "6":
                print("Exit.")
                break
            else:
                print("Invalid input. Please enter a number from 1-6!")

