def number_input(text: str):
    while True:
        try:
            result = float(input(text + "\n").replace(",", "."))
            if not 0 <= result <= 1000:
                raise ValueError()

            break
        except ValueError:
            print("Tente de novo.")

    return result
