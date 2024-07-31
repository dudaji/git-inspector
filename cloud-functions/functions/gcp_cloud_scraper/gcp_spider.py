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
from selenium.common.exceptions import (
    StaleElementReferenceException,
    NoSuchElementException,
)
from selenium.webdriver.common.action_chains import ActionChains

# from google.cloud import firestore
from datetime import datetime

# from pydantic import BaseModel, Field
from typing import List, Optional
from functions.clouds.cloud_cost import CloudCost
from functions.clouds._firestore import save_to_firestore
import logging


class GCPSpider(scrapy.Spider):
    name = "gcp_spider"

    def start_requests(self):
        region_urls = {
            "asia-northeast3": "https://cloud.google.com/products/calculator?hl=ko&region=asia-northeast3&dl=CiQ1ZGQyZTU1OS1lNzlmLTRkODAtODE3NS04YTBlOTkyMmMyNzAQCBokOEE5NDZFQ0QtMDYzMC00MDUzLThGRDMtOTIyNTY0QTNDNTE2",
            "us-central1": "https://cloud.google.com/products/calculator?hl=ko&region=us-central1&dl=CiQ1ZGQyZTU1OS1lNzlmLTRkODAtODE3NS04YTBlOTkyMmMyNzAQCBokOEE5NDZFQ0QtMDYzMC00MDUzLThGRDMtOTIyNTY0QTNDNTE2",
        }

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        for region, url in region_urls.items():
            region_driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options,
            )
            print(f"start {region} driver")
            region_driver.get(url)
            WebDriverWait(region_driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//ul[@aria-label="Series"]//li[@role="option"]')
                )
            )
            self.parse_machine_type(region_driver, region)
            print(f"quit {region} driver")
            region_driver.quit()

    def parse_machine_type(self, driver, region):
        try:
            cookie_consent_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, '//button[text()="나중에"]'))
            )
            cookie_consent_button.click()
        except Exception as e:
            print("쿠키 동의 창을 찾을 수 없습니다:", e)

        series_elements = driver.find_elements(
            By.XPATH, '//ul[@aria-label="Series"]//li[@role="option"]'
        )
        for series in series_elements:
            series_value = self.get_element_attribute(series, "data-value")
            try:
                series_type_dropdown = (
                    '//div[@aria-controls="i23" and @aria-haspopup="listbox"]'
                )
                series_type_dropdown_area = driver.find_element(
                    By.XPATH, series_type_dropdown
                )
                series_type_dropdown_area.click()
                time.sleep(1)
                actions = ActionChains(driver)
                actions.move_to_element(series).click().perform()
                print(
                    f"current machine series : {series_value} , region : {region} "
                )
                time.sleep(1)
                self.parse_machine_name_spec(driver, region, series_value)

                actions.move_to_element(
                    series_type_dropdown_area
                ).click.perform()

                WebDriverWait(driver, 3).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//ul[@aria-label="Series"]')
                    )
                )
                time.sleep(1)  # 1초 대기
            except:
                continue

    # have to click machine type and parse all data (final)
    def parse_machine_name_spec(self, driver, region, series_value):
        try:
            cookie_consent_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, '//button[text()="나중에"]'))
            )
            cookie_consent_button.click()
        except Exception as e:
            print("쿠키 동의 창을 찾을 수 없습니다:", e)
        machine_type_dropdown = (
            '//div[@aria-controls="i27" and @aria-haspopup="listbox"]'
        )
        machine_type_dropdown_area = driver.find_element(
            By.XPATH, machine_type_dropdown
        )
        machine_type_dropdown_area.click()
        time.sleep(2)  # 2초 대기
        machine_elements = driver.find_elements(
            By.XPATH, '//ul[@aria-label="Machine type"]/li[@data-value]'
        )
        # 드롭다운 버튼을 클릭하기 위해 Actions 사용
        for machine in machine_elements:
            try:
                # element = div, spans
                machine_type_value = self.get_element_attribute(
                    machine, "data-value"
                )
                # 해당 요소를 클릭하여 선택
                if machine_type_value == "custom":
                    print(f"skip machine type custom")
                    continue
                actions = ActionChains(driver)
                actions.move_to_element(machine).click().perform()
                # print("clicked machine element li")

                # 선택한 machine_type이 detail_element에 반영될 때까지 대기
                detail_element_xpath = f"//div[contains(@class, 'VVW32d')]//div[contains(text(), '{machine_type_value}')]"
                detail_element = WebDriverWait(driver, 3).until(
                    EC.text_to_be_present_in_element(
                        (By.XPATH, detail_element_xpath), machine_type_value
                    )
                )
                # vCPUs와 RAM 정보가 포함된 요소 기다림
                vcpu_ram_xpath = "//div[contains(@class, 'VVW32d')]//div[contains(text(), 'vCPUs')]"
                vcpu_ram_element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, vcpu_ram_xpath))
                )
                # vCPUs와 RAM 정보 추출
                spec_text = vcpu_ram_element.text
                # print(f"spec_text : {spec_text}")

                # vCPUs와 RAM 값 파싱
                vcpus = spec_text.split(",")[0].split(":")[1].strip()
                ram = (
                    spec_text.split(",")[1]
                    .split(":")[1]
                    .replace("GB", "")
                    .strip()
                )

                if (
                    vcpus.replace(".", "", 1).isdigit()
                    and ram.replace(".", "", 1).isdigit()
                ):
                    price_xpath = "//div[contains(@class, 'egBpsb')]/span[contains(@class, 'D0aEmf')]"
                    price_element = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, price_xpath))
                    )
                # 월별 가격 정보 추출
                price_text = price_element.text
                # 월별 가격을 시간별 가격으로 환산
                # 쉼표를 제거하고 월별 가격을 시간별 가격으로 환산
                monthly_price = float(
                    price_text.replace("$", "").replace(",", "")
                )
                hourly_price = monthly_price / (
                    30 * 24
                )  # 한 달을 30일로 가정하고 시간당 가격을 계산
                # CloudCost 모델 생성
                cloud_cost = CloudCost(
                    vendor="GCP",
                    name=machine_type_value,
                    region=region,
                    cpu=vcpus,
                    ram=ram,
                    cost_per_hour=hourly_price,
                    extraction_date=datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                )
                print(cloud_cost)
                # 드롭다운을 다시 클릭하여 열기
                actions.move_to_element(
                    machine_type_dropdown_area
                ).click().perform()

                # 드롭다운 메뉴 항목 기다리기
                WebDriverWait(driver, 3).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//ul[@aria-label="Machine type"]')
                    )
                )
                time.sleep(1)  # 2초 대기
            except:
                continue

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
    logging.getLogger("scrapy").setLevel(logging.ERROR)

    process = CrawlerProcess(
        settings={
            "LOG_LEVEL": "ERROR",  # 전체 Scrapy 로그 레벨 설정
        }
    )

    process.crawl(GCPSpider)
    process.start()
