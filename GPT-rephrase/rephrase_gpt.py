import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from fake_useragent import UserAgent
from selenium.webdriver.support import expected_conditions as EC
import json, os

with open("../fineweb_data/data/shard_0.json") as f:
    data = [json.loads(line) for line in f]


metrics = {}
for generated_text in data[0]["generation_complete"]:
   while True:
      try:
         op = webdriver.ChromeOptions()
         op.add_argument(f"user-agent={UserAgent.random}")
         op.add_argument("user-data-dir=./")
         op.add_experimental_option("detach", True)
         op.add_experimental_option("excludeSwitches", ["enable-logging"])

         driver = uc.Chrome(chrome_options=op)
         PATH = "chromedriver-linux64/chromedriver"
         driver.get('https://chat.openai.com/')

         inputElements = driver.find_elements(By.TAG_NAME, "textarea")

         prompt = "Perform sentence restructuring while keeping the paragraph length similar and make sure the rephrased text seems like written by AI. Don't include description of what you did"
         # Write the prompt to the text area
         inputElements[0].send_keys(prompt)
         sleep(5)
         inputElements[0].send_keys(Keys.RETURN)
         sleep(3)
         inputElements = driver.find_elements(By.TAG_NAME, "p")
         sleep(2)
         results = []
         for element in inputElements:
            results.append(element.text)
         print(generated_text)
         print(results)
         metrics[generated_text] = results[-2]
         driver.quit()
         break
      except:
         driver.quit()
         continue

with open("../rephrased_text/shard_0.json", "w") as f:
    json.dump(metrics, f)
