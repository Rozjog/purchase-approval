from datetime import date


request_title = 'Закупка ноутбуков для отдела разработки'
request_amount = 180000.0
contractor = 'ООО ТехноСнаб'
user_role = 'Руководитель'
department_budget = 250000.0
request_date = date.today()

def create_request(title, amount, contractor_name):
    if len(title) > 0 and amount > 0 and len(contractor_name) > 0:
        return 'Заявка успешно создана'
    return 'Ошибка: заявка не может быть создана'


def approve_request(amount, budget, role):
    if amount <= 50000:
        return 'Автоматическое одобрение'
    elif amount <= budget and role == 'Руководитель':
        return 'Согласовано руководителем отдела'
    elif amount > budget and role == 'Финдиректор':
        return 'Согласовано финансовым директором'
    elif amount > budget:
        return 'Требуется согласование финдиректора'
    return 'Ожидает решения руководителя'


def check_budget(budget, amount):
    budget_after = budget - amount
    if budget_after >= 0:
        return f'Заявка в пределах бюджета. Остаток: {budget_after} руб.'
    return f'Превышение бюджета на {abs(budget_after)} руб.'


print(f"Дата заявки: {request_date}")
print(f"Заявка: {request_title}")
print(f"Контрагент: {contractor}")
print(f"Сумма: {request_amount} руб.")
print(f"Роль пользователя: {user_role}")
print()

print("Создание заявки")
print(create_request(request_title, request_amount, contractor))
print()

print("Согласование заявки")
print(approve_request(request_amount, department_budget, user_role))
print()

print("Контроль бюджета")
print(check_budget(department_budget, request_amount))