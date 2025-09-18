# mcp_manager.py

import asyncio
from typing import List, Dict, Any, Optional, Tuple 
from fastapi import FastAPI, HTTPException, Query
from fastmcp import Client  # FastMCP 서버와 연결하기 위한 Client
from schemas.requests import CallToolRequest 

# -------------------------
# MCP 서버 URL 목록
# key: 서버 이름
# value: SSE URL
# -------------------------
SERVERS: Dict[str, str] = {
    "calculator": "http://localhost:8081/sse",
    "library": "http://localhost:8082/sse",
    "news": "http://localhost:8083/sse",
    "text_processor": "http://localhost:8084/sse",
}

app = FastAPI(title="MCP Server Manager API", version="1.0.0")

# =========================
# DEF: 서버 상태 확인
# =========================
async def _try_ping(base_url: str, timeout: float = 3.0) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    지정한 MCP 서버가 살아있는지 확인(ping)

    Parameters:
        base_url (str): MCP 서버 URL
        timeout (float): 연결 시 최대 대기 시간 (초)

    Returns:
        Tuple[alive, used_url, error]:
            alive: True/False
            used_url: 실제 연결에 사용한 URL, 실패 시 None
            error: 실패 시 예외 메시지, 성공 시 None
    """
    try:
        # Client를 사용해 서버에 비동기 연결
        async with Client(base_url, timeout=timeout) as client:
            await client.ping()  # 서버 응답 확인
            return True, base_url, None
    except Exception as e:
        # 연결 실패 시 False, URL 없음, 에러 메시지 반환
        return False, None, str(e)


# =========================
# DEF: 서버 도구 목록 조회
# =========================
async def _try_list_tools(base_url: str, timeout: float = 5.0) -> Tuple[Optional[Dict[str, str]], Optional[str], Optional[str]]:
    """
    MCP 서버가 제공하는 도구(tool) 목록 조회

    Parameters:
        base_url (str): MCP 서버 URL
        timeout (float): 연결 시 최대 대기 시간 (초)

    Returns:
        Tuple[tools_dict, used_url, error]:
            tools_dict: {tool_name: description} 형식, 실패 시 None
            used_url: 실제 연결 URL, 실패 시 None
            error: 실패 시 예외 메시지, 성공 시 None
    """
    try:
        # Client 연결
        async with Client(base_url, timeout=timeout) as client:

            # 서버에서 제공하는 모든 도구 목록 가져오기
            tools_raw = await client.list_tools()
            parsed: Dict[str, str] = {}

            for t in tools_raw:
                name = getattr(t, "name", None) or getattr(t, "tool_name", None) or str(t) # tool 함수명
                desc = getattr(t, "description", None) # tool 설명 """설명"""
                parsed[str(name)] = desc.strip() if isinstance(desc, str) and desc.strip() else ""

            # 정상 반환
            return parsed, base_url, None
    except Exception as e:
        # 실패 시 None, URL 없음, 예외 메시지 반환
        return None, None, str(e)


# =========================
# API: 서버 상태 확인
# =========================
@app.get("/status")
async def check_server_status(server_name: str = Query("calculator", description="서버 이름")):
    """
    지정 서버 상태 확인

    - server_name: calculator, library, news, text_processor 중 하나
    - 반환 예시: { "server": "calculator", "alive": True, "used_url": "...", "error": None }
    """
    if server_name not in SERVERS:
        raise HTTPException(status_code=404, detail=f"Unknown server '{server_name}'")

    ok, used_url, err = await _try_ping(SERVERS[server_name])
    return {"server": server_name, "alive": ok, "used_url": used_url, "error": err}


# =========================
# API: 특정 서버 도구 목록 조회
# =========================
@app.get("/tools")
async def get_server_tools(server_name: str = Query("library", description="서버 이름")):
    """
    지정 서버가 제공하는 도구 목록 조회
    - 반환: { "server": "...", "used_url": "...", "tools": {...} }
    """
    if server_name not in SERVERS:
        raise HTTPException(status_code=404, detail=f"Unknown server '{server_name}'")

    tools, used, err = await _try_list_tools(SERVERS[server_name])
    if tools is None:
        raise HTTPException(status_code=503, detail=f"도구 조회 실패: {err}")

    return {"server": server_name, "used_url": used, "tools": tools}


# =========================
# API: 여러 서버 도구 목록 조회 (batch)
# =========================
@app.get("/tools/batch")
async def get_multiple_server_tools(server_names: List[str] = Query(default=["calculator", "news"], description="서버 이름 목록")):
    """
    여러 서버를 병렬 조회하여 각 서버 도구 목록 반환
    """
    # 서버 이름 검증
    invalid = [s for s in server_names if s not in SERVERS]
    if invalid:
        raise HTTPException(status_code=400, detail=f"Unknown server(s): {invalid}")

    # worker: 각 서버별 도구 조회
    async def worker(name: str):
        tools, used, err = await _try_list_tools(SERVERS[name])
        return {"server": name, "ok": tools is not None, "used_url": used, "tools": tools, "error": err}

    # asyncio.gather로 병렬 처리
    results = await asyncio.gather(*[worker(n) for n in server_names])

    # 결과를 {server_name: {...}} 형식으로 반환
    return {
        "results": {
            r["server"]: {
                "ok": r["ok"],
                "used_url": r["used_url"],
                "tools": r["tools"],
                "error": r["error"]
            } for r in results
        }
    }


# -------------------------
# API: 특정 서버의 특정 tool 호출
# -------------------------
@app.post("/tools/call")
async def call_tool_endpoint(req: CallToolRequest):
    """
    특정 MCP 서버의 특정 도구(tool)를 호출합니다.

    Request body 예:
    {
      "server": "calculator",
      "tool": "add",
      "args": {"a": 2, "b": 3},
      "timeout": 5.0
    }

    {
    "server": "library",
    "tool": "search_by_year",
    "args": {"year":2023},
    "timeout": 5.0
    }

    {
    "server": "news",
    "tool": "search_by_category",
    "args": {"category": "IT"},
    "timeout": 5.0
    }

    동작:
    - server가 정의되어 있지 않으면 404 반환
    - Client에 연결하여 client.call_tool(tool, args) 실행
    - 결과 객체에서 가능한 필드(data, content)를 안전히 반환
    """
    server_name = req.server
    tool_name = req.tool
    args = req.args or {}
    timeout = req.timeout

    # 서버 이름 검증
    if server_name not in SERVERS:
        raise HTTPException(status_code=404, detail=f"Unknown server '{server_name}'")

    base_url = SERVERS[server_name]

    # Client 연결 및 tool 호출
    try:
        # timeout  전달
        client_kwargs = {"timeout": timeout} if timeout is not None else {}

        async with Client(base_url, **client_kwargs) as client:

            call_result = await client.call_tool(tool_name, args or {})
            result_payload = {}
            
            # fastmcp 버전에 따라 상이한 attr 처리
            if hasattr(call_result, "data"):
                try:
                    result_payload["data"] = call_result.data
                except Exception:
                    result_payload["data"] = None

            if hasattr(call_result, "content"):
                try:
                    result_payload["content"] = call_result.content
                except Exception:
                    result_payload["content"] = None

            raw_summary = repr(call_result) # repr는 디버깅용

            return {"ok": True, "server": server_name, "tool": tool_name, "result": result_payload, "raw": raw_summary}

    except Exception as e:
        # 호출 실패 503
        raise HTTPException(status_code=503, detail=f"Tool call failed: {e}")
    
# =========================
# 실행용 main
# uvicorn mcp_manager:app --host 0.0.0.0 --port 8080 --reload
# =========================
if __name__ == "__main__":
    import uvicorn
    print("Start MCP Server Manager API on http://localhost:8080")
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
