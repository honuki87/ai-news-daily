# AI News Daily 🤖📰

매일 아침 8시에 AI 관련 인기 뉴스 TOP5를 카카오톡으로 보내주는 서비스

## 기능

- 🔍 네이버 뉴스 API로 AI 관련 뉴스 검색
- 📱 카카오톡 "나에게 보내기"로 뉴스 전송
- ⏰ Cloud Scheduler로 매일 오전 8시 자동 실행
- ☁️ Google Cloud Run에 배포

## 로컬 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 서버 실행
python main.py
```

## 테스트

```bash
# 뉴스 크롤링 테스트
python news_crawler.py

# 카카오톡 전송 테스트
python kakao_sender.py

# API 테스트
curl -X POST http://localhost:8080/send-news
```

## Cloud Run 배포

```bash
# GCP 프로젝트 설정
gcloud config set project YOUR_PROJECT_ID

# Cloud Run 배포
gcloud run deploy ai-news-daily \
  --source . \
  --region asia-northeast3 \
  --set-env-vars "NAVER_CLIENT_ID=xxx,NAVER_CLIENT_SECRET=xxx,..." \
  --allow-unauthenticated

# Cloud Scheduler 설정 (매일 오전 8시 KST)
gcloud scheduler jobs create http ai-news-job \
  --schedule="0 8 * * *" \
  --time-zone="Asia/Seoul" \
  --uri="https://YOUR_CLOUD_RUN_URL/send-news" \
  --http-method=POST
```

## 환경 변수

| 변수 | 설명 |
|------|------|
| NAVER_CLIENT_ID | 네이버 API Client ID |
| NAVER_CLIENT_SECRET | 네이버 API Client Secret |
| KAKAO_REST_API_KEY | 카카오 REST API 키 |
| KAKAO_CLIENT_SECRET | 카카오 Client Secret |
| KAKAO_ACCESS_TOKEN | 카카오 Access Token |
| KAKAO_REFRESH_TOKEN | 카카오 Refresh Token |
