"""
네이버 뉴스 검색 API를 사용하여 AI 관련 뉴스를 수집하는 모듈
"""
import os
import urllib.request
import urllib.parse
import json
import re
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

def clean_html(text: str) -> str:
    """HTML 태그 및 특수문자 제거"""
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('&quot;', '"').replace('&amp;', '&')
    text = text.replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&apos;', "'")
    return text.strip()


def get_ai_news(query: str = "AI 인공지능", display: int = 10) -> list[dict]:
    """
    네이버 뉴스 검색 API로 AI 관련 뉴스 가져오기
    
    Args:
        query: 검색어
        display: 가져올 뉴스 개수 (최대 100)
    
    Returns:
        뉴스 리스트 [{title, link, description, pubDate}, ...]
    """
    encoded_query = urllib.parse.quote(query)
    url = f"https://openapi.naver.com/v1/search/news.json?query={encoded_query}&display={display}&sort=sim"
    
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", NAVER_CLIENT_ID)
    request.add_header("X-Naver-Client-Secret", NAVER_CLIENT_SECRET)
    
    try:
        response = urllib.request.urlopen(request)
        if response.getcode() == 200:
            data = json.loads(response.read().decode('utf-8'))
            items = data.get('items', [])
            
            news_list = []
            for item in items:
                news_list.append({
                    'title': clean_html(item.get('title', '')),
                    'link': item.get('link', ''),
                    'description': clean_html(item.get('description', '')),
                    'pubDate': item.get('pubDate', '')
                })
            
            return news_list
    except Exception as e:
        print(f"뉴스 검색 오류: {e}")
        return []


def extract_keywords(title: str) -> set:
    """제목에서 핵심 키워드 추출 (중복 비교용)"""
    # 불용어 제거
    stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 
                 '의', '이', '가', '은', '는', '을', '를', '에', '와', '과', 
                 '로', '으로', '에서', '도', '만', '까지', '부터', '에게'}
    
    # 특수문자 제거 및 소문자 변환
    clean_title = re.sub(r'[^\w\s]', ' ', title.lower())
    words = clean_title.split()
    
    # 불용어 제거 및 2글자 이상만
    keywords = {w for w in words if w not in stopwords and len(w) >= 2}
    return keywords


def is_similar_title(title1: str, title2: str, threshold: float = 0.25) -> bool:
    """두 제목의 유사도 비교 (키워드 기반)"""
    keywords1 = extract_keywords(title1)
    keywords2 = extract_keywords(title2)
    
    if not keywords1 or not keywords2:
        return False
    
    # 핵심 엔티티 (회사명, 제품명) - 이 키워드가 2개 이상 겹치면 같은 뉴스로 판단
    key_entities = {'애플', 'apple', '구글', 'google', '삼성', 'samsung', 'sk', 'lg', 
                    '네이버', 'naver', '카카오', 'kakao', '마이크로소프트', 'microsoft', 
                    'openai', 'chatgpt', '제미나이', 'gemini', '클로드', 'claude',
                    '하이닉스', '엔비디아', 'nvidia', '테슬라', 'tesla', '메타', 'meta',
                    '시총', '투자', '달러', '조원'}
    
    # 핵심 엔티티 겹침 체크
    common_keywords = keywords1 & keywords2
    common_entities = common_keywords & key_entities
    
    # 핵심 엔티티가 2개 이상 겹치면 같은 뉴스로 판단
    if len(common_entities) >= 2:
        return True
    
    # Jaccard 유사도 계산
    intersection = len(common_keywords)
    union = len(keywords1 | keywords2)
    
    similarity = intersection / union if union > 0 else 0
    return similarity >= threshold


def get_top_ai_news(count: int = 5) -> list[dict]:
    """
    AI 관련 TOP 뉴스 가져오기 (중복 제거 포함)
    
    Args:
        count: 가져올 뉴스 개수
    
    Returns:
        상위 뉴스 리스트
    """
    # 여러 검색어로 뉴스 수집
    queries = ["AI 인공지능", "ChatGPT", "생성형AI", "LLM", "머신러닝"]
    all_news = []
    seen_links = set()
    
    for query in queries:
        news = get_ai_news(query, display=15)  # 더 많이 가져와서 중복 제거 후 선별
        for item in news:
            if item['link'] not in seen_links:
                # 제목 유사도 체크 - 기존 뉴스와 너무 비슷하면 스킵
                is_duplicate = False
                for existing in all_news:
                    if is_similar_title(item['title'], existing['title']):
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    seen_links.add(item['link'])
                    all_news.append(item)
    
    # 상위 N개 반환
    return all_news[:count]


def format_news_for_kakao(news_list: list[dict]) -> str:
    """카카오톡 메시지용으로 뉴스 포맷팅"""
    today = datetime.now().strftime("%Y년 %m월 %d일")
    
    message = f"🤖 오늘의 AI 뉴스 ({today})\n\n"
    
    for i, news in enumerate(news_list, 1):
        title = news['title'][:50] + "..." if len(news['title']) > 50 else news['title']
        message += f"{i}. {title}\n"
        message += f"   👉 {news['link']}\n\n"
    
    return message


if __name__ == "__main__":
    # 테스트
    news = get_top_ai_news(5)
    print(format_news_for_kakao(news))
