if __name__ == "__main__":
    print("Enter any number. Use Ctrl + D to exit")

    while True:
        try:
            print("You entered:", int(input()))
            break
        except ValueError:
            print("Try again")
            continue
        except EOFError:
            break
