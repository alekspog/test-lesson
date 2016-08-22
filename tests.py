import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


url = "https://stepic.org/lesson/%D0%9A%D0%B0%D0%BA-%D0%B8%D0%B3%D1%80%D0%B0%D1%82%D1%8C-%D0%B8%D0%BD%D1%82%D1%80%D0%BE-%D0%B8%D0%B7-Stairway-to-Heaven-%D0%BD%D0%B0-%D1%83%D0%BA%D1%83%D0%BB%D0%B5%D0%BB%D0%B5-31049/step/3"
username = "liakhulia@gmail.com"
password = "512345"
path_to_chromedriver = "C://chromedriver"
test_text = "Answer below"

class LessonEdit(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(path_to_chromedriver)
        #self.driver = webdriver.Firefox()
    def open_lesson_to_edit(self):
        driver = self.driver
        driver.get(url)
        driver.implicitly_wait(10)

        elem = driver.find_element_by_xpath('//*[@class = "introjs-button introjs-skipbutton"]')
        elem.click()

        alert = driver.switch_to.alert
        alert.accept()
        print("alert accepted")

        time.sleep(2)
        login = driver.find_element_by_xpath('//*[@class = "navbar"]/div[2]/a[1]')
        login.click()

        login_field = driver.find_element_by_id('id_login')
        login_field.send_keys(username)
        password_field = driver.find_element_by_id('id_password')
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)


        edit = driver.find_element_by_xpath('//*[@class = "lesson-header__buttons"]/a[1]')
        edit.click()

    def restore_correst_option(self):
        driver = self.driver

        driver.execute_script("window.scrollTo(0,  0)")  # hardcoded
        edit = driver.find_element_by_xpath('//*[@class = "lesson-header__buttons"]/a[1]')
        edit.click()


        checkbox1 = driver.find_element_by_xpath('(//*[@class = "s-checkbox__border"])[5]')
        checkbox2 = driver.find_element_by_xpath('(//*[@class = "s-checkbox__border"])[3]')

        save = driver.find_element_by_xpath('//*[@class="lesson-editor__complete-actions"]/button[1]')

        driver.execute_script("window.scrollTo(0,  810)")           #hardcoded

        checkbox1.click()
        checkbox2.click()
        save.click()

    def restore_textfield(self):
        driver = self.driver
        driver.execute_script("window.scrollTo(0,  0)")  # hardcoded
        edit = driver.find_element_by_xpath('//*[@class = "lesson-header__buttons"]/a[1]')
        edit.click()

        textfield = driver.find_element_by_xpath('//*[@class="wysihtml5-textarea step-text-wrapper wysi-textarea__body theory"]')
        for i in range (len(test_text)):
            textfield.send_keys(Keys.BACK_SPACE)


    def test_correct_answer(self):
        self.open_lesson_to_edit()
        print ("Testing correct option")
        driver = self.driver

        checkbox1 = driver.find_element_by_xpath('(//*[@class = "s-checkbox__border"])[5]')
        checkbox2 = driver.find_element_by_xpath('(//*[@class = "s-checkbox__border"])[3]')

        save = driver.find_element_by_xpath('//*[@class="lesson-editor__complete-actions"]/button[1]')

        driver.execute_script("window.scrollTo(0,  810)")           #hardcoded

        checkbox1.click()
        checkbox2.click()
        save.click()

        start = driver.find_element_by_xpath('(//*[@class = "attempt__actions"])/button[1]')

        start.click()
        time.sleep(1)
        driver.execute_script("window.scrollTo(0,  315)")  # hardcoded

        option = driver.find_element_by_xpath('(//*[@class = "s-radio__border"])[1]')

        option.click()
        submit = driver.find_element_by_xpath('//*[@class = "submit-submission"]')

        submit.click()
        try:
            correct = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@class = "attempt-wrapper__result-icon ember-view svg-icon correct_icon"]'))
            )
        except:
            self.fail("Incorrect answer")

        self.restore_correst_option()

    def test_edit_text(self):
        self.open_lesson_to_edit()
        print("Testing text editing")

        driver = self.driver

        textfield = driver.find_element_by_xpath('//*[@class="wysihtml5-textarea step-text-wrapper wysi-textarea__body theory"]')

        textfield.send_keys("Answer below")

        assert "below" in textfield.text

        elem = driver.find_element_by_xpath('//*[@class="lesson-editor__complete-actions"]/button[1]')
        elem.click()

        textfield = driver.find_element_by_xpath('//*[@class="ember-view step-text-wrapper"]')
        assert "below" in textfield.text

        self.restore_textfield()

    def test_too_many_options(self):
        self.open_lesson_to_edit()
        print ("Testing quiz options. Too many options warning.")
        driver = self.driver
        checkbox = driver.find_element_by_xpath('(//*[@class = "s-checkbox__border"])[3]')

        driver.execute_script("window.scrollTo(0,  810)")           #hardcoded


        checkbox.click()


        save = driver.find_element_by_xpath('//*[@class="lesson-editor__complete-actions"]/button[1]')
        save.click()

        try:
            warning =  driver.find_element_by_xpath('//*[@class = "s-hint s-hint_warning"]')

        except:
            self.fail ("Warning is not displayed")


        try:
            error =  driver.find_element_by_xpath('//*[@class = "error"]')
        except:
            self.fail("Error is not displayed")


    def test_no_options(self):
        self.open_lesson_to_edit()
        print("Testing quiz options. No options selected.")

        driver = self.driver
        checkbox = driver.find_element_by_xpath('(//*[@class = "s-checkbox__border"])[5]')

        driver.execute_script("window.scrollTo(0,  810)")           #hardcoded
        checkbox.click()

        save = driver.find_element_by_xpath('//*[@class="lesson-editor__complete-actions"]/button[1]')
        save.click()

        try:
            warning = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@class = "s-hint s-hint_warning"]'))
            )

        except:
            self.fail ("Warning is not displayed")


        try:
            error = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@class = "error"]'))
            )

        except:
            self.fail("Error is not displayed")


        try:
             WebDriverWait(driver, 10).until(
                EC.alert_is_present()
            )
             alert = driver.switch_to.alert
             alert.accept()
        except:
            print("No alert is present")



    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()