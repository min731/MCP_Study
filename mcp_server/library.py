# library.py
from fastmcp import FastMCP

book_db = [
    {"title": "파이썬으로 배우는 알고리즘", "author": "김알고", "year": 2022, "content": "알고리즘의 기초부터 심화까지 다루는 파이썬 입문서."},
    {"title": "FastMCP 완벽 가이드", "author": "박에이전트", "year": 2024, "content": "MCP 서버를 빠르고 쉽게 구축하는 방법을 설명합니다."},
    {"title": "인공지능 시대의 글쓰기", "author": "이작가", "year": 2023, "content": "AI와 협업하여 창의적인 글을 쓰는 노하우를 담았습니다."},
    {"title": "데이터베이스 첫걸음", "author": "김알고", "year": 2021, "content": "관계형 데이터베이스의 기본 원리를 쉽게 풀어쓴 책."},
    {"title": "클라우드 네이티브 패턴", "author": "박에이전트", "year": 2023, "content": "현대적인 클라우드 환경을 위한 아키텍처 패턴을 소개합니다."}
]

mcp = FastMCP(name="Library Server")

@mcp.tool()
def search_by_title(query: str) -> list[dict] | str:
    """책 제목에 검색어가 포함된 모든 도서를 찾습니다."""
    print(f"도구 실행: search_by_title('{query}')")
    # list comprehension을 사용하여 간결하게 검색 결과를 필터링합니다.
    results = [book for book in book_db if query.lower() in book["title"].lower()]
    
    if not results:
        return f"'{query}' 제목을 포함하는 책을 찾을 수 없습니다."
    return results

@mcp.tool()
def search_by_author(query: str) -> list[dict] | str:
    """주어진 저자가 쓴 모든 도서를 찾습니다."""
    print(f"도구 실행: search_by_author('{query}')")
    results = [book for book in book_db if query.lower() == book["author"].lower()]

    if not results:
        return f"'{query}' 저자의 책을 찾을 수 없습니다."
    return results

@mcp.tool()
def search_by_year(year: int) -> list[dict] | str:
    """주어진 연도에 출판된 모든 도서를 찾습니다."""
    print(f"도구 실행: search_by_year({year})")
    results = [book for book in book_db if year == book["year"]]
    
    if not results:
        return f"{year}년에 출판된 책을 찾을 수 없습니다."
    return results


# Server 실행
# fastmcp run library.py:mcp --transport sse --port 8082 --host localhost
if __name__ == "__main__":
    print("--- Library Server - SSE ---")

    mcp.run(
        transport="sse",
        host="localhost",
        port=8082
    )