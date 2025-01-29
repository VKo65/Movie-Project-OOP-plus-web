import os

class MovieApp:
    """
    A movie management application that allows users to store, list,
    analyze, and generate an HTML page for their movie collection.
    """

    def __init__(self, storage):
        """
        Initializes the MovieApp with a storage backend.

        :param storage: An instance of a storage class (e.g., StorageJson).
        """
        self._storage = storage  # Speicherung der Filme

    def _command_list_movies(self):
        """Retrieves and displays all stored movies."""
        movies = self._storage.list_movies()
        if movies:
            for title, details in movies.items():
                print(
                    f"{title} ({details.get('year', 'Unbekannt')}) - rating: {details.get('rating', 'Keine Bewertung')}")
        else:
            print("No movie available.")

    def _command_add_movie(self):
        """Prompts the user to add a new movie and saves it."""
        title = input("Title: ")
        year = input("Year: ")
        rating = input("Rating (1-10): ")
        poster = input("Website of poster: ")

        self._storage.add_movie(title, {"year": year, "rating": rating, "poster": poster})
        print(f"Movie '{title}' was added!")

    def _command_movie_stats(self):
        """
        Calculates and displays statistics based on stored movies.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("No movie avaulable for statistics.")
            return

        ratings = [float(details['rating']) for details in movies.values() if 'rating' in details]
        if ratings:
            print(f"Average rating: {sum(ratings) / len(ratings):.2f}")
            print(f"Best rating: {max(ratings)}")
            print(f"Worst rating: {min(ratings)}")
        else:
            print("No rating.")

    def _generate_website(self):
        """Generates an HTML page displaying the movie collection."""
        movies = self._storage.list_movies()

        if not movies:
            print("No movie available. HTML-file can't be generated.")
            return

        html_content = """<html>
           <head><title>Meine Filme</title></head>
           <body><h1>Meine Filmsammlung</h1><ul>"""

        for title, details in movies.items():
            year = details.get('year', 'Unbekannt')
            rating = details.get('rating', 'Keine Bewertung')
            poster = details.get('poster', '')

            if poster:
                html_content += f'<li>{title} ({year}) - Bewertung: {rating} <br> <img src="{poster}" width="100"></li>'
            else:
                html_content += f'<li>{title} ({year}) - Bewertung: {rating}</li>'

        html_content += """</ul></body></html>"""

        # Datei im aktuellen Verzeichnis speichern
        file_path = os.path.join(os.getcwd(), "movies.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"HTML-site was generated: {file_path}")

    def run(self):
        """Runs the main application loop."""
        while True:
            print("\nMovie administration:")
            print("1. List Movies")
            print("2. Add Movie")
            print("3. Show statistic")
            print("4. Generate HTML-Site")
            print("5. Exit")

            choice = input("Please chose a option: ")

            if choice == "1":
                self._command_list_movies()
            elif choice == "2":
                self._command_add_movie()
            elif choice == "3":
                self._command_movie_stats()
            elif choice == "4":
                self._generate_website()
            elif choice == "5":
                print("Exit.")
                break
            else:
                print("Invalid input. Please enter a number from 1-5!")

