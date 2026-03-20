# 🚀 Google Cloud Run 배포 가이드 (초보자용)

AI News Daily 서비스를 Google Cloud Run에 배포하는 단계별 가이드입니다.

---

## 📋 목차

0. [긴급 보안 조치](#0-긴급-보안-조치)
1. [사전 준비](#1-사전-준비)
2. [Google Cloud SDK 설치](#2-google-cloud-sdk-설치)
3. [GCP 프로젝트 설정](#3-gcp-프로젝트-설정)
4. [Cloud Run 배포](#4-cloud-run-배포)
5. [Cloud Scheduler 설정](#5-cloud-scheduler-설정)
6. [트러블슈팅](#6-트러블슈팅)

---

## 0. 긴급 보안 조치

이 저장소에 실제 키나 토큰을 올린 적이 있다면 아래부터 먼저 진행하세요.

1. 네이버 API 시크릿 재발급
2. 카카오 Client Secret 재발급
3. 카카오 Access Token, Refresh Token 새로 발급
4. 새 값만 로컬 `env.yaml`에 저장
5. 다시 배포

> 중요: GitHub에서 파일을 지워도 이미 노출된 키와 토큰은 안전해지지 않습니다. 반드시 새 값으로 교체해야 합니다.

---

## 1. 사전 준비

### 필요한 것
- ✅ Google 계정
- ✅ 신용카드 (무료 체험용, 실제 결제 없음)
- ✅ 이 프로젝트 파일들
- ✅ 새로 발급한 네이버/카카오 키와 토큰

### 비용 안내
> 💡 Cloud Run은 소규모 사용량에서는 무료 범위 안에 들어가는 경우가 많습니다.

---

## 2. Google Cloud SDK 설치

### Windows에서 설치

1. [Google Cloud SDK 설치 페이지](https://cloud.google.com/sdk/docs/install) 접속
2. Windows용 설치 프로그램 다운로드
3. 설치 후 `Run 'gcloud init'` 체크
4. 브라우저에서 Google 계정 로그인

### 설치 확인
```powershell
gcloud --version
```

---

## 3. GCP 프로젝트 설정

### 3-1. Google Cloud Console 접속
1. [Google Cloud Console](https://console.cloud.google.com) 접속
2. Google 계정으로 로그인

### 3-2. 새 프로젝트 생성
1. 상단 프로젝트 선택 드롭다운 클릭
2. `새 프로젝트` 클릭
3. 프로젝트 이름 입력: `ai-news-daily`
4. `만들기` 클릭

### 3-3. 결제 계정 연결 (처음만)
1. 왼쪽 메뉴 → `결제`
2. `결제 계정 연결` 클릭
3. 카드 정보 입력

### 3-4. 필요한 API 활성화
다음 API를 켜세요.

- Cloud Run Admin API
- Cloud Build API
- Artifact Registry API
- Cloud Scheduler API

### 3-5. 터미널에서 프로젝트 설정
```powershell
gcloud config set project YOUR_PROJECT_ID
```

예시:
```powershell
gcloud config set project ai-news-daily-123456
```

---

## 4. Cloud Run 배포

### 4-1. 프로젝트 폴더로 이동
```powershell
cd "c:\Users\JonghoWoo\Desktop\#Sublime\antiGravity\ai-news-daily"
```

### 4-2. 배포용 환경 변수 파일 만들기
저장소에 있는 예시 파일을 복사해 로컬 전용 파일을 만듭니다.

```powershell
Copy-Item env.example.yaml env.yaml
```

### 4-3. `env.yaml`에 실제 값 입력
`env.yaml` 안에 아래 항목의 실제 값을 넣습니다.

```yaml
NAVER_CLIENT_ID: "실제 네이버 Client ID"
NAVER_CLIENT_SECRET: "실제 네이버 Client Secret"
KAKAO_REST_API_KEY: "실제 카카오 REST API 키"
KAKAO_CLIENT_SECRET: "실제 카카오 Client Secret"
KAKAO_ACCESS_TOKEN: "실제 카카오 Access Token"
KAKAO_REFRESH_TOKEN: "실제 카카오 Refresh Token"
```

> 주의: `env.yaml`은 Git에 올리면 안 됩니다.

### 4-4. 배포 명령 실행
```powershell
gcloud run deploy ai-news-daily `
  --source . `
  --region asia-northeast3 `
  --env-vars-file env.yaml `
  --allow-unauthenticated
```

### 4-5. 배포 중 질문 응답
배포 중 아래 질문이 나오면 모두 `y`로 답하면 됩니다.

- Enable Artifact Registry API?
- Enable Cloud Build API?
- Allow unauthenticated invocations?

### 4-6. 배포 완료 확인
배포가 완료되면 아래와 비슷한 메시지가 나옵니다.

```text
Service [ai-news-daily] revision [...] has been deployed
Service URL: https://ai-news-daily-xxxxx-an.a.run.app
```

### 4-7. 테스트
브라우저에서 서비스 URL에 접속합니다.

예상 응답:
```json
{"status": "healthy", "service": "AI News Daily"}
```

---

## 5. Cloud Scheduler 설정

### 5-1. Cloud Console에서 설정
1. [Cloud Scheduler](https://console.cloud.google.com/cloudscheduler) 접속
2. `작업 만들기` 클릭

### 5-2. 작업 정보 입력

| 항목 | 값 |
|------|-----|
| 이름 | `ai-news-daily-job` |
| 리전 | `asia-northeast3 (서울)` |
| 설명 | `매일 오전 8시 AI 뉴스 전송` |
| 빈도 | `0 8 * * *` |
| 시간대 | `Asia/Seoul` |

### 5-3. 실행 구성

| 항목 | 값 |
|------|-----|
| 대상 유형 | `HTTP` |
| URL | `https://YOUR_CLOUD_RUN_URL/send-news` |
| HTTP 메서드 | `POST` |

### 5-4. 즉시 테스트
1. 생성된 작업 옆 `⋮` 클릭
2. `지금 실행` 클릭
3. 카카오톡 도착 여부 확인

---

## 6. 트러블슈팅

### 문제: `Permission denied`
```powershell
gcloud auth login
```

### 문제: `Project not found`
```powershell
gcloud config set project YOUR_ACTUAL_PROJECT_ID
```

### 문제: 배포 실패
```powershell
gcloud run logs read --service ai-news-daily --region asia-northeast3
```

### 문제: 카카오톡 전송 안됨
가능성이 큰 순서대로 확인하세요.

1. 카카오 Refresh Token 만료 또는 무효화
2. 새 Access Token, Refresh Token을 발급하지 않음
3. `env.yaml`을 갱신하지 않음
4. 갱신 후 재배포하지 않음

해결 방법:

1. 카카오에서 새 토큰 발급
2. `env.yaml` 값 교체
3. 아래 명령으로 다시 배포

```powershell
gcloud run deploy ai-news-daily `
  --source . `
  --region asia-northeast3 `
  --env-vars-file env.yaml `
  --allow-unauthenticated
```

---

## 📌 유용한 명령어

```powershell
# 배포된 서비스 목록
gcloud run services list

# 서비스 삭제
gcloud run services delete ai-news-daily --region asia-northeast3

# 로그 실시간 확인
gcloud run logs tail --service ai-news-daily --region asia-northeast3
```

---

## ✅ 완료

이제 실제 키와 토큰은 로컬 파일에만 보관하고, Cloud Run에는 안전한 파일 기반 방식으로 배포하면 됩니다.
