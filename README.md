# MCP Server 개발

## Framework 

FastMCP vs MCP Python SDK

![alt text](image.png)

출처: [https://wikidocs.net/287360](https://wikidocs.net/287360)

## Protocol

(1) STDIO

서버와 클라이언트가 같은 시스템 내에서 표준 입출력 파이프(STDIO)를 통해 통신합니다. Claude Desktop, 로컬 도구, 로컬 테스트 환경 등에 적합합니다.

```python
from fastmcp import FastMCP

mcp = FastMCP()

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

(2) Streamable HTTP

HTTP 프로토콜을 기반으로 MCP 서버를 실행하는 방식입니다. 웹 기반 배포에 가장 적합하며, 공식 문서에서도 사용을 권장합니다.

```python
from fastmcp import FastMCP

mcp = FastMCP()

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

(3) SSE

SSE(Server-Sent Events)는 HTTP 기반의 스트리밍 프로토콜로, 서버가 클라이언트로 데이터를 지속적으로 전송할 수 있도록 설계되었습니다.

```python
from fastmcp import FastMCP

mcp = FastMCP()

if __name__ == "__main__":
    mcp.run(transport="sse")
```
