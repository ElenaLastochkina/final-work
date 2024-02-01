from selenium import webdriver
import yaml


class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.locators = self.load_locators()

    def load_locators(self):
        with open('locators.yaml') as file:
            locators = yaml.load(file, Loader=yaml.FullLoader)
        return locators

    def login(self, username, password):
        login_input = self.driver.find_element_by_id(self.locators['login_input'])
        password_input = self.driver.find_element_by_id(self.locators['password_input'])
        submit_button = self.driver.find_element_by_id(self.locators['submit_button'])

        login_input.send_keys(username)
        password_input.send_keys(password)
        submit_button.click()

    def click_about_link(self):
        about_link = self.driver.find_element_by_xpath(self.locators['about_link'])
        about_link.click()


class AboutPage:
    def __init__(self, driver):
        self.driver = driver
        self.locators = self.load_locators()

    def load_locators(self):
        with open('locators.yaml') as file:
            locators = yaml.load(file, Loader=yaml.FullLoader)
        return locators

    def get_opened_window_title_font_size(self):
        opened_window_title = self.driver.find_element_by_css_selector(self.locators['opened_window_title'])
        font_size = opened_window_title.value_of_css_property('font-size')
        return font_size


if __name__ == "__main__":
    # Открываем браузер Google Chrome
    driver = webdriver.Chrome()

    # Инициализируем страницы
    main_page = MainPage(driver)
    about_page = AboutPage(driver)

    # Переходим на страницу входа
    driver.get('https://test-stand.gb.ru')

    # Функция проверки шрифта заголовка окна
    def check_font_size(font_size):
        assert font_size == '32px', f"Размер шрифта: {font_size}, ожидалось 32px"

    # Тест 1: Логин на сайт
    main_page.login("autotest", "4956318935")

    # Проверяем, что логин выполнен успешно
    check_font_size(driver.current_url, "https://test-stand.gb.ru/successful_login")

    # Тест 2: Клик по ссылке "About"
    main_page.click_about_link()

    # Проверяем, что открыто окно "About"
    check_font_size(driver.current_url, "https://test-stand.gb.ru/about")

    # Тест 3: Проверка размера шрифта заголовка окна
    font_size = about_page.get_opened_window_title_font_size()
    check_font_size(font_size)

    # Закрываем браузер
    driver.quit()