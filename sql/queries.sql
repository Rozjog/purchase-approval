1. Список сотрудников
SELECT
    id,
    name,
    role
FROM employees
ORDER BY name;


2. Информация о конкретном сотруднике
SELECT
    id,
    name,
    role
FROM employees
WHERE id = 1;


3. Список заявок с именами сотрудников
SELECT
    requests.id,
    requests.name,
    requests.amount,
    requests.contractor,
    requests.status,
    employees.name AS employee_name
FROM requests
JOIN employees
    ON requests.employee_id = employees.id
ORDER BY requests.id;


4. Поиск заявок по минимальной сумме
SELECT
    requests.id,
    requests.name,
    requests.amount,
    requests.contractor,
    requests.status,
    employees.name AS employee_name
FROM requests
JOIN employees
    ON requests.employee_id = employees.id
WHERE requests.amount >= 10000
ORDER BY requests.id;


5. Поиск заявок по статусу
SELECT
    requests.id,
    requests.name,
    requests.amount,
    requests.contractor,
    requests.status,
    employees.name AS employee_name
FROM requests
JOIN employees
    ON requests.employee_id = employees.id
WHERE requests.status = 'Одобрена'
ORDER BY requests.id;


6. Информация о конкретной заявке
SELECT
    requests.id,
    requests.name,
    requests.amount,
    requests.contractor,
    requests.status,
    employees.name AS employee_name
FROM requests
JOIN employees
    ON requests.employee_id = employees.id
WHERE requests.id = 1;


7. Список согласований
SELECT
    approvals.id,
    approvals.status,
    requests.name AS request_name,
    requests.amount AS request_amount,
    employees.name AS approver_name
FROM approvals
JOIN requests
    ON approvals.request_id = requests.id
JOIN employees
    ON approvals.employee_id = employees.id
ORDER BY approvals.id;


8. Информация о конкретном согласовании
SELECT
    approvals.id,
    approvals.status,
    requests.name AS request_name,
    requests.amount AS request_amount,
    employees.name AS approver_name
FROM approvals
JOIN requests
    ON approvals.request_id = requests.id
JOIN employees
    ON approvals.employee_id = employees.id
WHERE approvals.id = 1;


9. Список решений
SELECT
    decisions.id,
    decisions.approval_id,
    decisions.result,
    decisions.comment,
    requests.name AS request_name,
    requests.amount AS request_amount
FROM decisions
JOIN approvals
    ON decisions.approval_id = approvals.id
JOIN requests
    ON approvals.request_id = requests.id
ORDER BY decisions.id;


10. Информация о конкретном решении
SELECT
    decisions.id,
    decisions.approval_id,
    decisions.result,
    decisions.comment,
    requests.name AS request_name,
    requests.amount AS request_amount
FROM decisions
JOIN approvals
    ON decisions.approval_id = approvals.id
JOIN requests
    ON approvals.request_id = requests.id
WHERE decisions.id = 1;


11. Общее количество заявок
SELECT
    COUNT(*) AS requests_count
FROM requests;


12. Общая сумма заявок
SELECT
    SUM(amount) AS total_amount
FROM requests;


13. Количество заявок по статусам
SELECT
    status,
    COUNT(*) AS requests_count
FROM requests
GROUP BY status
ORDER BY requests_count DESC;


14. Количество согласований по статусам
SELECT
    status,
    COUNT(*) AS approvals_count
FROM approvals
GROUP BY status
ORDER BY approvals_count DESC;


15. Пять самых дорогих заявок
SELECT
    id,
    name,
    amount
FROM requests
ORDER BY amount DESC
LIMIT 5 OFFSET 0;


16. HAVING: статусы, по которым создано не менее 2 заявок
SELECT
    status,
    COUNT(*) AS requests_count
FROM requests
GROUP BY status
HAVING COUNT(*) >= 2
ORDER BY requests_count DESC;
