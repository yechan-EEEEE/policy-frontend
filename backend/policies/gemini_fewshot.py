import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Gemini 설정
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash')

# Few-shot 예시 (위에서 선정한 5개)
EXAMPLES = [
    {
        "input": """정책명: 충북 청년여성 일자리 플랫폼 운영
내용: 취·창업지원, 전문교육, 멘토링, 커뮤니티 공간 제공 등""",
        "output": "충북 청년여성을 위한 취·창업 지원 및 커뮤니티 공간(청춘잡담) 운영"
    },
    {
        "input": """정책명: 김해시 신혼 첫 주택 리모델링 지원사업
내용: 리모델링 공사비의 50%, 최대 500만원 지원""",
        "output": "김해시 신혼부부의 첫 주택 리모델링 비용 일부 지원"
    },
    {
        "input": """정책명: 미래내일일경험 인턴형 호텔인터불고 참여자 모집
내용: 1주 직무교육 후 4~16주 인턴십 수행, 주 35만원 수당 지급""",
        "output": "호텔 직무 교육 및 인턴십 기회 제공과 주당 35만원의 수당 지원"
    },
    {
        "input": """정책명: 서울청년센터 강서 <치아미백 무료 지원>
내용: 검진, 스케일링, 미백치료 등 50만원 상당 시술 지원""",
        "output": "강서구 청년 대상 전문 치과 의료 서비스 무료 제공"
    },
    {
        "input": """정책명: 서귀포시 청년정책협의체 운영
내용: 청년 의견 수렴, 정책 발굴, 타 시도 네트워크 교류 활동 등""",
        "output": "서귀포 청년들이 직접 정책을 제안하고 시정에 참여하는 협의체 운영"
    }
]

def create_fewshot_prompt(policy_name, policy_content):
    """Few-shot 프롬프트 생성"""
    
    # 예시 포맷팅
    examples_text = ""
    for i, ex in enumerate(EXAMPLES, 1):
        examples_text += f"""
[예시 {i}]
{ex['input']}

→ 요약: {ex['output']}

"""
    
    # 최종 프롬프트
    prompt = f"""당신은 청년정책 전문가입니다. 다음 예시들을 참고하여 청년정책을 간결하게 한 문장으로 요약해주세요.

{examples_text}

이제 다음 정책을 같은 형식으로 요약해주세요:

정책명: {policy_name}
내용: {policy_content}

→ 요약:"""
    
    return prompt

def summarize_policy_fewshot(policy_name, policy_content):
    """Few-shot을 사용한 정책 요약"""
    
    try:
        # Few-shot 프롬프트 생성
        prompt = create_fewshot_prompt(policy_name, policy_content)
        
        # Gemini 호출
        response = model.generate_content(prompt)
        summary = response.text.strip()

        summary = summary.replace("→ 요약:", "").strip()
        summary = summary.replace("**요약:**", "").strip()
        summary = summary.replace("요약:", "").strip() 
        
        return summary
        
    except Exception as e:
        print(f"요약 생성 실패: {e}")
        return None

# 테스트 함수
def test_fewshot():
    """Few-shot 테스트"""
    
    test_policy = {
        "name": "청년 자기개발 도서구입비 지원",
        "content": "도서 구입비의 80%(최대 10만원) 환급 지원"
    }
    
    print("=" * 60)
    print("Few-shot Prompting 테스트")
    print("=" * 60)
    print(f"\n정책명: {test_policy['name']}")
    print(f"내용: {test_policy['content']}")
    
    summary = summarize_policy_fewshot(test_policy['name'], test_policy['content'])
    
    print(f"\n요약: {summary}")
    print("=" * 60)

if __name__ == "__main__":
    test_fewshot()
