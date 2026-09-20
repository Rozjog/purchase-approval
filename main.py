from requests import create_request, find_request


requests = []

create_request(
    requests,
    "Покупка ноутбуков",
    180000,
    "ООО Техно"
)

create_request(
    requests,
    "Покупка мониторов",
    90000,
    "ООО Монитор"
)

request = find_request(requests, 2)

if request:
    print("Заявка найдена:")
    print(request)
else:
    print("Заявка не найдена")