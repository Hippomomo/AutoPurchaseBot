import os
from dotenv import load_dotenv  # 引入 dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pytesseract
from PIL import Image
import time


# 加載 .env 文件中的環境變量
load_dotenv()

# 從 .env 文件中獲取帳號和密碼
username = os.getenv('MY_USERNAME')
password = os.getenv('MY_PASSWORD')
print(f"讀取到的帳號: {username}")
print(f"讀取到的密碼: {password}")

# 設置 Tesseract 路徑
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

# 設置 Chrome 的選項
chrome_options = Options()

# 初始化 Chrome WebDriver 使用 Service
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# 導航到網站
driver.get("https://shwoo.gov.taipei/shwoo/login/login00/index")

try:
    # 等待帳號輸入框出現
    account_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ACCOUNT"))
    )
    
    # 輸入帳號與密碼，使用從 .env 文件中讀取的變量
    account_field.send_keys(username)
    driver.find_element(By.ID, "PASSWORD").send_keys(password)
    
    # 抓取驗證碼圖片
    captcha_element = driver.find_element(By.ID, "validImgLogin")
    captcha_image_path = "captcha.png"
    captcha_element.screenshot(captcha_image_path)

    # 使用 OCR 解析驗證碼
    captcha_text = pytesseract.image_to_string(Image.open(captcha_image_path)).strip()
    print(f"識別的驗證碼為: {captcha_text}")

    # 使用 XPath 部分匹配來定位驗證碼輸入框
    captcha_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[contains(@id, 'CAPTCHA_CODE_LOGIN')]"))
    )
    captcha_input.send_keys(captcha_text)  # 輸入識別到的驗證碼

    # 使用 XPath 定位並點擊登入按鈕
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@value='登入']"))
    )
    login_button.click()

    # 等待頁面加載完成，假設登入成功後會跳轉到帶有 "loginSuccess" 的 URL
    WebDriverWait(driver, 10).until(
        EC.url_contains("loginSuccess")
    )
    print("登入成功！")

except Exception as e:
    print(f"發生錯誤: {e}")

finally:
    time.sleep(5)
    driver.quit()
