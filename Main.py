import psycopg2

import Teachers
import Departaments
import Subjects
import SQL_functions

# поля для ввода данных
conn = psycopg2.connect(
    database="phystech_wiki",
    user="postgres",
    password="Slash1965",
    host="localhost",
    port="5432"
)

long_load_time = 0.5    # для страниц преподавателей (min 0.5 !!!)
load_time = 0.1         # для остальных страниц
# конец полей для ввода данных


# создадим таблицы

print("Во время парсинга НЕ ВЫКЛЮЧАЙТЕ компьютер и интернет")
SQL_functions.create_tables(conn)
SQL_functions.clear_tables(conn)
print("Таблица успешно была создана/найдена")
print()

dep = Departaments.departments(conn, "https://wiki.mipt.tech/index.php/Категория:Кафедры_по_алфавиту", load_time)
dep.put_all_departments_in_table()
print()

subj = Subjects.subjects(conn, "https://wiki.mipt.tech/index.php/Категория:Предметы_по_алфавиту", load_time)
subj.put_all_subjects_in_table()
print()

teach = Teachers.teachers(conn, "https://wiki.mipt.tech/index.php/Категория:Преподаватели_по_алфавиту", long_load_time)
teach.put_all_teachers_in_table()

conn.close()
