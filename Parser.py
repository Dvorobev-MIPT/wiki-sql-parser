from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# добавить исключения все
# залогинить их
# и останосить программу
# кроме "хороших" except

class parser:
    def __init__(self, main_link):
        self.main_link = main_link
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
        self.driver = webdriver.Chrome(options = chrome_options)  # Инициализируем драйвер один раз

    def parse_links(self):
        next_page_url = self.main_link
        links = []  # Список для хранения ссылок

        while next_page_url:
            self.driver.get(next_page_url)

            try:
                next_page = WebDriverWait(self.driver, 0.2).until(
                    EC.presence_of_element_located((By.LINK_TEXT, 'Следующая страница'))
                )
                next_page_url = next_page.get_attribute('href')
            except:
                next_page_url = None
            print(next_page_url)

            # Находим элементы, содержащие ссылки на преподавателей
            elements = self.driver.find_elements(By.CLASS_NAME, "mw-category-group")
            for element in elements:
                a_tags = element.find_elements(By.TAG_NAME, "a")
                for a in a_tags:
                    links.append(a.get_attribute("href"))

        # Выводим все ссылки
        for link in links:
            print(link)

        print(len(links))
        return links