import random
import psycopg2
from prettytable import PrettyTable
from faker import Faker

# Підключення до PostgreSQL
connection = psycopg2.connect(
    dbname="hr_db", user="user", password="password", host="localhost", port="5432"
)
cursor = connection.cursor()
fake = Faker()
Faker.seed(0)


def init_db(cursor, connection):
    # Створення таблиць

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS Departments (
        department_id SERIAL PRIMARY KEY,
        department_name VARCHAR(255) NOT NULL,
        phone CHAR(35) NOT NULL,
        room_number INT CHECK (room_number BETWEEN 701 AND 710)
    );

    CREATE TABLE IF NOT EXISTS Positions (
        position_id SERIAL PRIMARY KEY,
        position_name VARCHAR(255) NOT NULL,
        salary NUMERIC(10, 2) NOT NULL,
        bonus_percent NUMERIC(5, 2) DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS Projects (
        project_id SERIAL PRIMARY KEY,
        project_name VARCHAR(255) NOT NULL,
        deadline DATE NOT NULL,
        budget NUMERIC(15, 2) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Employees (
        employee_id SERIAL PRIMARY KEY,
        last_name VARCHAR(255) NOT NULL,
        first_name VARCHAR(255) NOT NULL,
        middle_name VARCHAR(255),
        address VARCHAR(255),
        phone CHAR(35),
        education VARCHAR(50) CHECK (education IN ('Special', 'Secondary', 'Higher')),
        department_id INT REFERENCES Departments(department_id) ON DELETE SET NULL,
        position_id INT REFERENCES Positions(position_id) ON DELETE SET NULL
    );

    CREATE TABLE IF NOT EXISTS ProjectExecution (
        execution_id SERIAL PRIMARY KEY,
        project_id INT REFERENCES Projects(project_id) ON DELETE CASCADE,
        department_id INT REFERENCES Departments(department_id) ON DELETE CASCADE,
        start_date DATE NOT NULL
    );
    """
    )
    connection.commit()

    print("Таблиці створено успішно!")


def insert_departments(cursor):
    departments = [
        ("Programming", "701"),
        ("Design", "702"),
        ("IT Support", "703"),
    ]
    for name, room in departments:
        phone = fake.phone_number()
        cursor.execute(
            """
            INSERT INTO Departments (department_name, phone, room_number)
            VALUES (%s, %s, %s)
        """,
            (name, phone, room),
        )


def insert_positions(cursor):
    positions = [
        ("Engineer", 2500, 10),
        ("Editor", 1800, 5),
        ("Programmer", 3000, 15),
    ]
    for title, salary, bonus_percent in positions:
        cursor.execute(
            """
            INSERT INTO Positions (position_name, salary, bonus_percent)
            VALUES (%s, %s, %s)
        """,
            (title, salary, bonus_percent),
        )


def insert_employees(cursor):
    for _ in range(17):
        first_name = fake.first_name()
        last_name = fake.last_name()
        middle_name = fake.first_name()
        address = fake.address()
        phone = fake.phone_number()
        education = random.choice(["Special", "Secondary", "Higher"])
        department_id = random.randint(1, 3)  # Assuming 3 departments
        position_id = random.randint(1, 3)  # Assuming 3 positions
        cursor.execute(
            """
            INSERT INTO Employees (first_name, last_name, middle_name, address, phone, education, department_id, position_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
            (
                first_name,
                last_name,
                middle_name,
                address,
                phone,
                education,
                department_id,
                position_id,
            ),
        )


def insert_projects(cursor):
    for _ in range(8):
        project_name = fake.catch_phrase()
        deadline = fake.date_between(start_date="+30d", end_date="+365d")
        budget = random.randint(10000, 100000)
        cursor.execute(
            """
            INSERT INTO Projects (project_name, deadline, budget)
            VALUES (%s, %s, %s)
        """,
            (project_name, deadline, budget),
        )


def insert_project_execution(cursor):
    for _ in range(10):
        project_id = random.randint(1, 8)  # Assuming 8 projects
        department_id = random.randint(1, 3)  # Assuming 3 departments
        start_date = fake.date_between(start_date="-365d", end_date="today")
        cursor.execute(
            """
            INSERT INTO ProjectExecution (project_id, department_id, start_date)
            VALUES (%s, %s, %s)
        """,
            (project_id, department_id, start_date),
        )


def fill_tables(cursor, connection):
    try:
        insert_departments(cursor)
        insert_positions(cursor)
        insert_employees(cursor)
        insert_projects(cursor)
        insert_project_execution(cursor)
        connection.commit()
        print("Дані успішно додано до бази.")
    except Exception as e:
        connection.rollback()
        print("Помилка при додаванні даних:", e)


def drop_tables(cursor, connection):
    cursor.execute(
        """
    DROP TABLE IF EXISTS ProjectExecution;
    DROP TABLE IF EXISTS Projects;
    DROP TABLE IF EXISTS Employees;
    DROP TABLE IF EXISTS Positions;
    DROP TABLE IF EXISTS Departments;
"""
    )
    connection.commit()
    print("Таблиці успішно видалено.")


def print_table(description, rows):
    table = PrettyTable()
    table.field_names = [desc[0] for desc in description]
    for row in rows:
        table.add_row(row)
    print(table)


def print_tables(cursor):
    # Виведення всіх таблиць
    tables = ["Departments", "Positions", "Projects", "Employees", "ProjectExecution"]
    for table in tables:
        cursor.execute(f"SELECT * FROM {table}")
        print(f"Таблиця: {table}")
        print_table(cursor.description, cursor.fetchall())
