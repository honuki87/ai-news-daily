# AI News Daily 🤖📰

매일 아침 8시에 AI 관련 인기 뉴스 TOP5를 카카오톡으로 보내주는 서비스

## 기능

- 🔍 네이버 뉴스 API로 AI 관련 뉴스 검색
- 📱 카카오톡 "나에게 보내기"로 뉴스 전송
- ⏰ Cloud Scheduler로 매일 오전 8시 자동 실행
- ☁️ Google Cloud Run에 배포

## 보안 주의

- 실제 API 키와 토큰은 저장소에 커밋하지 마세요.
- Cloud Run 배포용 값은 로컬 `env.yaml`에만 넣고 Git에는 올리지 않습니다.
- 한 번이라도 공개 저장소에 올라간 키와 토큰은 삭제가 아니라 폐기 후 재발급 대상입니다.

## 로컬 실행

1. 의존성 설치
```bash
pip install -r requirements.txt
```

2. 환경 변수 파일 준비
```powershell
Copy-Item .env.example .env
```

3. `.env` 파일에 실제 값을 입력한 뒤 서버 실행
```bash
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

1. 프로젝트 설정
```powershell
gcloud config set project YOUR_PROJECT_ID
```

2. 배포용 환경 변수 파일 준비
```powershell
Copy-Item env.example.yaml env.yaml
```

3. `env.yaml`에 실제 값을 입력

4. Cloud Run 배포
```powershell
gcloud run deploy ai-news-daily `
  --source . `
  --region asia-northeast3 `
  --env-vars-file env.yaml `
  --allow-unauthenticated
```

5. Cloud Scheduler 설정 (매일 오전 8시 KST)
```powershell
gcloud scheduler jobs create http ai-news-job `
  --schedule="0 8 * * *" `
  --time-zone="Asia/Seoul" `
  --uri="https://YOUR_CLOUD_RUN_URL/send-news" `
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

## 운영 팁

- 카카오 Access Token은 짧게 유지되고, Refresh Token도 주기적으로 재발급이 필요할 수 있습니다.
- 발송이 멈추면 새 토큰을 발급받아 `env.yaml` 값을 바꾸고 다시 배포하세요.
- 공유 PC라면 배포 후 로컬 `env.yaml` 파일을 안전한 위치에 보관하거나 삭제하세요.
