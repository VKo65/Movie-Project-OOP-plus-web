from abc import ABC, abstractmethod


class IStorage(ABC):
    """
        Interface (abstract base class) for movie storage systems.

        This class defines the blueprint for any storage system used in the movie_app.
        Any class that inherits from IStorage MUST implement the following methods:

        - list_movies(): Returns all stored movies.
        - add_movie(title, details): Adds a new movie to the storage.
        - delete_movie(title): Deletes a movie from the storage.
        - update_movie(title, rating): Updates the rating of a movie.

        If a subclass does not implement these methods, Python will raise an error.
    """
    @abstractmethod
    def list_movies(self):
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        pass

    @abstractmethod
    def delete_movie(self, title):
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        pass
