# 청년 정책 추천 플랫폼 API 문서

## 기본 정보
- **Base URL**: `http://127.0.0.1:8000/api`
- **인증 방식**: Session Authentication (Cookie 기반)
- **응답 형식**: JSON

---

## 🔐 회원 관리 (accounts)

### 회원가입
- **POST** `/accounts/signup/`
- **Body**:
```json
{
    "username": "testuser",
    "password": "password123",
    "password2": "password123",
    "real_name": "홍길동",
    "birth_date": "1999-01-15",
    "region": "서울특별시",
    "job": "개발자",
    "gender": "M"
}
```
- **Response**: User 정보

### 로그인
- **POST** `/accounts/login/`
- **Body**:
```json
{
    "username": "testuser",
    "password": "password123"
}
```

### 로그아웃
- **POST** `/accounts/logout/`
- **인증 필요**: ✅

### 내 정보 조회
- **GET** `/accounts/profile/`
- **인증 필요**: ✅

### 내 정보 수정
- **PUT** `/accounts/profile/update/`
- **인증 필요**: ✅
- **Body**: 수정할 필드만 (partial update)

### 회원탈퇴
- **DELETE** `/accounts/delete/`
- **인증 필요**: ✅

---

## 📋 게시판 (community)

### 게시글 목록 조회
- **GET** `/community/posts/`
- **Query Parameters**:
  - `search`: 제목 검색
  - `ordering`: `popular` (인기순) 또는 생략 (최신순)
- **예시**: `/community/posts/?search=창업&ordering=popular`

### 게시글 작성
- **POST** `/community/posts/`
- **인증 필요**: ✅
- **Body**:
```json
{
    "title": "게시글 제목",
    "content": "게시글 내용"
}
```

### 게시글 상세 조회
- **GET** `/community/posts/{post_id}/`

### 게시글 수정
- **PUT** `/community/posts/{post_id}/`
- **인증 필요**: ✅ (본인만)
- **Body**: 수정할 내용

### 게시글 삭제
- **DELETE** `/community/posts/{post_id}/`
- **인증 필요**: ✅ (본인만)

### 게시글 좋아요/취소
- **POST** `/community/posts/{post_id}/like/`
- **인증 필요**: ✅

---

## 💬 댓글 (community)

### 댓글 목록 조회
- **GET** `/community/posts/{post_id}/comments/`

### 댓글 작성
- **POST** `/community/posts/{post_id}/comments/`
- **인증 필요**: ✅
- **Body**:
```json
{
    "content": "댓글 내용"
}
```

### 댓글 수정
- **PUT** `/community/comments/{comment_id}/`
- **인증 필요**: ✅ (본인만)

### 댓글 삭제
- **DELETE** `/community/comments/{comment_id}/`
- **인증 필요**: ✅ (본인만)

### 댓글 좋아요/취소
- **POST** `/community/comments/{comment_id}/like/`
- **인증 필요**: ✅

---

## 🎯 정책 (policies)

### 정책 목록 조회
- **GET** `/policies/list/`
- **Query Parameters**:
  - `search`: 정책명 검색
  - `region`: 지역 필터 (예: 서울특별시)
  - `category`: 분류 필터 (예: 일자리)
- **예시**: `/policies/list/?search=창업&region=경기도&category=일자리`

### 정책 상세 조회
- **GET** `/policies/{plcyNo}/`

### 정책 좋아요/취소
- **POST** `/policies/{plcyNo}/like/`
- **인증 필요**: ✅

### AI 추천 정책
- **GET** `/policies/recommend/ai/`
- **인증 필요**: ✅
- **설명**: 로그인한 사용자의 나이, 지역 기반 맞춤 추천

### 정책 AI 요약 ✨
- **POST** `/policies/{plcyNo}/summarize/`
- **Response**:
```json
{
    "plcyNo": "...",
    "plcyNm": "정책명",
    "summary": "AI 요약 내용"
}
```

### 온통청년 API 데이터 수집 (관리자용)
- **POST** `/policies/fetch/data/`

---

## 📝 주요 필드 설명

### User
- `username`: 로그인 ID (닉네임으로도 사용)
- `real_name`: 실명
- `birth_date`: 생년월일 (YYYY-MM-DD)
- `region`: 시/도 (예: 서울특별시, 경기도)
- `job`: 직업
- `gender`: 성별 (M/F)

### Policy
- `plcyNo`: 정책번호 (Primary Key)
- `plcyNm`: 정책명
- `plcyExplnCn`: 정책 설명
- `lclsfNm`: 대분류 (일자리, 주거 등)
- `mclsfNm`: 중분류 (창업, 취업 등)
- `sprvsnInstCdNm`: 지역
- `liked_count`: 좋아요 수

---

## 🚀 CORS 설정
프론트엔드 개발 서버: `http://localhost:5173`

---

## 📌 참고사항
1. 로그인 후 Cookie로 세션 유지
2. 모든 날짜는 ISO 8601 형식
3. 에러 응답은 JSON 형태로 제공

# Backend API 배포 완료! 

## API Base URL
http://43.201.38.152

## 설정 필요사항
Vue 프로젝트에서:
- API_BASE_URL = 'http://43.201.38.152/api'

## API 문서
API_DOCS.md 참고

## CORS
- 현재: localhost:5173 허용됨
- Frontend 배포 URL 나오면 알려줘! (CORS 추가해줄게)

## 테스트 계정
- Username: admin
- Password: (직접 전달)
