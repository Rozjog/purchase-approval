SELECT
    id,
    name,
    role
FROM employees
ORDER BY name;


SELECT
    id,
    name,
    amount,
    contractor,
    status
FROM requests
ORDER BY id;


SELECT
    id,
    name,
    amount
FROM requests
WHERE amount >= 10000
ORDER BY amount DESC;


SELECT
    id,
    name,
    status
FROM requests
WHERE status = 'Одобрена';


SELECT
    requests.id,
    requests.name AS request_name,
    requests.amount,
    employees.name AS employee_name
FROM requests
JOIN employees
    ON requests.employee_id = employees.id
ORDER BY requests.id;


SELECT
    approvals.id,
    requests.name AS request_name,
    employees.name AS approver_name,
    approvals.status
FROM approvals
JOIN requests
    ON approvals.request_id = requests.id
JOIN employees
    ON approvals.employee_id = employees.id
ORDER BY approvals.id;


SELECT
    COUNT(*) AS requests_count
FROM requests;


SELECT
    SUM(amount) AS total_amount
FROM requests;


SELECT
    status,
    COUNT(*) AS requests_count
FROM requests
GROUP BY status
ORDER BY requests_count DESC;


SELECT
    status,
    COUNT(*) AS approvals_count
FROM approvals
GROUP BY status
ORDER BY approvals_count DESC;


SELECT
    status,
    COUNT(*) AS requests_count
FROM requests
GROUP BY status
HAVING COUNT(*) >= 1;


SELECT
    id,
    name,
    amount
FROM requests
ORDER BY amount DESC
LIMIT 5 OFFSET 0;
