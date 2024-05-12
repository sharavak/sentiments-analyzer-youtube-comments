import time
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def extract_comment(contents):
    comments=[]
    for i in contents:
        try:
            comments.append(i.find_element(By.CSS_SELECTOR,'#content-text').text)
        except:pass
    return comments

def scrape(url):
    options=Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
    driver.get(url)
    print("Started")
    track_height=driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        htmlelement = driver.find_element(By.TAG_NAME,"body")  
        htmlelement.send_keys(Keys.END) 
        time.sleep(2)
        newHeight=driver.execute_script("return document.documentElement.scrollHeight")
        if newHeight==track_height:
            break
        track_height=newHeight
    contents=driver.find_elements(By.XPATH,'//*[@id="contents"]/ytd-comment-thread-renderer')
    comments=extract_comment(contents)
    print(len(comments))
    return comments
