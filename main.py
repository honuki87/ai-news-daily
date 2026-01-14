"""
AI News Daily - Flask 서버
Cloud Run에서 실행되며, Cloud Scheduler에 의해 트리거됨
"""
import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv

from news_crawler import get_top_ai_news, format_news_for_kakao
from kakao_sender import send_to_me

load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def health_check():
    """헬스체크 엔드포인트"""
    return jsonify({
        "status": "healthy",
        "service": "AI News Daily"
    })


@app.route("/send-news", methods=["POST", "GET"])
def send_news():
    """
    AI 뉴스를 수집하여 카카오톡으로 전송
    Cloud Scheduler가 매일 아침 8시에 호출
    """
    try:
        # AI 뉴스 TOP 5 가져오기
        news_list = get_top_ai_news(5)
        
        if not news_list:
            return jsonify({
                "success": False,
                "message": "뉴스를 가져오지 못했습니다."
            }), 500
        
        # 카카오톡 메시지 포맷팅
        message = format_news_for_kakao(news_list)
        
        # 카카오톡으로 전송
        success = send_to_me(message)
        
        if success:
            return jsonify({
                "success": True,
                "message": "AI 뉴스가 카카오톡으로 전송되었습니다.",
                "news_count": len(news_list)
            })
        else:
            return jsonify({
                "success": False,
                "message": "카카오톡 전송에 실패했습니다."
            }), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"오류 발생: {str(e)}"
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
