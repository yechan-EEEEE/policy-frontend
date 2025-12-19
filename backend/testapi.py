import requests
import json

url = 'https://www.youthcenter.go.kr/go/ythip/getPlcy'
params = {
    'openApiVlak': '4bd0fd7f-e82b-467f-9932-b014f9588431',
    'pageIndex': 1,
    'display': 1  # 일단 1개만 가져오기
}

response = requests.get(url, params=params)
data = response.json()

# 예쁘게 출력
print(json.dumps(data, indent=2, ensure_ascii=False))