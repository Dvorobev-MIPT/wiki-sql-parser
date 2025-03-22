import time
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
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

class subjects(parser, attribute_getter):
    def __init__(self, main_link, load_time):
        self.main_link = main_link
        self.load_time = load_time
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
        self.driver = webdriver.Chrome(options = chrome_options)  # Инициализируем драйвер один раз\

    def _get_teachers_names(self):
        try:
            elements = WebDriverWait(self.driver, 0.1).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".gallerytext p a"))
            )
            names = [element.text for element in elements]
            return names
        except TimeoutException:
            return []
        except NoSuchElementException:
            return []

    def _put_subjects_in_table(self, link):
        # Открываем страницу
        self.driver.get(link)
        time.sleep(self.load_time)

        print(self.driver.find_element(By.ID, 'firstHeading').text) # name
        print(self._get_maybe_none_attr('Читается на кафедрах'))
        #print(self._get_description())
        print(self._get_teachers_names())


    def put_all_subjects_in_table(self):
        links = self.parse_links()
        for link in links:         # цикл по всем ссылкам на преподавателей
            self._put_subjects_in_table(link)
        self.driver.quit()