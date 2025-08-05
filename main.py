import os
import json
from dotenv import load_dotenv
from seleniumwire import webdriver
from seleniumwire.utils import decode
from selenium.webdriver.common.by import By

load_dotenv()
AMUL_WEBSITE_URL = os.getenv('AMUL_WEBSITE_URL')
PINCODE = os.getenv('PINCODE')
def writeToFile(driver):
    with open("requests_log.txt", "w") as file:
        for request in driver.requests:
            if request.response and "substore=" in request.url:
                body = decode(request.response.body,request.response.headers.get('Content-Encoding', 'identity'))
                decoded_body = body.decode('utf-8')
                json_data = json.loads(decoded_body)
                items = json_data['data']
                
                for item in items:
                    file.write(f"{item['name']} {item['_id']} {item['available']}\n")

                
                file.write(
                    f"{request.url}\n"
                )
                break


options = webdriver.ChromeOptions()
# options.add_argument("--no-sandbox")
# options.add_argument("--headless")


driver = webdriver.Chrome(options=options)
# driver.implicitly_wait(5)

driver.get(AMUL_WEBSITE_URL)

pincode_input_element = driver.find_element(By.ID,'search')
pincode_input_element.send_keys(PINCODE)

pincode_found_element = driver.find_element(By.CLASS_NAME,'searchitem-name')
pincode_found_element.click()

driver.wait_for_request(r"substore=",5)
# writeToFile(driver)

driver.quit()
