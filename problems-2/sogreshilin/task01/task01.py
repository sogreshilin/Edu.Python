if __name__ == "__main__":
    print("Enter any number. Use Ctrl + D to exit")

    while True:
        try:
            float(input())
            break
        except ValueError:
            continue
        except EOFError:
            break
