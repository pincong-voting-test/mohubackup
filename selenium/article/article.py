import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait

import pyautogui
startpage=6135
endpage=6150
options = webdriver.ChromeOptions()

options.add_experimental_option('excludeSwitches', ['enable-logging'])

for page in range(startpage,endpage):
    URL = r'https://webcache.googleusercontent.com/search?q=cache:https://mohu.rocks/article/' + str(page)

    # 用selenium打开网页
    # (首先要下载 Chrome webdriver, 或 firefox webdriver)
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    
    # 等待结果加载
    WebDriverWait(driver, 60)
    # 打开"另存为"来保存html和资源文件
    pyautogui.hotkey('ctrl', 's')
    time.sleep(3)
    pyautogui.typewrite(str(page) + '.html')
    
    pyautogui.hotkey('enter')
    
    time.sleep(3)
    driver.quit()
