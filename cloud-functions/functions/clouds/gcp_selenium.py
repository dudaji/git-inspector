import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from model import CloudCost
from functions.clouds._firestore import save_to_firestore
from webdriver_manager.chrome import ChromeDriverManager
from typing import List
from datetime import datetime


"""
region 
1. us-central1, 


2. asia-northeast3
N1, N2, N4, E2, N2D, T2A, T2D, C3, C3D
f1-micro
cpu 1 ram 0.9
g1-small
cpu 1 ram 1.7
n1-standard-1
cpu 1 ram 3.75

...

"""


def setup_driver():
    options = Options()
    options.add_argument("--headless")  # 브라우저 창을 표시하지 않음
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def get_gcp_prices(region: str) -> List[CloudCost]:
    driver = setup_driver()

    # 각 지역에 맞는 URL 설정
    region_urls = {
        "asia-northeast3": "https://cloud.google.com/products/calculator/?utm_source=google&utm_medium=cpc&utm_campaign=japac-SG-all-en-dr-SKWS-all-all-trial-DSA-dr-1605216&utm_content=text-ad-none-none-DEV_c-CRE_655856180768-ADGP_Hybrid%20%7C%20SKWS%20-%20BRO%20%7C%20DSA%20-All%20Webpages-KWID_39700076131767978-dsa-1456167871416&userloc_9195692-network_g&utm_term=KW_&gad_source=1&gclid=Cj0KCQjw-5y1BhC-ARIsAAM_oKmOGMzycVnRnHr83GfQwifv_kxnKU1wVw8DYWgUEHo8LjCco41p1B0aAogBEALw_wcB&gclsrc=aw.ds&dl=CiRlYjUyYTI1OC0yYjRiLTRkODItYWU1Ny1hYzdhZmI0Nzk4ZmUQCBokMDBGMjg2M0ItQUYxMi00NUM1LUIzNzAtMEQ1MkExNDFFMEY4",
        "us-central1": "https://cloud.google.com/products/calculator/?utm_source=google&utm_medium=cpc&utm_campaign=japac-SG-all-en-dr-SKWS-all-all-trial-DSA-dr-1605216&utm_content=text-ad-none-none-DEV_c-CRE_655856180768-ADGP_Hybrid%20%7C%20SKWS%20-%20BRO%20%7C%20DSA%20-All%20Webpages-KWID_39700076131767978-dsa-1456167871416&userloc_9195692-network_g&utm_term=KW_&gad_source=1&gclid=Cj0KCQjw-5y1BhC-ARIsAAM_oKmOGMzycVnRnHr83GfQwifv_kxnKU1wVw8DYWgUEHo8LjCco41p1B0aAogBEALw_wcB&gclsrc=aw.ds&dl=CiQxMzU5NjQxZC02ZGViLTQ2ZWUtODAxZC1iMGFjODkzM2ZiOWYQCBokMDBGMjg2M0ItQUYxMi00NUM1LUIzNzAtMEQ1MkExNDFFMEY4",
    }

    if region not in region_urls:
        print(f"Region {region} is not supported.")
        return []

    url = region_urls[region]
    driver.get(url)
    time.sleep(5)

    # Step 2: Select machine type
    machine_type_button = driver.find_element(
        By.XPATH, '//*[@id="machine-type"]'
    )
    machine_type_button.click()
    time.sleep(1)

    n1_standard_1_option = driver.find_element(
        By.XPATH, '//*[@id="machine-type"]/option[text()="n1-standard-1"]'
    )
    n1_standard_1_option.click()
    time.sleep(1)

    # Step 3: Get vCPU, RAM
    vcpu = driver.find_element(By.XPATH, '//*[@id="vcpu"]').text
    ram = driver.find_element(By.XPATH, '//*[@id="ram"]').text

    # Step 4: Get cost
    cost_per_hour = driver.find_element(
        By.XPATH, '//*[@id="cost-per-hour"]'
    ).text

    # Step 5: Make CloudCost and send to Firestore
    extraction_date = datetime.utcnow().strftime("%Y-%m-%d")

    cloud_cost = CloudCost(
        vendor="GCP",
        name="n1-standard-1",
        region=region,
        cpu=float(vcpu),
        ram=float(ram.replace(" GB", "")),
        cost_per_hour=float(cost_per_hour.replace("$", "")),
        extraction_date=extraction_date,
    )

    save_to_firestore([cloud_cost])

    driver.quit()


if __name__ == "__main__":
    # 원하는 지역을 지정하여 함수 호출
    get_gcp_prices("asia-northeast3")
    get_gcp_prices("us-central1")
