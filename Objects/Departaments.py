import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from alive_progress import alive_bar

from Parser.Parser import parser
from Parser.Attribute_getter import attribute_getter

class departments(parser, attribute_getter):
    def __init__(self, conn, main_link, load_time):
        self.conn = conn
        self.main_link = main_link
        self.load_time = load_time
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
        self.driver = webdriver.Chrome(options = chrome_options)  # Инициализируем драйвер один раз

    def _get_site_url(self):
        try:
            next_page = WebDriverWait(self.driver, 0.2).until(
                EC.presence_of_element_located((By.LINK_TEXT, 'Сайт кафедры'))
            )
            next_page_url = next_page.get_attribute('href')
        except:
            next_page_url = None

    def _get_teachers_name(self, id):
        try:
            main_span = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, id))
            )

            # Находим родительский элемент (например, div), который содержит нужные ссылки
            parent_div = main_span.find_element(By.XPATH, './following::div[1]')  # Изменено на 'following::div[1]'

            # Находим все элементы <a> внутри родительского div
            links = parent_div.find_elements(By.TAG_NAME, 'a')

            # Извлекаем и выводим значения атрибута title
            titles = [link.get_attribute('title') for link in links]

            # Извлекаем и выводим значения атрибута title

            titles = [link.get_attribute('title') for link in links if link.get_attribute('title') != '']
            if (len(titles) > 0):
                return titles
            else:
                return None
        except NoSuchElementException:
            return None

    def _put_departments_in_table(self, link):
        # Открываем страницу
        self.driver.get(link)
        time.sleep(self.load_time)

        self.name = self.driver.find_element(By.ID, 'firstHeading').text
        self.type = self._get_maybe_none_attr('Тип')
        self.faculty = self._get_maybe_none_attr('Факультет')
        self.leader = self._get_maybe_none_attr('Заведующий кафедрой')
        self.website = self._get_site_url()
        self._get_subjects_list_by_css('ul.smw-format li.smw-row a')


        self.base_organizations = self._get_maybe_none_attr("Базовая организация")



    def _insert_department(self):
        query = """
        INSERT INTO departments (name, type, leader, website, faculty, base_organizations)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING department_id;
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query, (self.name, self.type, self.leader, self.website, self.faculty, self.base_organizations))
            self.department_id = cursor.fetchone()[0]
            self.conn.commit()

    def put_all_departments_in_table(self):
        links = self.parse_links()
        print("Парсинг страниц кафедр (займет не более 2 минут)")
        with alive_bar(len(links), force_tty=True) as bar:
            for link in links:         # цикл по всем ссылкам на преподавателей
                self._put_departments_in_table(link)
                self._insert_department()
                bar()
        self.driver.quit()