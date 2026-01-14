# 🚀 Google Cloud Run 배포 가이드 (초보자용)

AI News Daily 서비스를 Google Cloud Run에 배포하는 단계별 가이드입니다.

---

## 📋 목차

1. [사전 준비](#1-사전-준비)
2. [Google Cloud SDK 설치](#2-google-cloud-sdk-설치)
3. [GCP 프로젝트 설정](#3-gcp-프로젝트-설정)
4. [Cloud Run 배포](#4-cloud-run-배포)
5. [Cloud Scheduler 설정](#5-cloud-scheduler-설정)
6. [트러블슈팅](#6-트러블슈팅)

---

## 1. 사전 준비

### 필요한 것
- ✅ Google 계정
- ✅ 신용카드 (무료 체험용, 실제 결제 없음)
- ✅ 이 프로젝트 파일들

### 비용 안내
> 💡 **무료입니다!** Cloud Run은 월 200만 요청까지 무료이고, 매일 1번 호출이면 월 30회뿐입니다.

---

## 2. Google Cloud SDK 설치

### Windows에서 설치

1. **Google Cloud SDK 다운로드**
   - https://cloud.google.com/sdk/docs/install 접속
   - **Windows용 설치 프로그램** 다운로드

2. **설치 실행**
   - 다운로드한 `GoogleCloudSDKInstaller.exe` 실행
   - 기본 옵션으로 설치 진행
   - "Run 'gcloud init'" 체크박스 선택

3. **초기화**
   - 설치 완료 후 터미널이 열리면:
   ```
   Welcome to the Google Cloud CLI!
   ```
   - `Y`를 입력하여 로그인 진행
   - 브라우저에서 Google 계정 로그인

### 설치 확인
```powershell
gcloud --version
```
버전 정보가 출력되면 성공!

---

## 3. GCP 프로젝트 설정

### 3-1. Google Cloud Console 접속
1. https://console.cloud.google.com 접속
2. Google 계정으로 로그인

### 3-2. 새 프로젝트 생성
1. 상단의 프로젝트 선택 드롭다운 클릭
2. **"새 프로젝트"** 클릭
3. 프로젝트 이름 입력: `ai-news-daily` (원하는 이름)
4. **"만들기"** 클릭

### 3-3. 결제 계정 연결 (처음만)
1. 왼쪽 메뉴 → **결제**
2. **"결제 계정 연결"** 클릭
3. 신용카드 정보 입력 (무료 체험, 실제 결제 없음)

### 3-4. 필요한 API 활성화
1. 왼쪽 메뉴 → **API 및 서비스** → **라이브러리**
2. 다음 API들을 검색하여 **"사용 설정"** 클릭:
   - Cloud Run Admin API
   - Cloud Build API
   - Artifact Registry API
   - Cloud Scheduler API

### 3-5. 터미널에서 프로젝트 설정
```powershell
# 프로젝트 ID 확인 (Console에서 복사)
gcloud config set project YOUR_PROJECT_ID

# 예시:
gcloud config set project ai-news-daily-123456
```

---

## 4. Cloud Run 배포

### 4-1. 프로젝트 폴더로 이동
```powershell
cd "c:\Users\JonghoWoo\Desktop\#Sublime\antiGravity\ai-news-daily"
```

### 4-2. 배포 명령 실행
아래 명령어를 **한 줄로** 복사해서 실행하세요:

```powershell
gcloud run deploy ai-news-daily --source . --region asia-northeast3 --set-env-vars "NAVER_CLIENT_ID=ccZw7DNm6bzY_90DXrKt,NAVER_CLIENT_SECRET=tQrLAMEDnL,KAKAO_REST_API_KEY=d0981cf383b39a8b6e5d77379f9d9346,KAKAO_CLIENT_SECRET=svOWX6Gdzbj2gghOevEe0szWC93dybet,KAKAO_ACCESS_TOKEN=YpvOKCKECNJ9amRnWSsrurls2bcye0aDAAAAAQoNG5oAAAGbsZX1D0e54X7lJw5n,KAKAO_REFRESH_TOKEN=yeXeYhGghOzSOLlCPgHyS7Pwnvok4kGJAAAAAgoNG5oAAAGbsZX1DEe54X7lJw5n" --allow-unauthenticated
```

### 4-3. 배포 중 질문 응답
배포 중 몇 가지 질문이 나올 수 있습니다:

| 질문 | 답변 |
|------|------|
| Enable Artifact Registry API? | `y` |
| Enable Cloud Build API? | `y` |
| Allow unauthenticated invocations? | `y` |

### 4-4. 배포 완료 확인
배포가 완료되면 이런 메시지가 나옵니다:
```
Service [ai-news-daily] revision [...] has been deployed
Service URL: https://ai-news-daily-xxxxx-an.a.run.app
```

**이 URL을 복사해두세요!** (다음 단계에서 사용)

### 4-5. 테스트
브라우저에서 `https://ai-news-daily-xxxxx-an.a.run.app` 접속

아래와 같이 나오면 성공:
```json
{"status": "healthy", "service": "AI News Daily"}
```

---

## 5. Cloud Scheduler 설정

### 5-1. Cloud Console에서 설정
1. https://console.cloud.google.com/cloudscheduler 접속
2. **"작업 만들기"** 클릭

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
| URL | `https://ai-news-daily-xxxxx-an.a.run.app/send-news` |
| HTTP 메서드 | `POST` |

> ⚠️ URL은 위에서 배포 후 받은 URL + `/send-news`

### 5-4. 저장
**"만들기"** 클릭

### 5-5. 즉시 테스트
1. 생성된 작업 옆의 **⋮** (더보기) 클릭
2. **"지금 실행"** 클릭
3. 카카오톡 확인!

---

## 6. 트러블슈팅

### 문제: "Permission denied" 오류
```powershell
gcloud auth login
```

### 문제: "Project not found" 오류
```powershell
gcloud config set project YOUR_ACTUAL_PROJECT_ID
```

### 문제: 배포 실패
```powershell
# 로그 확인
gcloud run logs read --service ai-news-daily --region asia-northeast3
```

### 문제: 카카오톡 전송 안됨
- 토큰이 만료되었을 수 있음
- 새 토큰 발급 후 환경변수 업데이트 필요

---

## 📌 유용한 명령어

```powershell
# 배포된 서비스 목록
gcloud run services list

# 서비스 삭제
gcloud run services delete ai-news-daily --region asia-northeast3

# 환경변수 업데이트
gcloud run services update ai-news-daily --region asia-northeast3 --set-env-vars "KEY=VALUE"

# 로그 실시간 확인
gcloud run logs tail --service ai-news-daily --region asia-northeast3
```

---

## ✅ 완료!

이제 매일 아침 8시에 AI 뉴스가 카카오톡으로 전송됩니다! 🎉
