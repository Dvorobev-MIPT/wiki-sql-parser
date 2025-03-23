import psycopg2
import re

'''
В данном файле содержатся все необходимые для работы с SQL функции
'''



# функция разделения строки words(date) на 2 строки words + date, причем date мб None
def extract_strings(input_str):
    # Используем регулярное выражение для поиска строки с датой
    match = re.match(r'^(.*?)(?:\s+\((.*?)\))?', input_str.strip())

    if match:
        str1 = match.group(1).strip()  # Первая строка (все слова до даты)
        str2 = match.group(2) if match.group(2) else None  # Вторая строка (дата или None)
        return str1, str2


# Возвращает значение PK для строки, где значение столбца search_column_name равно search_value
def get_pk_by_column_value(conn, table_name, pk_column_name, search_column_name, search_value):
    query = f"""
       SELECT {pk_column_name}
       FROM {table_name}
       WHERE {search_column_name} = %s;
       """
    with conn.cursor() as cursor:
        cursor.execute(query, (search_value,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

# Функция для создания таблиц, если они не существуют
def create_table_if_not_exists(create_table_sql, conn, cur):
    try:
        cur.execute(create_table_sql)
        conn.commit()
    except psycopg2.Error as e:
        print(f"Ошибка при создании таблицы: {e}")

def create_tables(conn):
    # Создание курсора
    cur = conn.cursor()

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
        name TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS teachers (
        teacher_id SERIAL PRIMARY KEY,
        name TEXT,
        birth_date DATE,
        alma_mater TEXT, 
        graduation_year DATE,
        degree TEXT,
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
    create_table_if_not_exists(create_tables, conn, cur)

    # Закрытие курсора и соединения
    cur.close()

def clear_tables(conn):
    # Создание курсора
    cur = conn.cursor()

    # SQL для очистки таблиц и обнуления PK
    clear_tables_sql = """
    TRUNCATE TABLE department_subject CASCADE;
    TRUNCATE TABLE department_teacher CASCADE;
    TRUNCATE TABLE subject_teacher CASCADE;
    TRUNCATE TABLE teachers CASCADE;
    TRUNCATE TABLE subjects CASCADE;
    TRUNCATE TABLE departments CASCADE;
    
    ALTER SEQUENCE departments_department_id_seq RESTART WITH 1;
    ALTER SEQUENCE subjects_subject_id_seq RESTART WITH 1;
    ALTER SEQUENCE teachers_teacher_id_seq RESTART WITH 1;
    """

    try:
        cur.execute(clear_tables_sql)
        conn.commit()
        print("Все таблицы успешно очищены.")
    except psycopg2.Error as e:
        print(f"Ошибка при очистке таблиц: {e}")

    # Закрытие курсора
    cur.close()