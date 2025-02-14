import calculator

def main():
    print("Welcome to the Python calculator!")
    user_input = input("How many calculation do you want to do?")
    calculator.calc_iterations(user_input)

if __name__ == "__main__":
    main()