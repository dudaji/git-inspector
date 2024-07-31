import sys
import os
import time
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
from selenium.webdriver.common.action_chains import ActionChains

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
        # chrome_options.add_argument("--headless")
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
            # element = div, spans
            machine_type_value = self.get_element_attribute(element, "data-value")
            print(f"Found machine type value : machine name: {machine_type_value}, region : {region}, machine-series: {series_value}")
            try:
                cookie_consent_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[text()="나중에"]'))
                )
                cookie_consent_button.click()
            except Exception as e:
                print("쿠키 동의 창을 찾을 수 없습니다:", e)
            # 드롭다운 버튼을 클릭하기 위해 Actions 사용
            dropdown_button_xpath = '//div[@aria-controls="i27" and @aria-haspopup="listbox"]'
            dropdown_area = driver.find_element(By.XPATH, dropdown_button_xpath)
            dropdown_area.click()
            time.sleep(2)  # 2초 대기
            # li element 클릭
            
            
            # 머신 타입 정보가 포함된 요소를 기다림
            detail_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'coMZGe')]"))
            )
            # vCPUs와 RAM 정보 추출
            spec_text = detail_element.find_element(By.XPATH, ".//div[contains(text(), 'vCPUs')]").text

            # vCPUs와 RAM 값 파싱
            vcpus = spec_text.split(',')[0].split(':')[1].strip()
            ram = spec_text.split(',')[1].split(':')[1].replace("GB", "").strip()

            if vcpus.replace('.', '', 1).isdigit() and ram.replace('.', '', 1).isdigit():
                print(f"Machine type: {machine_type_value}")
                print(f"vCPUs: {vcpus}, RAM: {ram}")
                print(f"Region: {region}, Series: {series_value}")
            
    
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