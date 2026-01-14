FROM python:3.11-slim

WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# 환경 변수 (Cloud Run에서 설정)
ENV PORT=8080

# 서버 실행
CMD ["gunicorn", "--bind", ":8080", "--workers", "1", "--threads", "2", "main:app"]
