import requests
import json
from bs4 import BeautifulSoup


from clouds.aws import aws
from functions.clouds.get_azure_price import azure
from clouds.gcp import gcp


def get_aws_prices():
    # AWS Price List API 사용
    # 구현 필요
    pass


def get_azure_prices():
    # Azure Retail Prices API 사용
    # 구현 필요
    pass


def get_gcp_prices():
    # Google Cloud Billing API 사용
    # 구현 필요
    pass


def crawl_prices(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    # 웹 페이지의 특정 요소를 찾고 가격 정보를 추출하는 로직 구현
    pass


def convert_currency(amount, from_currency, to_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(url)
    data = response.json()
    rate = data["rates"].get(to_currency)
    if rate:
        return amount * rate
    return None


def main():
    aws_prices = get_aws_prices()
    azure_prices = get_azure_prices()
    gcp_prices = get_gcp_prices()

    # 결과 처리 및 출력
    print("AWS Prices:", json.dumps(aws_prices, indent=2))
    print("Azure Prices:", json.dumps(azure_prices, indent=2))
    print("GCP Prices:", json.dumps(gcp_prices, indent=2))


if __name__ == "__main__":
    main()
