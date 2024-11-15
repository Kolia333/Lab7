from db import connection, cursor, drop_tables, fill_tables, print_tables, init_db
from queries import *


def menu():
    menu = [
        "Робітники з окладом більше 2000 грн",
        "Середня зарплата по відділах",
        "всі проекти, які виконуються в обраному відділі",
        "Кількість працівників у відділах",
        "Розмір премії кожного працівника",
        "Освіта працівників по відділах",
    ]

    for i in range(len(menu)):
        print(f"{i+1}: {menu[i]}")


def main(cursor):
    menu()
    while True:
        param = input("Введіть номер запиту (q - exit):")
        if param.lower() == "q":
            break
        if param == "1":
            query_1(cursor)
        elif param == "2":
            query_2(cursor)
        elif param == "3":
            dep_id = int(input("Введіть id відділу"))
            query_3(cursor, dep_id)
        elif param == "4":
            query_4(cursor)
        elif param == "5":
            query_5(cursor)
        elif param == "6":
            query_6(cursor)
        else:
            print("Incorrect param")


if __name__ == "__main__":
    init_db(cursor, connection)
    fill_tables(cursor, connection)
    print_tables(cursor)
    main(cursor)

    drop_tables(cursor, connection)
    cursor.close()
    connection.close()
