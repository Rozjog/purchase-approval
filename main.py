from requests import (
    create_request,
    find_by_name,
    cancel_request,
    show_requests
)
from approvals import approve_request
from storage import load_requests, save_requests
from utils import input_int


FILENAME = "data/requests.json"


def main() -> None:
    requests: list[dict] = load_requests(FILENAME)

    budget = 250000
    role = "Директор"

    while True:
        print("\n=== Согласование закупок ===\n")
        print("1. Показать заявки")
        print("2. Создать заявку")
        print("3. Найти заявку")
        print("4. Согласовать заявку")
        print("5. Отменить заявку")
        print("0. Выход")

        choice = input_int("Выберите действие: ")

        if choice == 1:
            show_requests(requests)

        elif choice == 2:
            name = input("Название заявки: ")
            amount = input_int("Сумма: ")
            contractor = input("Контрагент: ")

            create_request(
                requests,
                name,
                amount,
                contractor
            )

            save_requests(FILENAME, requests)
            print("Заявка создана")

        elif choice == 3:
            name = input("Введите название заявки: ")

            request = find_by_name(requests, name)

            if request is None:
                print("Заявка не найдена")
            else:
                print(request)

        elif choice == 4:
            name = input("Введите название заявки: ")

            request = find_by_name(requests, name)

            if request is None:
                print("Заявка не найдена")
            else:
                budget = approve_request(
                    request,
                    budget,
                    role
                )

                save_requests(FILENAME, requests)

                print("Статус:", request["status"])
                print("Остаток бюджета:", budget)

        elif choice == 5:
            name = input("Введите название заявки: ")

            if cancel_request(requests, name):
                save_requests(FILENAME, requests)
                print("Заявка отменена")
            else:
                print("Заявка не найдена")

        elif choice == 0:
            print("Программа завершена")
            break

        else:
            print("Такого пункта нет")


if __name__ == "__main__":
    main()
