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

# API 설정
API_KEY = "S14P02AR10-0799b0ea-4a18-4e9c-ba71-e09a544a3c46"
API_URL = "https://gms.ssafy.io/gmsapi/api.openai.com/v1/chat/completions"
MODEL = "gpt-5-nano"

print("=" * 60)
print("🚀 2000개 정책 요약 자동 생성 (GPT-5 nano)")
print("=" * 60)

# 1. 전체 정책 로드
print("\n📊 정책 데이터 로딩 중...")
all_policies = list(Policy.objects.all())
print(f"전체 정책: {len(all_policies)}개")

# 2. 유효한 정책 필터링
filtered = [p for p in all_policies if p.plcySprtCn and 100 < len(p.plcySprtCn) < 2000]
print(f"유효한 정책: {len(filtered)}개")

# 3. 2000개 샘플링
import random
random.shuffle(filtered)
selected = filtered[:2000]

print(f"\n✅ 2000개 정책 선정 완료!")
print(f"⏱️  예상 시간: 20-30분")
print(f"💰 예상 크레딧: 6,000개")
print("\n" + "=" * 60)

# 4. 요약 생성
summaries = []
errors = []

for idx, policy in enumerate(selected, 1):
    try:
        prompt = f"""다음 청년 정책을 간결하게 한 문장으로 요약해주세요.

정책명: {policy.plcyNm}
내용: {policy.plcySprtCn}

요약 형식: [대상] [지원내용] [혜택/금액]
예시: 서울 거주 청년 대상 월세 지원으로 최대 20만원 12개월간 지급"""

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
            content = result['choices'][0]['message']['content']
            
            # 디버깅: 첫 3개 응답 전체 출력
            if idx <= 3:
                print(f"\n{'=' * 60}")
                print(f"[디버깅 {idx}] 전체 응답:")
                print(json.dumps(result, indent=2, ensure_ascii=False))
                print(f"\nContent: '{content}'")
                print(f"Content 길이: {len(content) if content else 0}")
                print(f"finish_reason: {result['choices'][0].get('finish_reason')}")
                print('=' * 60)
            
            # 빈 응답 체크
            if content and content.strip():
                summary = content.strip()
                
                summaries.append({
                    'input': f"정책명: {policy.plcyNm}\n내용: {policy.plcySprtCn}",
                    'output': summary
                })
                
                # 진행상황
                if idx % 100 == 0:
                    print(f"\n[{idx}/2000] 완료 ({idx/2000*100:.1f}%)")
                    print(f"최근 요약: {summary[:60]}...")
                    
                    # 중간 저장
                    df_temp = pd.DataFrame(summaries)
                    df_temp.to_csv('training_data_progress.csv', index=False, encoding='utf-8-sig')
                    print(f"💾 중간 저장 완료! (현재: {len(summaries)}개)")
            else:
                print(f"⚠️  [{idx}] 빈 응답!")
                errors.append(f"[{idx}] Empty content")
        else:
            print(f"❌ 에러 [{idx}]: {response.status_code}")
            if idx <= 3:
                print(f"응답 내용: {response.text[:200]}")
            errors.append(f"[{idx}] HTTP {response.status_code}")
            
        # Rate limit 방지
        time.sleep(0.5)
        
    except Exception as e:
        print(f"❌ 예외 [{idx}]: {e}")
        errors.append(f"[{idx}] Exception: {str(e)}")
        continue

# 5. 최종 저장
print("\n" + "=" * 60)
print("💾 최종 결과 저장 중...")

df_final = pd.DataFrame(summaries)
df_final.to_csv('training_data_2000.csv', index=False, encoding='utf-8-sig')

print(f"\n✅ 완료!")
print(f"📊 성공: {len(summaries)}개")
print(f"❌ 실패: {len(errors)}개")
print(f"📁 파일: training_data_2000.csv")

if errors:
    print(f"\n⚠️  에러 샘플 (처음 10개):")
    for err in errors[:10]:
        print(f"  - {err}")

print("=" * 60)
