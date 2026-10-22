
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    amount INTEGER NOT NULL,
    contractor TEXT NOT NULL,
    employee_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'Создана',

    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

CREATE TABLE IF NOT EXISTS approvals (
    id INTEGER PRIMARY KEY,
    request_id INTEGER NOT NULL,
    employee_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'Ожидает решения',

    FOREIGN KEY (request_id) REFERENCES requests(id),
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

CREATE TABLE IF NOT EXISTS decisions (
    id INTEGER PRIMARY KEY,
    approval_id INTEGER NOT NULL,
    result TEXT NOT NULL,
    comment TEXT NOT NULL,

    FOREIGN KEY (approval_id) REFERENCES approvals(id)
);
