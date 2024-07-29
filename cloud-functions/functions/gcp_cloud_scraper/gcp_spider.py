import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
import scrapy
from scrapy.crawler import CrawlerProcess

# from google.cloud import firestore
from datetime import datetime

# from pydantic import BaseModel, Field
from typing import List, Optional
from functions.clouds.model import CloudCost

# from functions.clouds._firestore import save_to_firestore


class GcpSpider(scrapy.Spider):
    name = "gcp_spider"
    allowed_domains = ["cloud.google.com"]

    start_urls = [
        "https://cloud.google.com/products/calculator?hl=ko&dl=CiQwZWQ5MTMxNC1jYjgwLTRiOTYtODk4ZS1mNTVkYTlmNDRjMjUQCBokRUVCQjRGQkUtQkQxRS00M0M2LUI1QzAtRDA1MzA3MDg1N0U4",
    ]

    def parse(self, response):
        regions = ["asia-northeast3", "us-central1"]
        for region in regions:
            url = self.get_region_url(region)
            yield scrapy.Request(
                url=url, callback=self.parse_series, meta={"region": region}
            )

    def get_region_url(self, region):
        region_urls = {
            "asia-northeast3": "https://cloud.google.com/products/calculator/?region=asia-northeast3&hl=ko",
            "us-central1": "https://cloud.google.com/products/calculator/?region=us-central1&hl=ko",
        }
        return region_urls[region]

    def parse_series(self, response):
        region = response.meta["region"]
        series_options = response.xpath('//select[@id="series"]/option')
        for option in series_options:
            series_value = option.xpath("@value").get()
            series_name = option.xpath("text()").get()
            if series_value:
                url = f"https://cloud.google.com/products/calculator/?region={region}&series={series_value}&hl=ko"
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_machine_types,
                    meta={"region": region, "series": series_name},
                )

    def parse_machine_types(self, response):
        region = response.meta["region"]
        series = response.meta["series"]
        machine_types = response.xpath('//select[@id="machine-type"]/option')
        for option in machine_types:
            machine_type_value = option.xpath("@value").get()
            machine_type_name = option.xpath("text()").get()
            if machine_type_value:
                url = f"https://cloud.google.com/products/calculator/?region={region}&series={series}&machine-type={machine_type_value}&hl=ko"
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_machine_details,
                    meta={
                        "region": region,
                        "series": series,
                        "machine_type": machine_type_name,
                    },
                )

    def parse_machine_details(self, response):
        region = response.meta["region"]
        machine_type = response.meta["machine_type"]
        vcpu = response.xpath('//input[@id="vcpu"]/@value').get()
        ram = response.xpath('//input[@id="ram"]/@value').get()
        cost_per_hour = response.xpath(
            '//input[@id="cost-per-hour"]/@value'
        ).get()

        if vcpu and ram and cost_per_hour:
            extraction_date = datetime.utcnow().strftime("%Y-%m-%d")
            cloud_cost = CloudCost(
                vendor="GCP",
                name=machine_type,
                region=region,
                cpu=float(vcpu),
                ram=float(ram.replace(" GB", "")),
                cost_per_hour=float(cost_per_hour.replace("$", "")),
                extraction_date=extraction_date,
            )
            print(cloud_cost)


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(GcpSpider)
    process.start()
