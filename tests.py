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


class LessonEdit(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(path_to_chromedriver)
        #self.driver = webdriver.Firefox()
    def open_lesson_to_edit(self):
        driver = self.driver
        driver.get(url)
        print ("Opening lesson to edit")
        try:
            elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, u'Пропустить'))
            )
        except:
            TimeoutException()

        elem.click()


        try:
             WebDriverWait(driver, 10).until(
                EC.alert_is_present()
            )
        except:
            TimeoutException()

        alert = driver.switch_to.alert
        alert.accept()
        print("alert accepted")

        time.sleep(2)
        login = driver.find_element_by_xpath('//*[@class = "navbar"]/div[2]/a[1]')
        login.click()

        try:
            login_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'id_login'))
            )
        except:
            TimeoutException()

        login_field.send_keys(username)
        password_field = driver.find_element_by_id("id_password")
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        try:
            edit = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@title="Редактировать"]'))
            )
        except:
            TimeoutException()

        edit.click()

    def restore_lesson(self):
        driver = self.driver

        driver.execute_script("window.scrollTo(0,  0)")  # hardcoded
        try:
            elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@title="Редактировать"]'))
            )
        except:
            TimeoutException()

        elem.click()

        try:
            checkbox1 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '(//*[@class = "s-checkbox__border"])[5]'))
            )
            checkbox2 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '(//*[@class = "s-checkbox__border"])[3]'))
            )
        except:
            TimeoutException()

        save = driver.find_element_by_xpath('//*[@class="lesson-editor__complete-actions"]/button[1]')
        time.sleep(1)
        driver.execute_script("window.scrollTo(0,  810)")           #hardcoded

        checkbox1.click()
        checkbox2.click()
        save.click()

    def test_correct_answer(self):
        self.open_lesson_to_edit()
        print ("Testing correct option")
        driver = self.driver

        try:
            checkbox1 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '(//*[@class = "s-checkbox__border"])[5]'))
            )
            checkbox2 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '(//*[@class = "s-checkbox__border"])[3]'))
            )
        except:
            TimeoutException()

        save = driver.find_element_by_xpath('//*[@class="lesson-editor__complete-actions"]/button[1]')
        time.sleep(1)
        driver.execute_script("window.scrollTo(0,  810)")           #hardcoded

        checkbox1.click()
        checkbox2.click()
        save.click()
        time.sleep(1)
        try:
            start = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '(//*[@class = "attempt__actions"])/button[1]'))
            )
        finally:

            TimeoutException()

        start.click()
        time.sleep(1)
        driver.execute_script("window.scrollTo(0,  315)")  # hardcoded

        option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '(//*[@class = "s-radio__border"])[1]'))
            )

        option.click()

        try:
            submit = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@class = "submit-submission"]'))
            )
        finally:
            TimeoutException()

        submit.click()
        try:
            correct = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@class = "attempt-wrapper__result-icon ember-view svg-icon correct_icon"]'))
            )
        except:
            self.fail("Incorrect answer")

        self.restore_lesson()

    def test_edit_text(self):
        self.open_lesson_to_edit()
        print("Testing test editing")

        driver = self.driver

        try:
            elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@class="wysihtml5-textarea step-text-wrapper wysi-textarea__body theory"]'))
            )
        except:
            TimeoutException()

        elem.send_keys("Answer below")

        assert "below" in elem.text

        elem = driver.find_element_by_xpath('//*[@class="lesson-editor__complete-actions"]/button[1]')
        elem.click()

        try:
            elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@class="ember-view step-text-wrapper"]'))
            )
        except:
            TimeoutException()

        assert "below" in elem.text

    def test_too_many_options(self):
        self.open_lesson_to_edit()
        print ("Testing quiz options. Too many options warning.")
        driver = self.driver
        try:
            checkbox = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '(//*[@class = "s-checkbox__border"])[3]'))
            )
        except:
            TimeoutException()

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

    def test_no_options(self):
        self.open_lesson_to_edit()
        print("Testing quiz options. No options selected.")
        driver = self.driver

        try:
            checkbox = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '(//*[@class = "s-checkbox__border"])[5]'))
            )

        except:
            TimeoutException()

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