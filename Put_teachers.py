from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import re

def get_name():
    name = driver.find_element(By.ID, 'firstHeading').text
    return name

def GetMaybeNoneAttr(text):
    try:
        # Найдем элемент <th> с текстом "Учёная степень"
        attr_header = driver.find_element(By.XPATH, '//th[normalize-space(text())="' + text + '"]')
        # Найдем соответствующий <td> элемент
        attr = attr_header.find_element(By.XPATH, 'following-sibling::td').text
    except NoSuchElementException:
        attr = None
    return attr

def get_degree():
    return GetMaybeNoneAttr('Учёная степень')


def get_birth_date():
    return GetMaybeNoneAttr('Дата рождения')

def get_alma_mater():
    return GetMaybeNoneAttr('Альма-матер')

def get_workplace():
    return GetMaybeNoneAttr('Работает')


def get_subject():
    return GetMaybeNoneAttr('Ведёт')


def GetEstimation(text):
    try:
        data = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-contest="' + text + '"]'))
        )
        # Извлекаем текст или атрибуты
        pattern_assessment = re.compile(r'\d.\d{2}')
        pattern_count = re.compile(r'\(\d+\)')

        # Информация

        # Замечание заносить будем со ссылкой на страницу, поскольку тогда заполним строки работает и ведет через SQL
        estimation = float(re.findall(pattern_assessment, data.text)[0])
        estimations_count = int(re.findall(pattern_count, data.text)[0][1:-1])
        return estimation, estimations_count
    except Exception as e:
        return None, 0

def get_knowledge():
    return GetEstimation('expert')

def get_instructor():
    return GetEstimation('instructor')

def get_communication():
    return GetEstimation('communication')

def get_freebie():
    return GetEstimation('freebie')

def get_total():
    return GetEstimation('total')


# Инициализируем веб-драйвер (например, Chrome)
driver = webdriver.Chrome()  # Убедитесь, что у вас установлен драйвер Chrome


# Открываем страницу
driver.get('https://wiki.mipt.tech/index.php/Uyen')
time.sleep(1)

print(get_name())
print(get_degree())
print(get_alma_mater())
print(get_birth_date())
print(get_workplace())
print()
print(get_subject())
print()

# Характеристики (оценки)
print('Знания:', get_knowledge())

print('Умение преподавать:', get_instructor())

print('В общении:', get_communication())

print('Халявность:', get_freebie())

print('Общая оценка:', get_total())

driver.quit()
"""
def PutAllTeachersInTable(links):
    for link in links:
        PutTeacherInTable(link)

def ParseLinks():
    next_page_url = "https://wiki.mipt.tech/index.php?title=Категория:Преподаватели_по_алфавиту"
    links = []  # Cписок для хранения ссылок

    while (next_page_url != None):
        driver = webdriver.Chrome()
        driver.get(next_page_url)
        time.sleep(3)


        try:
            next_page = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.LINK_TEXT, 'Следующая страница'))
            )
            next_page_url = next_page.get_attribute('href')
        except:
            next_page_url = None
        print(next_page_url)

        # Находим элементы, содержащие ссылки на преподавателей
        # Здесь мы ищем элементы с классом 'mw-category-group'
        elements = driver.find_elements(By.CLASS_NAME, "mw-category-group")

        for element in elements:
            # Находим все ссылки внутри текущего элемента
            a_tags = element.find_elements(By.TAG_NAME, "a")
            for a in a_tags:
                links.append(a.get_attribute("href"))  # Получаем ссылку из атрибута href
        driver.quit()

    # Выводим все ссылки
    for link in links:
        print(link)

    print(len(links))
    return links
"""
