from movie_app import MovieApp
from storage.storage_json import StorageJson

def main():
    """Starts the MovieApp with the JSON storage"""
    storage = StorageJson("data/movies.json")
    app = MovieApp(storage)
    app.run()

if __name__ == "__main__":
    main()


















































