from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import csv

#Creating the web scraper
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
browser = webdriver.Chrome(options=chrome_options)
browser.get("https://schedule.cpp.edu/")

#Changing the Search Requirements to access all the teachers
time.sleep(20)
sunday_checkbox = WebDriverWait(browser, 20).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/main/div/section/form/fieldset/table/tbody/tr[10]/td/table/tbody/tr/td[7]/input"))
)
time.sleep(15)
sunday_checkbox.click()

print("Sunday checkmark click successful")

search = WebDriverWait(browser, 15).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/main/div/section/form/fieldset/table/tbody/tr[13]/td[2]/span[1]/input"))
)
search.click()
print("Search successful")
time.sleep(25)

#Querying through the data
list_of_teachers = {}
for i in range(1,5184):
    teacher = browser.find_element(By.XPATH, "/html/body/main/div/section/form/div[3]/ol/li[" + str(i) + "]/table/tbody/tr[5]/td[1]").text

    parts = teacher.split(", ")  
    print(i, teacher)
    try:
        reordered_name = parts[1] + " " + parts[0]

        course = browser.find_element(By.XPATH, "/html/body/main/div/section/form/div[3]/ol/li[" + str(i) + "]/span/strong").text
        department = course.split()[0]

        if reordered_name not in list_of_teachers:
            list_of_teachers[reordered_name] = department
        
        csv_file = "AllTeachers.csv"

        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Name', 'Department'])  # Write header row
            for key, value in list_of_teachers.items():
                writer.writerow([key, value])
    except:
        print("Could not insert:" + teacher)