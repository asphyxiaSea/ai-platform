from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os, time

URL = "https://www.ymt.com/hangqing/juhe-7240?text=%E8%8F%9C%E7%B1%BD%E6%B2%B9"

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/123.0.0.0 Safari/537.36")

for binary in ["/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome"]:
    if os.path.exists(binary):
        options.binary_location = binary
        break

for driver_path in ["/usr/bin/chromedriver", "/usr/local/bin/chromedriver"]:
    if os.path.exists(driver_path):
        service = Service(driver_path)
        break
else:
    raise FileNotFoundError("找不到 chromedriver")

driver = ChromeWebDriver(service=service, options=options)

try:
    driver.get(URL)
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".price"))
        )
    except:
        pass
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    price_el = soup.select_one(".price span")
    compare_els = soup.select(".price ~ div span")

    if price_el:
        price = price_el.get_text(strip=True)
        # 涨跌数值和方向
        texts = [el.get_text(strip=True) for el in compare_els if el.get_text(strip=True)]
        change = " ".join(texts)
        print(f"今日均价: {price}")
    else:
        print("未找到价格数据")

finally:
    driver.quit()