#!/usr/bin/env python
# coding: utf-8

import requests

#url = 'http://localhost:8080/2015-03-31/functions/function/invocations'

url = 'https://oe6aug0jqj.execute-api.sa-east-1.amazonaws.com/Test/predict'


data = {'url': 'https://raw.githubusercontent.com/mary435/kitchenware_classification/main/images/6172.jpg'}

result = requests.post(url, json=data).json()
print(result)