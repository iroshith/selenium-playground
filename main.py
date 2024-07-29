import xvfbwrapper
from selenium import webdriver
from selenium.webdriver.firefox import options, service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from os import environ
from time import sleep

username = ""
password = ""

options = options.Options()
options.binary_location = environ["FIREFOX"]
driver = webdriver.Firefox(
    options=options, service=service.Service(log_path="../gecko.log")
)

# head to github login page
driver.get("https://cloud.samsara.com/signin")
# find username/email field and send the username itself to the input field
driver.find_element(By.NAME, "email").send_keys(username)
driver.find_element(By.XPATH, "//button[contains(@type,'submit')]").click()
# find password input field and insert password as well
driver.find_element(By.CSS_SELECTOR, 'input[type="password"]').send_keys(password)
# click login button
driver.find_element(By.XPATH, "//button[contains(@type,'submit')]").click()

# wait the ready state to be complete
WebDriverWait(driver=driver, timeout=10).until(
    lambda x: x.execute_script("return document.readyState === 'complete'")
)
error_message = "Incorrect username or password."
# get the errors (if there are)
errors = driver.find_elements("css selector", ".flash-error")
# print the errors optionally
# for e in errors:
#     print(e.text)
# if we find that error message within errors, then login is failed
if any(error_message in e.text for e in errors):
    print("[!] Login failed")
else:
    print("[+] Login successful")

# an example scenario, show me my public repositories
repos = driver.find_element("css selector", ".js-repos-container")
# wait for the repos container to be loaded
WebDriverWait(driver=driver, timeout=10).until((lambda x: repos.text != "Loading..."))
# iterate over the repos and print their names
for repo in repos.find_elements(
    "css selector", "li.public"
):  # you can use "li.private" for private repos
    print(repo.find_element("css selector", "a").get_attribute("href"))

# close the driver
driver.close()
