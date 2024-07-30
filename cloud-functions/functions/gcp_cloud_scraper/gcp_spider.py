import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
import scrapy
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

# from google.cloud import firestore
from datetime import datetime

# from pydantic import BaseModel, Field
from typing import List, Optional
from functions.clouds.model import CloudCost

import logging

# from functions.clouds._firestore import save_to_firestore

class GCPSpider(scrapy.Spider):
    name = "gcp_spider"
    
    def start_requests(self):
        region_urls = {
            "asia-northeast3": "https://cloud.google.com/products/calculator?hl=ko&region=asia-northeast3&dl=CiQ1ZGQyZTU1OS1lNzlmLTRkODAtODE3NS04YTBlOTkyMmMyNzAQCBokOEE5NDZFQ0QtMDYzMC00MDUzLThGRDMtOTIyNTY0QTNDNTE2",
            "us-central1": "https://cloud.google.com/products/calculator?hl=ko&region=us-central1&dl=CiQ1ZGQyZTU1OS1lNzlmLTRkODAtODE3NS04YTBlOTkyMmMyNzAQCBokOEE5NDZFQ0QtMDYzMC00MDUzLThGRDMtOTIyNTY0QTNDNTE2",
        }

        # 하나의 WebDriver 인스턴스 생성
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")


        for region, url in region_urls.items():
            region_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            region_driver.get(url)
            WebDriverWait(region_driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//ul[@aria-label="Series"]//li[@role="option"]'))
            )
            self.parse_machine_type(region_driver, region)
            region_driver.quit()

    def parse_machine_type(self, driver, region):
        series_elements = driver.find_elements(By.XPATH, '//ul[@aria-label="Series"]//li[@role="option"]')
        for element in series_elements:
            series_value = self.get_element_attribute(element, "data-value")
            if series_value:
                # print(f"Found series with value: {series_value}")
                self.parse_machine_name_spec(driver, region, series_value)

    def parse_machine_name_spec(self, driver, region, series_value):
        machine_elements = driver.find_elements(By.XPATH, '//ul[@aria-label="Machine type"]/li[@data-value]')
        for element in machine_elements:
            machine_type_value = self.get_element_attribute(element, "data-value")
            print(f"Found machine type value : {machine_type_value}, {region}, {series_value}")
            # 머신 타입 선택
            # "custom" 타입은 스킵
            if machine_type_value == "custom":
                print(f"Skipping custom type: {machine_type_value}")
                continue
            # 선택에서 막힘


    
    def get_element_attribute(self, element, attribute):
        try:
            return element.get_attribute(attribute)
        except StaleElementReferenceException:
            return None

    def get_element_text(self, element, xpath):
        try:
            return element.find_element(By.XPATH, xpath).text
        except StaleElementReferenceException:
            return ""

if __name__ == "__main__":
    # Scrapy logging 설정을 최소화
    logging.getLogger('scrapy').setLevel(logging.ERROR)

    process = CrawlerProcess(settings={
        'LOG_LEVEL': 'ERROR',  # 전체 Scrapy 로그 레벨 설정
    })

    process.crawl(GCPSpider)
    process.start()