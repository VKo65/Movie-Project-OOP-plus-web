from movie_app import MovieApp
from storage_csv import StorageCSV

storage = StorageCSV('movies.csv')
movie_app = MovieApp(storage)
movie_app.run()