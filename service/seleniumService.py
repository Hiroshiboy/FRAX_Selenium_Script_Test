import time
from platform import system
from selenium import webdriver

# This is used for Frax calculations. It creates Chrome Windows and inputs the data
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set logging to info
import logging
logging.basicConfig(level=logging.INFO)


class Selenium_Driver:
    driver = None
    driver_exists = False

    def __init__(self):
        try:
            if system() == "Windows":
                self.driver = webdriver.Chrome(
                    r"C:\Users\alexc\Pictures\Osteoporosis\drivers\chromedriverwindows.exe")
            elif system() == "Linux":
                self.driver = webdriver.Chrome(r"C:\Users\alexc\Pictures\Osteoporosis\drivers\chromedriverlinux.exe")
            elif system() == "Darwin":
                self.driver = webdriver.Chrome(r"C:\Users\alexc\Pictures\Osteoporosis\drivers\chromedrivermac.exe")
            self.driver_exists = True
        except:
            logging.error("Could not find Chrome driver")

    def get_frax_risk_percentage(self, patient_id, gender, age, weight, height, previous_fracture, parent_fractured_hip,
                                 smoking,
                                 alcohol,
                                 diabetes,
                                 arthritis, rxlist, t_score):
        try:

            logging.info("Starting to calculate Frax Risk for patient : %s" % patient_id)

            self.driver.get(
                'https://www.sheffield.ac.uk/FRAX/tool.aspx?country=19')

            # Age
            self.driver.find_element_by_xpath(
                '/html/body/form/div[3]/div[4]/div[1]/div/div[4]/div[2]/div[2]/div[2]/input[1]').send_keys(str(age))

            # Gender
            if gender == 2:
                self.driver.find_element_by_xpath(
                    '/html/body/form/div[3]/div[4]/div[1]/div/div[4]/div[2]/div[3]/div[2]/div[1]/input').click()
            else:
                self.driver.find_element_by_xpath(
                    '/html/body/form/div[3]/div[4]/div[1]/div/div[4]/div[2]/div[3]/div[2]/div[2]/input').click()

            # weight
            self.driver.find_element_by_xpath(
                '/html/body/form/div[3]/div[4]/div[1]/div/div[4]/div[2]/div[4]/div[2]/input[1]').send_keys(
                str(weight))

            # height
            self.driver.find_element_by_xpath(
                '/html/body/form/div[3]/div[4]/div[1]/div/div[4]/div[2]/div[5]/div[2]/input[1]').send_keys(
                str(height))

            # Previous fracture
            if previous_fracture == 0 or previous_fracture == 2:
                self.driver.find_element_by_xpath(
                    '/html/body/form/div[3]/div[4]/div[1]/div/div[4]/div[2]/div[6]/div[2]/div[1]/input').click()
            else:
                self.driver.find_element_by_xpath(
                    '/html/body/form/div[3]/div[4]/div[1]/div/div[4]/div[2]/div[6]/div[2]/div[2]/input').click()

            # Parent fracture
            if parent_fractured_hip == 0 or parent_fractured_hip == 2:
                self.driver.find_element_by_xpath(
                    '/html/body/form/div[3]/div[4]/div[1]/div/div[4]/div[2]/div[7]/div[2]/div[1]/input').click()
            else:
                self.driver.find_element_by_xpath(
                    '/html/body/form/div[3]/div[4]/div[1]/div/div[4]/div[2]/div[7]/div[2]/div[2]/input').click()

            # smoking
            if smoking == 0:
                self.driver.find_element_by_xpath(
                    '/html/body/form/div[3]/div[4]/div[1]/div/div[4]/div[2]/div[8]/div[2]/div[1]/input').click()
            else:
                self.driver.find_element_by_xpath(
                    '/html/body/form/div[3]/div[4]/div[1]/div/div[4]/div[2]/div[8]/div[2]/div[2]/input').click()

            # glucocorticoids
            if rxlist == 13:
                self.driver.find_element_by_xpath(
                    '/html/body/form/div[3]/div[4]/div[1]/div/div[4]/div[2]/div[9]/div[2]/div[1]/input').click()
            else:
                self.driver.find_element_by_xpath(
                    '/html/body/form/div[3]/div[4]/div[1]/div/div[4]/div[2]/div[9]/div[2]/div[2]/input').click()

            # arthritis
            if arthritis == 0:
                self.driver.find_element_by_xpath(
                    '/html/body/form/div[3]/div[4]/div[1]/div/div[4]/div[2]/div[10]/div[2]/div[1]/input').click()
            else:
                self.driver.find_element_by_xpath(
                    '/html/body/form/div[3]/div[4]/div[1]/div/div[4]/div[2]/div[10]/div[2]/div[2]/input').click()

            # secondary
            if diabetes == 0:
                self.driver.find_element_by_xpath(
                    '/html/body/form/div[3]/div[4]/div[1]/div/div[4]/div[3]/div[1]/div[2]/div[1]/input').click()
            else:
                self.driver.find_element_by_xpath(
                    '/html/body/form/div[3]/div[4]/div[1]/div/div[4]/div[3]/div[1]/div[2]/div[2]/input').click()

            # alcohol
            if alcohol == 0:
                self.driver.find_element_by_xpath(
                    '/html/body/form/div[3]/div[4]/div[1]/div/div[4]/div[3]/div[2]/div[2]/div[1]/input').click()
            else:
                self.driver.find_element_by_xpath(
                    '/html/body/form/div[3]/div[4]/div[1]/div/div[4]/div[3]/div[2]/div[2]/div[2]/input').click()

            self.driver.find_element_by_xpath(
                "/html/body/form/div[3]/div[4]/div[1]/div/div[4]/div[3]/div[3]/div[2]/div[1]/select").click()
            self.driver.find_element_by_xpath(
                "/html/body/form/div[3]/div[4]/div[1]/div/div[4]/div[3]/div[3]/div[2]/div[1]/select/option[5]").click()

            # Wait for alert box to appear and then accept it
            obj = self.driver.switch_to.alert
            time.sleep(1)
            obj.accept()

            # t_score
            self.driver.find_element_by_xpath(
                '/html/body/form/div[3]/div[4]/div[1]/div/div[4]/div[3]/div[3]/div[2]/div[1]/input').send_keys(
                str(t_score))

            # Wait 3 seconds until submit button is clickable
            time.sleep(3)
            self.driver.find_element_by_xpath(
                '/html/body/form/div[3]/div[4]/div[1]/div/div[4]/div[3]/div[4]/div[1]/input').click()

            frax_textbox = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH,
                                                "/html/body/form/div[3]/div[4]/div[1]/div/div[4]/div[3]/div[4]/div["
                                                "2]/div[1]/div/div[2]/div[1]/div[2]/span"))
            )

            frax_percent_str = frax_textbox.text
            return float(frax_percent_str)

        except Exception as e:
            logging.error(e)
            logging.error("Error in get_frax_percent for patient %s" % patient_id)
            return None

    def close_driver(self):
        self.driver.close()
