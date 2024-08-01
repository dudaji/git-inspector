import sys
import os
import time
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
import scrapy
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    NoSuchElementException,
    TimeoutException
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# from google.cloud import firestore
from datetime import datetime

# from pydantic import BaseModel, Field
from typing import List, Optional
from functions.clouds.cloud_cost import CloudCost
from functions.clouds._firestore import save_to_firestore_each
import logging


class GCPSpider(scrapy.Spider):
    name = "gcp_spider"
    data_file = "gcp_cloud_costs.csv"

    def press_escape_key(self, driver):
        actions = ActionChains(driver)
        actions.send_keys(Keys.ESCAPE).perform()
        print(f"pressed ESC key to close dropdown menu")
        time.sleep(0.5)

    def set_zoom_level(self, driver, zoom_percent):
        driver.execute_script(f"document.body.style.zoom='{zoom_percent}%'")
        time.sleep(1)

    def remove_all_asides(self, driver):
        driver.execute_script(
            "const asides = document.querySelectorAll('aside'); asides.forEach(aside => aside.remove());"
        )
        print(f"remove all asides runned")
        time.sleep(1)  # Give time for the script to execute

    def close_popup(self, driver):
        try:
            close_button = driver.find_element(
                By.XPATH,
                '//span[@class="VfPpkd-kBDsod" and @aria-hidden="true"]/svg/path',
            )
            close_button.click()
            print(f"close popup runned")
        except Exception as e:
            pass  # Ignore if the element is not found

    def is_element_visible(self, element, driver):
        return driver.execute_script(
            "var elem = arguments[0],                 "
            "  box = elem.getBoundingClientRect(),    "
            "  cx = box.left + box.width / 2,         "
            "  cy = box.top + box.height / 2,         "
            "  e = document.elementFromPoint(cx, cy); "
            "for (; e; e = e.parentElement) {         "
            "  if (e === elem)                        "
            "    return true;                         "
            "}                                        "
            "return false;                            ",
            element
        )

    def scroll_to_element_if_not_visible(self, driver, element, timeout=3):
        if not self.is_element_visible(element, driver):
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            try:
                WebDriverWait(driver, timeout).until(
                    lambda d: self.is_element_visible(element, d)
                )
            except TimeoutException:
                print("Element is still not visible after scrolling")
                self.press_escape_key(driver)  # Press ESC key to close any open dropdowns
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)  # Retry scrolling
                try:
                    WebDriverWait(driver, timeout).until(
                        lambda d: self.is_element_visible(element, d)
                    )
                except TimeoutException:
                    print("Element is still not visible after second scrolling attempt")
                    self.press_escape_key(driver)  # Press ESC key to close any open dropdowns


    def start_requests(self):
        compute_engine_url = "https://cloud.google.com/products/calculator?hl=ko&region=asia-northeast3&dl=CiQ2MzljY2Q1Mi1hYWNlLTQ1MWQtYjhjMS00MWM4MTgzZWIwZWQQCBokOEE5NDZFQ0QtMDYzMC00MDUzLThGRDMtOTIyNTY0QTNDNTE2"
        firefox_options = Options()
        firefox_options.binary_location = "/Applications/Firefox.app/Contents/MacOS/firefox"
        firefox_options.add_argument("--headless")  # Enable headless mode
        firefox_options.add_argument("--disable-gpu")
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        firefox_options.add_argument("--disable-notifications")
        geckodriver_path = os.path.join(os.path.dirname(__file__), "geckodriver")

        driver = webdriver.Firefox(service=Service(geckodriver_path), options=firefox_options)
        driver.get(compute_engine_url)
        screen_width = 3840
        screen_height = 2160
        driver.set_window_position(0, 0)
        driver.set_window_size(screen_width // 2, screen_height)
        self.set_zoom_level(driver, 40)
        self.parse_region(driver)

    def parse_region(self, driver):
        try:
            self.close_popup(driver)
            # self.remove_all_asides(driver)
            cookie_consent_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, '//button[text()="나중에"]'))
            )
            cookie_consent_button.click()
        except Exception as e:
            print("쿠키 동의 창을 찾을 수 없습니다:", e)
        region_xpath = '//ul[@aria-label="Region"]//li[@data-value]'
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.XPATH, region_xpath)
            )
        )
        region_elements = driver.find_elements(
            By.XPATH, '//ul[@aria-label="Region"]/li[@data-value]'
        )
        print(f"length of region elements: {len(region_elements)}")

        for index, region in enumerate(region_elements):
            try: 
                self.scroll_to_element_if_not_visible(driver, region)
                region_value = self.get_element_attribute(region, "data-value")
                print(f"current region_value : {region_value}")
                region_type_dropdown = (
                    '//div[@aria-controls="i39" and @aria-haspopup="listbox"]'
                )
                region_type_dropdown_area = driver.find_element(
                    By.XPATH, region_type_dropdown
                )
                self.scroll_to_element_if_not_visible(driver, region_type_dropdown_area)
                region_type_dropdown_area.click()

                time.sleep(1)
                self.scroll_to_element_if_not_visible(driver, region)
                actions = ActionChains(driver)
                actions.move_to_element(region).click().perform()
                time.sleep(1)
                # parse machine series
                self.parse_series(driver, region_value)

                if index < len(region_elements) - 1:
                    self.scroll_to_element_if_not_visible(driver, region_type_dropdown_area)
                    actions.move_to_element(
                        region_type_dropdown_area
                    ).click().perform()
                    time.sleep(1)
                    WebDriverWait(driver, 3).until(
                        EC.visibility_of_element_located(
                            (By.XPATH, '//ul[@aria-label="Region"]')
                        )
                    )
                    time.sleep(1)  # 1초 대기
            except Exception as e:
                print(f"error occurred in region crawling: {e}, but continue")
                self.press_escape_key(driver)
                continue

    def parse_series(self, driver, region):
        try:
            self.close_popup(driver)
            # self.remove_all_asides(driver)
            cookie_consent_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, '//button[text()="나중에"]'))
            )
            cookie_consent_button.click()
        except Exception as e:
            print("쿠키 동의 창을 찾을 수 없습니다:", e)

        series_elements = driver.find_elements(
            By.XPATH, '//ul[@aria-label="Series"]/li[@data-value]'
        )
        print(f"length of sereis element : {len(series_elements)}")
        for index, series in enumerate(series_elements):
            series_value = self.get_element_attribute(series, "data-value")
            if self.is_machine_processed(region, series_value):
                print(f"Skip already processed machine series: {series_value}")
                if series_type_dropdown_area.get_attribute("aria-expanded") == "true":
                    # Find a safe location to click, here we assume the header exists and is clickable
                    self.press_escape_key(driver)
                continue
            try:
                print(
                    f"current machine series : {series_value} , region : {region} "
                )
                series_type_dropdown = (
                    '//div[@aria-controls="i23" and @aria-haspopup="listbox"]'
                )
                series_type_dropdown_area = driver.find_element(
                    By.XPATH, series_type_dropdown
                )
                self.scroll_to_element_if_not_visible(driver, series_type_dropdown_area)
                series_type_dropdown_area.click()

                time.sleep(0.5)

                self.scroll_to_element_if_not_visible(driver, series)
                actions = ActionChains(driver)
                actions.move_to_element(series).click().perform()
                time.sleep(0.5)
                self.parse_machine(driver, region, series_value)
                
                # 마지막 요소가 아니라면 dropdown area를 다시 클릭
                if index < len(series_elements) - 1:
                    self.scroll_to_element_if_not_visible(driver, series_type_dropdown_area)
                    actions.move_to_element(
                        series_type_dropdown_area
                    ).click().perform()
                    time.sleep(0.5)

                    WebDriverWait(driver, 3).until(
                        EC.visibility_of_element_located(
                            (By.XPATH, '//ul[@aria-label="Series"]')
                        )
                    )
                    time.sleep(1)  # 1초 대기
            except Exception as e:
                print(f"error occurred in series crawling: {e}, but continue")
                continue

    # have to click machine type and parse all data (final)
    def parse_machine(self, driver, region, series_value):
        try:
            # self.remove_all_asides(driver)
            cookie_consent_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, '//button[text()="나중에"]'))
            )
            cookie_consent_button.click()
        except Exception as e:
            print("쿠키 동의 창을 찾을 수 없습니다:", e)
  
        # machine_type_dropdown = f'//div[@aria-controls" and @aria-haspopup="listbox"]'
        machine_type_dropdown = (
            '//div[@aria-controls="i27" and @aria-haspopup="listbox"]'
        )
        machine_type_dropdown_area = driver.find_element(
            By.XPATH, machine_type_dropdown
        )
        machine_type_dropdown_area.click()
        time.sleep(0.5)  # 2초 대기
        machine_elements = driver.find_elements(
            By.XPATH, '//ul[@aria-label="Machine type"]/li[@data-value]'
        )
        # 드롭다운 버튼을 클릭하기 위해 Actions 사용
        for index, machine in enumerate(machine_elements):
            try:
                # self.remove_all_asides(driver)
                # element = div, spans
                machine_type_value = self.get_element_attribute(
                    machine, "data-value"
                )
                print(f"current machine type element: {machine_type_value}")
                if machine_type_value == "custom":
                    print(f"skip machine type custom")
                    continue

                # 이미 처리된 데이터 확인
                if self.is_machine_processed(region, machine_type_value):
                    print(f"Skip already processed machine type: {machine_type_value}")
                    if machine_type_dropdown_area.get_attribute("aria-expanded") == "true":
                        self.press_escape_key(driver)
                    continue

                # 안보이면 스크롤해서 찾기
                self.scroll_to_element_if_not_visible(driver, machine)
                actions = ActionChains(driver)
                actions.move_to_element(machine).click().perform()

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
                # 한국의 경우 가격이 나오는 타입이 별로 없음. region 재설정해서 다시해야할듯.
                price_text = price_element.text
                if price_text == "--":
                    unsupported_type = CloudCost(
                        vendor="GCP",
                        name=machine_type_value,
                        region=region,
                        cpu=vcpus,
                        ram=ram,
                        cost_per_hour="unsupported",
                        extraction_date=datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                    )
                    print(f"Unsupported type: {unsupported_type}")
                    self.save_to_file(unsupported_type)
                    self.press_escape_key(driver)
                    continue
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
                self.save_to_file(cloud_cost)
                # 드롭다운 영역으로 다시 스크롤
                if index < len(machine_elements) - 1:
                    # 드롭다운 영역으로 다시 스크롤
                    self.scroll_to_element_if_not_visible(driver, machine_type_dropdown_area)
                    actions.move_to_element(
                        machine_type_dropdown_area
                    ).click().perform()

                    # 드롭다운 메뉴 항목 기다리기
                    WebDriverWait(driver, 3).until(
                        EC.visibility_of_element_located(
                            (By.XPATH, '//ul[@aria-label="Machine type"]')
                        )
                    )
                    time.sleep(1)  # 1초 대기
            except Exception as e:
                print(f"exception occured : {e}, but continue")
                self.press_escape_key(driver)
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
        
    def save_to_file(self, cloud_cost):
        file_exists = os.path.isfile(self.data_file)
        cloud_cost_df = pd.DataFrame([cloud_cost.to_dict()])
        if file_exists:
            existing_df = pd.read_csv(self.data_file)
            updated_df = pd.concat([existing_df, cloud_cost_df], ignore_index=True)
        else:
            updated_df = cloud_cost_df
        updated_df.to_csv(self.data_file, index=False)


    def is_machine_processed(self, region, machine_type_value):
        if not os.path.isfile(self.data_file):
            return False
        df = pd.read_csv(self.data_file)
        processed = df[
            (df['region'] == region) &
            (df['name'] == machine_type_value) &
            df['cpu'].notnull() &
            df['ram'].notnull()
        ]
        return not processed.empty and (processed['cost_per_hour'] != 'unsupported').all()


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
