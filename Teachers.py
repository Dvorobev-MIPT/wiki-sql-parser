from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

from Parser import parser
from Attribute_getter import attribute_getter

# добавить исключения все
# залогинить их
# и останосить программу
# кроме "хороших" except

class teachers(parser, attribute_getter):
    def __init__(self, main_link, load_time):
        self.main_link = main_link
        self.load_time = load_time
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
        self.driver = webdriver.Chrome(options = chrome_options)  # Инициализируем драйвер один раз

    def _put_teacher_in_table(self, link):
        # Открываем страницу
        self.driver.get(link)
        time.sleep(self.load_time)

        print(self.driver.find_element(By.ID, 'firstHeading').text) # name
        print(self._get_maybe_none_attr('Учёная степень'))
        print(self._get_maybe_none_attr('Альма-матер'))
        print(self._get_maybe_none_attr('Дата рождения'))
        print(self._get_maybe_none_attr('Работает'))
        print(self._get_maybe_none_attr('Ведёт'))
        print()

        print('Знания:', self._get_estimation('expert'))
        print('Умение преподавать:', self._get_estimation('instructor'))
        print('В общении:', self._get_estimation('communication'))
        print('Халявность:', self._get_estimation('freebie'))
        print('Общая оценка:', self._get_estimation('total'))

    def put_all_teachers_in_table(self):
        links = self.parse_links()
        for link in links:         # цикл по всем ссылкам на преподавателей
            self._put_teacher_in_table(link)
        self.driver.quit()