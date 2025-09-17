# calculator_mcp.py
from fastmcp import FastMCP

mcp = FastMCP(name="Calculator MCP Server")

# tool 정의
@mcp.tool()
def add(a: int, b: int) -> int:
    """두 개의 정수를 더합니다."""
    print(f"도구 실행: add({a}, {b})")
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """두 번째 정수를 첫 번째 정수에서 뺍니다."""
    print(f"도구 실행: subtract({a}, {b})")
    return a - b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """두 개의 정수를 곱합니다."""
    print(f"도구 실행: multiply({a}, {b})")
    return a * b

@mcp.tool()
def divide(a: int, b: int) -> float | str:
    """첫 번째 정수를 두 번째 정수로 나눕니다. 0으로 나눌 경우 오류 메시지를 반환합니다."""
    print(f"도구 실행: divide({a}, {b})")
    if b == 0:
        return "오류: 0으로 나눌 수 없습니다."
    return a / b

# resource 정의
@mcp.resource("data://gugudan")
def get_gugudan() -> dict:
    """2단부터 9단까지의 구구단 데이터를 JSON(dict) 형태로 제공합니다."""
    print("리소스 요청: data://gugudan")
    gugudan_data = {}
    for i in range(2, 10):  # 2단부터 9단까지
        dan = f"{i}단"
        gugudan_data[dan] = [f"{i} x {j} = {i*j}" for j in range(1, 10)]
    return gugudan_data


# Server 실행
# fastmcp run calculator.py:mcp --transport sse --port 8081 --host localhost
if __name__ == "__main__":
    print("--- Calculator MCP Server - SSE ---")

    mcp.run(
        transport="sse",
        host="localhost",
        port=8081
    )