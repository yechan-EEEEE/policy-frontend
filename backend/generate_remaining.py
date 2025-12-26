import os
import django
import requests
import json
import pandas as pd
from tqdm import tqdm
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finalpjt.settings')
django.setup()

from policies.models import Policy

# API 설정 (nano 모델)
API_KEY = "S14P02AR10-0799b0ea-4a18-4e9c-ba71-e09a544a3c46"
API_URL = "https://gms.ssafy.io/gmsapi/api.openai.com/v1/chat/completions"
MODEL = "gpt-5-nano"  # ← nano로 변경!

print("=" * 60)
print("🚀 나머지 1565개 정책 요약 생성 (GPT-5 nano)")
print("=" * 60)

# 1. 기존 완성된 데이터 로드
print("\n📁 기존 데이터 로딩...")
df_existing = pd.read_csv('training_data_temp.csv')
print(f"✅ 기존: {len(df_existing)}개")

# 2. 이미 처리된 정책 추출 (input에서 정책명 파싱)
processed_names = set()
for inp in df_existing['input']:
    try:
        policy_name = inp.split('정책명: ')[1].split('\n')[0]
        processed_names.add(policy_name)
    except:
        continue

print(f"✅ 처리 완료된 정책: {len(processed_names)}개")

# 3. 전체 정책 로드
all_policies = list(Policy.objects.all())
filtered = [p for p in all_policies if p.plcySprtCn and 100 < len(p.plcySprtCn) < 2000]

# 4. 미처리 정책만 필터링
remaining = [p for p in filtered if p.plcyNm not in processed_names]
print(f"✅ 남은 정책: {len(remaining)}개")

# 5. 남은 정책만 처리
summaries = []
errors = []

for idx, policy in enumerate(remaining, 1):
    try:
        prompt = f"""다음 청년 정책을 간결하게 한 문장으로 요약해주세요.

정책명: {policy.plcyNm}
내용: {policy.plcySprtCn}

요약 형식: [대상] [지원내용] [혜택/금액]"""

        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_completion_tokens": 500
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            summary = result['choices'][0]['message']['content'].strip()
            
            summaries.append({
                'input': f"정책명: {policy.plcyNm}\n내용: {policy.plcySprtCn}",
                'output': summary
            })
            
            if idx % 100 == 0:
                print(f"\n[{idx}/{len(remaining)}] 완료 ({idx/len(remaining)*100:.1f}%)")
                print(f"최근 요약: {summary[:60]}...")
                
                # 중간 저장 (기존 + 신규)
                df_new = pd.DataFrame(summaries)
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                df_combined.to_csv('training_data_combined.csv', index=False, encoding='utf-8-sig')
                print("💾 중간 저장 완료!")
        else:
            print(f"❌ 에러 [{idx}]: {response.status_code}")
            
        time.sleep(0.5)
        
    except Exception as e:
        print(f"❌ 예외 [{idx}]: {e}")
        continue

# 6. 최종 합치기
print("\n" + "=" * 60)
print("💾 최종 결과 저장 중...")

df_new = pd.DataFrame(summaries)
df_final = pd.concat([df_existing, df_new], ignore_index=True)
df_final.to_csv('training_data_2765.csv', index=False, encoding='utf-8-sig')

print(f"\n✅ 완료!")
print(f"📊 기존: {len(df_existing)}개")
print(f"📊 신규: {len(summaries)}개")
print(f"📊 총합: {len(df_final)}개")
print(f"📁 파일: training_data_2765.csv")
print("=" * 60)
