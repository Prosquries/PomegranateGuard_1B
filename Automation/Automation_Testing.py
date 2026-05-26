import time

from openpyxl.chart.title import Title
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
import string

#--------------- Drivers ------------------

driver = webdriver.Chrome()
driver.get("http://127.0.0.1:5000")
driver.maximize_window()

wait = WebDriverWait(driver,10)

#--------------- Functions ------------------

def random_username(length=8):
    return ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=length
        )
    )


def workflow():

    username = random_username()
    Email = f"{username}@gmail.com"

    # ---------------- Signup ----------------

    wait.until(EC.element_to_be_clickable((By.XPATH,"//a[@class='auth-link']"))).click()

    wait.until(EC.presence_of_element_located((By.ID,"username"))).send_keys(username)
    print(f"Username is : {username}")

    wait.until(EC.presence_of_element_located((By.ID,"email"))).send_keys(Email)
    print(f"Email is : {Email}")

    wait.until(EC.presence_of_element_located((By.ID,"password"))).send_keys("Test@123")
    print("Password is : Test@123")

    wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Sign Up']"))).click()
    print("Clicking on Signup Button")

    # ---------------- Login ----------------

    email_box = wait.until(EC.visibility_of_element_located((By.ID,"email")))

    password_box = wait.until(EC.visibility_of_element_located((By.ID,"password")))

    email_box.send_keys(Email)
    password_box.send_keys("Test@123")

    wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Log In']"))).click()
    print("Login is performed")

    # ---------------- Symptom Checker -----------------

    wait.until(EC.element_to_be_clickable((By.XPATH,"//a[normalize-space()='Symptom Checker']"))).click()

    Message = input("Enter the Symptoms")
    wait.until(EC.presence_of_element_located((By.XPATH,"//textarea[@placeholder='e.g., I see black sunken spots on the fruit, and it seems to be rotting fast...']"))).send_keys(Message)
    print(f"Message is {Message}")

    wait.until(EC.element_to_be_clickable((By.XPATH,"//button[normalize-space()='Analyze Symptoms']"))).click()

    # --------------- Pomegranate Disease Library -------------

    wait.until(EC.element_to_be_clickable((By.XPATH,"//a[normalize-space()='Disease Library']"))).click()
    print("Disease Library is clicked")

    Text = "Disease Library - PomegranateGuard"

    assert driver.title == Text

    #----------------- Scanner --------------------------------

    wait.until(EC.element_to_be_clickable((By.XPATH,"//a[normalize-space()='Scanner']"))).click()
    print("Scanner is clicked")

    path = wait.until(EC.presence_of_element_located((By.XPATH,"//input[@id='fileInput']")))
    path.send_keys(r"D:\Aarav\Pomogrante\PomegranateGuard_1B\Selected photo.jfif")

    wait.until(EC.element_to_be_clickable((By.XPATH,"//span[@id='btnText']"))).click()

    print("Image is uploaded")

    # --------------- Logout ---------------------------

    wait.until(EC.element_to_be_clickable((By.XPATH,"//a[normalize-space()='Logout']"))).click()
    print("Logged out successfully")

#--------------- Execute -------------------------------

workflow()

time.sleep(5)
driver.quit()