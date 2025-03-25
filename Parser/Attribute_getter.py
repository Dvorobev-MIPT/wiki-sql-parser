from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import re


class attribute_getter():
    def __init__(self, main_link, load_time):
        self.main_link = main_link
        self.load_time = load_time

        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
        self.driver = webdriver.Chrome(options = chrome_options)  # Инициализируем драйвер один раз

    def _get_maybe_none_attr(self, text):
        try:
            attr_header = self.driver.find_element(By.XPATH, f'//th[normalize-space(text())="{text}"]')
            return attr_header.find_element(By.XPATH, 'following-sibling::td').text
        except NoSuchElementException:
            return None
    '''
    def _get_description(self):
        try:
            # Ждем, пока элемент <p> будет доступен
            paragraph = WebDriverWait(self.driver, 0.5).until(
                EC.presence_of_element_located((By.TAG_NAME, "p"))
            )
            return paragraph.text
        except NoSuchElementException:
            return None
    '''
    def _get_subjects_list_by_css(self, css_selector):
        # Найти все элементы <a> в списке с классом 'smw-format ul-format'
        links = self.driver.find_elements(By.CSS_SELECTOR, css_selector)

        # Извлечь атрибут title из каждого элемента <a>
        subjects = [link.get_attribute('title') for link in links]

        if (len(subjects) > 0):
            return subjects
        else:
            return None

    def _get_estimation(self, text):
        try:
            data = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'div[data-contest="{text}"]'))
            )
            pattern_assessment = re.compile(r'\d+\.\d{2}')
            pattern_count = re.compile(r'\(\d+\)')

            estimation = float(re.findall(pattern_assessment, data.text)[0])
            estimations_count = int(re.findall(pattern_count, data.text)[0][1:-1])
            return estimation, estimations_count
        except Exception:
            return None, 0
