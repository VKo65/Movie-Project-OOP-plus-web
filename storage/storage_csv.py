import csv
from istorage import IStorage

class StorageCSV:
    """A storage class that manages movies using a CSV file.
    Implements the IStorage interface."""

    def __init__(self, file_path):
        self.file_path = file_path


    def _load_movies(self):
        """Loads movies from the CSV file and returns them as a dictionary."""
        movies = {}
        try:
            with open(self.file_path, newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    movies[row["title"]] = {
                        "year": row["year"],
                        "rating": row["rating"],
                        "poster": row["poster"]
                    }
        except FileNotFoundError:
            return {}  # if there is an empty file, an empty dictionary will return
        except Exception as e:
            print(f"Error loading CSV file: {e}")
            return {}
        return movies


    def _save_movies(self, movies):
        """Saves movies to the CSV file.
        Newline takes care, that we don't have empty row.
        With utf-8 we make sure, that we have umlaute"""
        #print(f"Saving CSV file at: {self.file_path}")
        with open(self.file_path, "w", newline="", encoding="utf-8") as file:
            fieldnames = ["title", "year", "rating", "poster"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for title, details in movies.items():
                writer.writerow({
                    "title": title,
                    "year": details["year"],
                    "rating": details["rating"],
                    "poster": details["poster"]
                })

    def list_movies(self):
        """Returns all movies from the storage."""
        return self._load_movies()

    def add_movie(self, title, details):
        """Adds a new movie to the storage."""
        movies = self._load_movies()
        if title in movies:
            raise ValueError(f"Movie '{title}' already exists.")
        movies[title] = details
        self._save_movies(movies)

    def delete_movie(self, title):
        """Deletes a movie from the storage."""
        movies = self._load_movies()
        if title not in movies:
            raise ValueError(f"Movie '{title}' not found.")
        del movies[title]
        self._save_movies(movies)

    def update_movie(self, title, rating):
        """Updates the rating of a movie."""
        movies = self._load_movies()
        if title not in movies:
            raise ValueError(f"Movie '{title}' not found.")
        movies[title]["rating"] = rating
        self._save_movies(movies)