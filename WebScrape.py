from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import random
from IPython import get_ipython
get_ipython().magic('clear')
import time


Huberman_Path = '/Users/lucinogarcia/Downloads/Huberman_Element.txt'
Transcript_Site = 'https://www.hubermantranscripts.com'
with open(Huberman_Path, 'r') as file:
    Huberman_Element = file.read()
Pod_URLs = sorted(list(set(re.findall(r'href="(.*?)"', Huberman_Element))), reverse=True)


firefox_browser = webdriver.Firefox()


for episode_num in range(len(Pod_URLs)):

    firefox_browser.get(Transcript_Site+Pod_URLs[episode_num])
    
    input_element = firefox_browser.find_element(By.XPATH, '//input[@aria-label="Summary hierarchy"]')
    firefox_browser.execute_script("arguments[0].setAttribute('value', '0')", input_element)
    firefox_browser.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }))", input_element)
    time.sleep(round(random.uniform(1, 3), 1))
    button_element = firefox_browser.find_element(By.XPATH, '//button[text()="Expand All"]').click()
    text_content = firefox_browser.find_element(By.XPATH, "//*").text
    
    text_elements = text_content.split('\n')
    EpisodeTitle = text_elements[1]
    while text_elements[0][:3] != '1. ':
        del text_elements[0]
    while text_elements[-1][:10] != 'Be the fir':
        del text_elements[-1]
    del text_elements[-1]
    
    file_name = str(len(Pod_URLs) - episode_num).zfill(3) + " - " + EpisodeTitle + ".txt"
    with open(file_name, "w") as file:
        for element in text_elements:
            file.write(element + "\n")
    time.sleep(round(random.uniform(1, 5), 1))