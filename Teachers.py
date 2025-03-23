from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from alive_progress import alive_bar


import SQL_functions
from Parser import parser
from Attribute_getter import attribute_getter
from datetime import datetime


class teachers(parser, attribute_getter):
    def __init__(self, conn, main_link, load_time):
        self.conn = conn
        self.main_link = main_link
        self.load_time = load_time
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
        self.driver = webdriver.Chrome(options = chrome_options)  # Инициализируем драйвер один раз


    def _parse_date(self, date_str):
        # Словарь для преобразования названий месяцев
        months = {
            'января': 1,
            'февраля': 2,
            'марта': 3,
            'апреля': 4,
            'мая': 5,
            'июня': 6,
            'июля': 7,
            'августа': 8,
            'сентября': 9,
            'октября': 10,
            'ноября': 11,
            'декабря': 12
        }

        # Разделяем строку на части
        day, month_name, year = date_str.split()

        month = months.get(month_name.lower())
        if not month:
            return date_str

        # Создаем объект datetime
        date_obj = datetime(int(year), month, int(day))

        # Возвращаем дату в формате YYYY-MM-DD
        return date_obj.strftime('%Y-%m-%d')

    def _put_teacher_in_table(self, link):
        # Открываем страницу
        self.driver.get(link)
        time.sleep(self.load_time)

        self.name = self.driver.find_element(By.ID, 'firstHeading').text

        degree = self._get_maybe_none_attr('Учёная степень')
        if (degree):
            self.degree, self.graduation_year = SQL_functions.extract_strings(degree)
        else:
            self.degree, self.graduation_year = None, None

        self.alma_mater = self._get_maybe_none_attr('Альма-матер')

        self.birth_date = self._get_maybe_none_attr('Дата рождения')
        if (self.birth_date):
            self.birth_date = self._parse_date(self.birth_date)

        self.department = self._get_maybe_none_attr('Работает')

        subjects_text = self._get_maybe_none_attr('Ведёт')
        if (subjects_text):
            self.subjects = subjects_text.split('\n')
        else:
            self.subjects = None


        knownledge = self._get_estimation('expert')
        if (knownledge):
            self.knowledge_score, self.knowledge_rating_num = knownledge[0], knownledge[1]
        else:
            self.knowledge_score, self.knowledge_rating_num = None, None

        teachers_skill_score = self._get_estimation('instructor')
        if (teachers_skill_score):
            self.teaching_skill_score, self.teaching_skill_rating_num = teachers_skill_score[0], teachers_skill_score[1]
        else:
            self.teaching_skill_score, self.teaching_skill_rating_num = None, None

        communication_score = self._get_estimation('communication')
        if (communication_score):
            self.communication_score, self.communication_rating_num = communication_score[0], communication_score[1]
        else:
            self.communication_score, self.communication_rating_num = None, None

        leniency_score = self._get_estimation('freebie')
        if (leniency_score):
            self.leniency_score,self. leniency_rating_num = leniency_score[0], leniency_score[1]
        else:
            self.leniency_score, self.leniency_rating_num = None, None

        overall_score = self._get_estimation('total')
        if (overall_score):
            self.overall_score, self.overall_rating_num = overall_score[0], overall_score[1]
        else:
            self.overall_score, self.overall_rating_num = None, None

    # Функция заполнения SQL таблицы  teachers
    def _insert_teacher(self):
        query = """
        INSERT INTO teachers (name, birth_date, alma_mater, graduation_year, degree, knowledge_score, 
                              teaching_skill_score, communication_score, leniency_score, overall_score, knowledge_rating_num, 
                              teaching_skill_rating_num, communication_rating_num, leniency_rating_num, overall_rating_num)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING teacher_id;
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query, (self.name, self.birth_date, self.alma_mater, self.graduation_year, self.degree,
                                   self.knowledge_score, self.teaching_skill_score, self.communication_score,
                                   self.leniency_score, self.overall_score, self.knowledge_rating_num,
                                   self.teaching_skill_rating_num,self.communication_rating_num,
                                   self.leniency_rating_num, self.overall_rating_num))
            self.teacher_id = cursor.fetchone()[0]
            self.conn.commit()

    def _insert_subject_teacher(self):
        query = """
        INSERT INTO subject_teacher (subject_id, teacher_id)
        VALUES (%s, %s)
        ON CONFLICT (subject_id, teacher_id) DO NOTHING;
        """
        with self.conn.cursor() as cursor:
            with self.conn.cursor() as cursor:
                if (self.subjects):
                    for subject in self.subjects:
                        if (subject):
                            subject_id = SQL_functions.get_pk_by_column_value(self.conn, "subjects",
                                                                                 "subject_id", "name", subject)
                            if (subject_id):
                                cursor.execute(query, (subject_id, self.teacher_id))
                                self.conn.commit()

    def _insert_department_teacher(self):
        query = """
        INSERT INTO department_teacher (department_id, teacher_id)
        VALUES (%s, %s)
        ON CONFLICT (department_id, teacher_id) DO NOTHING;
        """
        with self.conn.cursor() as cursor:
            if (self.department):
                department_id = SQL_functions.get_pk_by_column_value(self.conn, "departments", "department_id",
                                                                     "name", self.department)
                if (department_id):
                    cursor.execute(query, (department_id, self.teacher_id))
                    self.conn.commit()

    def put_all_teachers_in_table(self):
        links = self.parse_links()
        print("Парсинг страниц преподавателей (займет не более 40 минут)")
        with alive_bar(len(links), force_tty=True) as bar:
            for link in links:         # цикл по всем ссылкам на преподавателей
                bar()
                self._put_teacher_in_table(link)
                self._insert_teacher()
                self._insert_subject_teacher()
                self._insert_department_teacher()
        self.driver.quit()