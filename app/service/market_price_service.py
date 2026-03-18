from __future__ import annotations

import asyncio
import os
import re
import time

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver

from app.domain.errors import ExternalServiceError


def _extract_price_from_url(url: str) -> str:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/123.0.0.0 Safari/537.36"
    )

    for binary in [
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/usr/bin/google-chrome",
    ]:
        if os.path.exists(binary):
            options.binary_location = binary
            break

    service: Service | None = None
    for driver_path in ["/usr/bin/chromedriver", "/usr/local/bin/chromedriver"]:
        if os.path.exists(driver_path):
            service = Service(driver_path)
            break

    if service is None:
        raise ExternalServiceError(message="找不到 chromedriver")

    driver = ChromeWebDriver(service=service, options=options)
    try:
        driver.get(url)
        time.sleep(1)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        price_el = soup.select_one(".price span")
        if price_el is None:
            raise ExternalServiceError(message="未找到价格数据")

        raw_price = price_el.get_text(strip=True)
        # Remove currency symbols and other non-numeric wrappers while preserving decimals.
        price = re.sub(r"[^\d.]", "", raw_price)
        if not price:
            raise ExternalServiceError(message="价格数据为空")

        return price
    finally:
        driver.quit()


async def market_price_service(*, url: str) -> dict[str, str]:
    price = await asyncio.to_thread(_extract_price_from_url, url)
    return {"price": price}
