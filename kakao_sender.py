"""
카카오톡 '나에게 보내기' API를 사용하여 메시지를 전송하는 모듈
"""
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")
KAKAO_CLIENT_SECRET = os.getenv("KAKAO_CLIENT_SECRET")
KAKAO_ACCESS_TOKEN = os.getenv("KAKAO_ACCESS_TOKEN")
KAKAO_REFRESH_TOKEN = os.getenv("KAKAO_REFRESH_TOKEN")


def refresh_access_token() -> str | None:
    """
    Refresh Token을 사용하여 새 Access Token 발급
    
    Returns:
        새 Access Token 또는 None
    """
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": KAKAO_REST_API_KEY,
        "refresh_token": KAKAO_REFRESH_TOKEN,
        "client_secret": KAKAO_CLIENT_SECRET
    }
    
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            result = response.json()
            new_access_token = result.get("access_token")
            print(f"토큰 갱신 성공!")
            return new_access_token
        else:
            print(f"토큰 갱신 실패: {response.text}")
            return None
    except Exception as e:
        print(f"토큰 갱신 오류: {e}")
        return None


def send_to_me(message: str, access_token: str = None) -> bool:
    """
    카카오톡 나에게 보내기
    
    Args:
        message: 보낼 메시지
        access_token: 카카오 Access Token (없으면 환경변수 사용)
    
    Returns:
        성공 여부
    """
    token = access_token or KAKAO_ACCESS_TOKEN
    
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    # 텍스트 메시지 템플릿
    template = {
        "object_type": "text",
        "text": message,
        "link": {
            "web_url": "https://news.naver.com",
            "mobile_web_url": "https://news.naver.com"
        },
        "button_title": "뉴스 더보기"
    }
    
    data = {
        "template_object": json.dumps(template)
    }
    
    try:
        response = requests.post(url, headers=headers, data=data)
        
        if response.status_code == 200:
            print("카카오톡 전송 성공!")
            return True
        elif response.status_code == 401:
            # 토큰 만료 시 갱신 후 재시도
            print("토큰 만료, 갱신 시도...")
            new_token = refresh_access_token()
            if new_token:
                return send_to_me(message, new_token)
            return False
        else:
            print(f"카카오톡 전송 실패: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"카카오톡 전송 오류: {e}")
        return False


if __name__ == "__main__":
    # 테스트
    test_message = "🤖 테스트 메시지입니다!\n\nAI News Daily 서비스가 정상 작동합니다."
    send_to_me(test_message)
