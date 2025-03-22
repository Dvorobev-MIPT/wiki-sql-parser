import psycopg2

import Teachers
import Parser
import Departaments
import Subjects


conn = psycopg2.connect(
    database="phystech_wiki",
    user="postgres",
    password="Slash1965",
    host="localhost",
    port="5432"
)

# Создание курсора
cur = conn.cursor()

# Функция для создания таблиц, если они не существуют
def create_table_if_not_exists(create_table_sql):
    try:
        cur.execute(create_table_sql)
        conn.commit()
    except psycopg2.Error as e:
        print(f"Ошибка при создании таблицы: {e}")

# SQL для создания таблиц с проверкой существования
create_tables = """
CREATE TABLE IF NOT EXISTS departments (
    department_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    leader TEXT,
    website TEXT,
    faculty TEXT,
    base_organizations TEXT
);

CREATE TABLE IF NOT EXISTS subjects (
    subject_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    department_id INTEGER REFERENCES departments(department_id)
);

CREATE TABLE IF NOT EXISTS teachers (
    teacher_id SERIAL PRIMARY KEY,
    name TEXT,
    birth_date DATE,
    alma_mater TEXT, 
    graduation_year DATE,
    degree TEXT,
    department_id INTEGER REFERENCES departments(department_id),
    subject_id INTEGER REFERENCES subjects(subject_id),
    knowledge_score DECIMAL(3, 2),
    teaching_skill_score DECIMAL(3, 2),
    communication_score DECIMAL(3, 2),
    leniency_score DECIMAL(3, 2),
    overall_score DECIMAL(3, 2),
    knowledge_rating_num SMALLINT,
    teaching_skill_rating_num SMALLINT,
    communication_rating_num SMALLINT,
    leniency_rating_num SMALLINT,
    overall_rating_num SMALLINT
);

CREATE TABLE IF NOT EXISTS subject_teacher (
    subject_id INTEGER REFERENCES subjects(subject_id),
    teacher_id INTEGER REFERENCES teachers(teacher_id),
    PRIMARY KEY (subject_id, teacher_id)
);

CREATE TABLE IF NOT EXISTS department_teacher (
    department_id INTEGER REFERENCES departments(department_id),
    teacher_id INTEGER REFERENCES teachers(teacher_id),
    PRIMARY KEY (department_id, teacher_id)
);

CREATE TABLE IF NOT EXISTS department_subject (
    department_id INTEGER REFERENCES departments(department_id),
    subject_id INTEGER REFERENCES subjects(subject_id),
    PRIMARY KEY (department_id, subject_id)
);
"""

# Запуск создания таблиц
create_table_if_not_exists(create_tables)

# Закрытие курсора и соединения
cur.close()
    conn.close()

    print("CREATE TABLETS")
    #Parser.Parser("https://wiki.mipt.tech/index.php/Категория:Преподаватели_по_алфавиту").parse_links()


    #t = Teachers.teachers("https://wiki.mipt.tech/index.php/Категория:Преподаватели_по_алфавиту", 0)
    #t.put_all_teachers_in_table()
    #t = Departaments.departments("https://wiki.mipt.tech/index.php/Категория:Кафедры_по_алфавиту", 0.2)
    #t.put_all_departments_in_table()
t = Subjects.subjects("https://wiki.mipt.tech/index.php/Категория:Предметы_по_алфавиту", 0.2)
t.put_all_subjects_in_table()

