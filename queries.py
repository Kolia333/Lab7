from db import connection, cursor, print_table


def query_1(cursor):
    cursor.execute(
        """
        SELECT e.last_name, e.first_name, e.middle_name, p.salary
        FROM Employees e
        JOIN Positions p ON e.position_id = p.position_id
        WHERE p.salary > 2000
        ORDER BY e.last_name;
    """
    )

    print_table(cursor.description, cursor.fetchall())


def query_2(cursor):
    cursor.execute(
        """
        SELECT d.department_name, AVG(p.salary) AS average_salary
FROM Employees e
JOIN Positions p ON e.position_id = p.position_id
JOIN Departments d ON e.department_id = d.department_id
GROUP BY d.department_name;

    """
    )
    print_table(cursor.description, cursor.fetchall())


def query_3(cursor, department_id: int):
    cursor.execute(
        """
SELECT pr.project_name, pe.start_date
FROM Projects pr
JOIN ProjectExecution pe ON pr.project_id = pe.project_id
WHERE pe.department_id = %s;
""",
        ((department_id,)),
    )
    print_table(cursor.description, cursor.fetchall())


def query_4(cursor):
    cursor.execute(
        """
SELECT e.last_name, e.first_name, e.middle_name,
       p.salary,
       (p.salary * p.bonus_percent / 100) AS bonus
FROM Employees e
JOIN Positions p ON e.position_id = p.position_id;
"""
    )
    print_table(cursor.description, cursor.fetchall())


def query_4(cursor):
    cursor.execute(
        """
SELECT d.department_name, COUNT(e.employee_id) AS employee_count
FROM Departments d
LEFT JOIN Employees e ON d.department_id = e.department_id
GROUP BY d.department_name;
"""
    )
    print_table(cursor.description, cursor.fetchall())


def query_5(cursor):
    cursor.execute(
        """
SELECT e.last_name, e.first_name, e.middle_name,
       p.salary,
       (p.salary * p.bonus_percent / 100) AS bonus
FROM Employees e
JOIN Positions p ON e.position_id = p.position_id;

"""
    )
    print_table(cursor.description, cursor.fetchall())


def query_6(cursor):
    cursor.execute(
        """
SELECT d.department_name,
       e.education,
       COUNT(e.employee_id) AS employee_count
FROM Departments d
JOIN Employees e ON d.department_id = e.department_id
GROUP BY d.department_name, e.education
ORDER BY d.department_name, e.education;
"""
    )
    print_table(cursor.description, cursor.fetchall())
