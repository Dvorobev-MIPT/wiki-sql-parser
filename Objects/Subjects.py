import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from alive_progress import alive_bar


from SQL_function import SQL_functions
from Parser.Parser import parser
from Parser.Attribute_getter import attribute_getter


class subjects(parser, attribute_getter):
    def __init__(self, conn, main_link, load_time):
        self.conn = conn
        self.main_link = main_link
        self.load_time = load_time
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
        self.driver = webdriver.Chrome(options = chrome_options)  # Инициализируем драйвер один раз\


    def _put_subjects_in_table(self, link):
        # Открываем страницу
        self.driver.get(link)
        time.sleep(self.load_time)

        self.name = self.driver.find_element(By.ID, 'firstHeading').text
        self.depatments = self._get_maybe_none_attr('Читается на кафедрах')

    def _insert_subject(self):
        query = """
        INSERT INTO subjects (name)     
        VALUES (%s)
        RETURNING subject_id;
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query, (self.name,))
            self.subject_id = cursor.fetchone()[0]
            self.conn.commit()

    def _insert_department_subject(self):
        query = """
        INSERT INTO department_subject (department_id, subject_id)
        VALUES (%s, %s)
        ON CONFLICT (department_id, subject_id) DO NOTHING;
        """
        with self.conn.cursor() as cursor:
            department_id = SQL_functions.get_pk_by_column_value(self.conn, "departments",
                                                                         "department_id","name", self.depatments)
            if (department_id):
                cursor.execute(query, (department_id, self.subject_id))
                self.conn.commit()

    def put_all_subjects_in_table(self):
        links = self.parse_links()
        print("Парсинг страниц предметов (займет не более 2 минут)")
        with alive_bar(len(links), force_tty=True) as bar:
            for link in links:         # цикл по всем ссылкам на преподавателей
                bar()
                self._put_subjects_in_table(link)
                self._insert_subject()
                self._insert_department_subject()
        self.driver.quit()
