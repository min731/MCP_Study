# news.py

from fastmcp import FastMCP
from datetime import date 

news_db = [
    {"title": "한국, AI 반도체 시장 주도권 경쟁 본격화", "category": "IT", "date": "2025-09-15", "content": "차세대 AI 반도체 개발에 국내 기업들이 대규모 투자를 발표하며 기술 경쟁에 불을 지폈다."},
    {"title": "정부, 부동산 안정화 위한 추가 대책 발표", "category": "경제", "date": "2025-09-16", "content": "정부는 오늘 오전 부동산 시장 안정을 목표로 하는 새로운 공급 및 규제 정책을 공개했다."},
    {"title": "가을 단풍 절정, 주말 나들이객으로 국립공원 '북적'", "category": "사회", "date": "2025-09-15", "content": "완연한 가을 날씨 속에 전국의 산들이 오색 단풍으로 물들자 등산객들의 발길이 이어지고 있다."},
    {"title": "CES 2026, 핵심 키워드는 '초연결 사회'", "category": "IT", "date": "2025-09-17", "content": "내년 초 열릴 세계 최대 IT 전시회 CES의 주제가 공개되며 기술 업계의 이목이 집중되고 있다."},
    {"title": "한국은행, 기준금리 동결 결정... 경기 관망세", "category": "경제", "date": "2025-09-17", "content": "금융통화위원회는 오늘 기준금리를 현 수준으로 유지하기로 만장일치로 결정했다."}
]

mcp = FastMCP(name="뉴스 검색 서버")

@mcp.tool()
def search_by_category(category: str) -> list[dict] | str:
    """주어진 카테고리에 해당하는 모든 뉴스를 찾습니다. (예: IT, 경제, 사회)"""
    print(f"도구 실행: search_by_category('{category}')")
    # 카테고리가 정확히 일치하는 뉴스를 필터링합니다.
    results = [news for news in news_db if category.lower() == news["category"].lower()]
    
    if not results:
        return f"'{category}' 카테고리의 뉴스를 찾을 수 없습니다."
    return results

@mcp.tool()
def search_since_date(start_date: str) -> list[dict] | str:
    """주어진 날짜(YYYY-MM-DD) 이후에 작성된 모든 뉴스를 찾습니다."""
    print(f"도구 실행: search_since_date('{start_date}')")
    try:
        # 입력받은 문자열을 날짜 객체로 변환합니다.
        query_date = date.fromisoformat(start_date)
    except ValueError:
        return "❌ 오류: 날짜 형식이 잘못되었습니다. 'YYYY-MM-DD' 형식으로 입력해주세요."

    results = []
    for news in news_db:
        news_date = date.fromisoformat(news["date"])
        if news_date >= query_date:
            results.append(news)
            
    if not results:
        return f"'{start_date}' 이후에 작성된 뉴스를 찾을 수 없습니다."
    return results


# --- 서버 실행 ---
# fastmcp run news.py:mcp --transport sse --port 8083 --host localhost
if __name__ == "__main__":
    print("--- News Server - SSE ---")
    
    mcp.run(
        transport="sse",
        host="localhost",
        port=8083
    )