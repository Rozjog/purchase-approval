def input_int(prompt: str):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Введите целое число")
