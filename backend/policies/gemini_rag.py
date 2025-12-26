import google.generativeai as genai
import os
from dotenv import load_dotenv
from django.db.models import Q

load_dotenv()

# Gemini 설정
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash')

def search_relevant_policies(query, limit=5):
    """사용자 질문과 관련된 정책 검색 (Retrieval)"""
    from .models import Policy
    
    # 키워드 추출 (간단 버전)
    keywords = query.split()
    
    # OR 검색
    q_objects = Q()
    for keyword in keywords:
        q_objects |= Q(plcyNm__icontains=keyword)
        q_objects |= Q(plcySprtCn__icontains=keyword)
        q_objects |= Q(lclsfNm__icontains=keyword)
    
    policies = Policy.objects.filter(q_objects).distinct()[:limit]
    
    return list(policies)

def generate_rag_answer(user_question):
    """RAG: 검색 + 생성"""
    
    # 1. Retrieval: 관련 정책 검색
    relevant_policies = search_relevant_policies(user_question)
    
    if not relevant_policies:
        return {
            'answer': "죄송합니다. 관련된 청년 정책을 찾지 못했습니다. 다른 키워드로 검색해주세요.",
            'policies': []
        }
    
    # 2. Context 구성
    context = "관련 정책 목록:\n\n"
    for i, policy in enumerate(relevant_policies, 1):
        context += f"{i}. {policy.plcyNm}\n"
        context += f"   분류: {policy.lclsfNm}\n"
        if policy.plcySprtCn:
            content = policy.plcySprtCn[:200] + "..." if len(policy.plcySprtCn) > 200 else policy.plcySprtCn
            context += f"   내용: {content}\n"
        context += "\n"
    
    # 3. Generation: 답변 생성
    prompt = f"""당신은 청년 정책 상담 전문가입니다.

사용자 질문: {user_question}

{context}

위 정책 정보를 바탕으로 사용자의 질문에 친절하고 구체적으로 답변해주세요.
답변 형식:
1. 간단한 인사와 질문 이해
2. 관련 정책 2-3개 소개 (정책명과 핵심 내용)
3. 추가 도움이 필요한지 물어보기

자연스럽고 친근한 말투로 답변해주세요."""

    try:
        response = model.generate_content(prompt)
        answer = response.text.strip()
        
        # 정책 정보 반환
        policy_list = [
            {
                'plcyNo': p.plcyNo,
                'plcyNm': p.plcyNm,
                'lclsfNm': p.lclsfNm
            }
            for p in relevant_policies
        ]
        
        return {
            'answer': answer,
            'policies': policy_list
        }
        
    except Exception as e:
        print(f"RAG 답변 생성 실패: {e}")
        return {
            'answer': "답변 생성 중 오류가 발생했습니다.",
            'policies': []
        }

# 테스트 함수
def test_rag():
    """RAG 챗봇 테스트"""
    
    test_questions = [
        "청년 창업 지원 정책 알려줘",
        "서울에서 월세 지원받을 수 있어?",
        "취업 준비생 지원 프로그램 있어?"
    ]
    
    print("=" * 60)
    print("RAG 챗봇 테스트")
    print("=" * 60)
    
    for question in test_questions:
        print(f"\n질문: {question}")
        print("-" * 60)
        
        result = generate_rag_answer(question)
        
        print(f"답변:\n{result['answer']}\n")
        print(f"관련 정책 {len(result['policies'])}개:")
        for p in result['policies']:
            print(f"  - {p['plcyNm']}")
        print("=" * 60)

if __name__ == "__main__":
    import django
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finalpjt.settings')
    django.setup()
    
    test_rag()
