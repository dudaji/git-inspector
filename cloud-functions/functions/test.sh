curl https://pricing.api.infracost.io/graphql \
  -X POST \
  -H 'X-Api-Key: ico-oqf6aBsUqPpgRHeaKhatAHSCMjrr23Yl' \
  -H 'Content-Type: application/json' \
  --data '
  {"query": "{ products(filter: {vendorName: \"aws\", service: \"AmazonEC2\", productFamily: \"Compute Instance\", region: \"us-east-1\", attributeFilters: [{key: \"instanceType\", value: \"m3.large\"}, {key: \"operatingSystem\", value: \"Linux\"}, {key: \"tenancy\", value: \"Shared\"}, {key: \"capacitystatus\", value: \"Used\"}, {key: \"preInstalledSw\", value: \"NA\"}]}) { prices(filter: {purchaseOption: \"on_demand\"}) { USD } } } "}
  '

curl https://pricing.api.infracost.io/graphql \
  -X POST \
  -H 'X-Api-Key: ico-oqf6aBsUqPpgRHeaKhatAHSCMjrr23Yl' \
  -H 'Content-Type: application/json' \
  --data '{
    "query": "{ products(filter: {vendorName: \"aws\", service: \"AmazonEC2\", productFamily: \"Compute Instance\", region: \"us-east-1\"}) { attributes { instanceType } } }"
  }'

  curl https://pricing.api.infracost.io/graphql \
  -X POST \
  -H 'X-Api-Key: ico-oqf6aBsUqPpgRHeaKhatAHSCMjrr23Yl' \
  -H 'Content-Type: application/json' \
  --data '{
    "query": "{ products(filter: {vendorName: \"aws\", service: \"AmazonEC2\", productFamily: \"Compute Instance\", region: \"us-east-1\"}) { attributes { key value } } }"
  }'
