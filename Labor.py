import movie_storage

def main():
    while True:
        print("\nMenu:")
        print("1. Add Movie")
        print("2. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            movie_storage.add_movie()
        elif choice == "2":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()