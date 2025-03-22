import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from Parser import parser
from Attribute_getter import attribute_getter

# добавить исключения все
# залогинить их
# и останосить программу
# кроме "хороших" except

class departments(parser, attribute_getter):
    def __init__(self, main_link, load_time):
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
        print(next_page_url)

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

        print(self.driver.find_element(By.ID, 'firstHeading').text) # name
        print(self._get_maybe_none_attr('Тип'))
        print(self._get_maybe_none_attr('Факультет'))
        print(self._get_maybe_none_attr('Заведующий кафедрой'))
        print(self._get_site_url())
        print(self._get_subjects_list_by_css('ul.smw-format li.smw-row a')) # subjects
        print(self._get_teachers_name("Преподаватели_кафедры"))
        print(self._get_teachers_name("Бывшие_преподаватели_кафедры"))
        print(self._get_maybe_none_attr("Базовая организация"))

       # print('Знания:', self._get_estimation('expert'))
       # print('Умение преподавать:', self._get_estimation('instructor'))
       # print('В общении:', self._get_estimation('communication'))
       # print('Халявность:', self._get_estimation('freebie'))
       # print('Общая оценка:', self._get_estimation('total'))

    def put_all_departments_in_table(self):
        links = self.parse_links()
        for link in links:         # цикл по всем ссылкам на преподавателей
            self._put_departments_in_table(link)
        self.driver.quit()