import httpx
from fastapi import FastAPI, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .auth import verify_token, login

GOODS_SERVICE = "http://goods-service:8001"
ORDER_SERVICE = "http://order-service:8002"

ORDER_PREFIXES = ("/orders", "/admin/orders")

app = FastAPI(title="API Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginRequest(BaseModel):
    username: str
    password: str


@app.post("/auth/login")
def auth_login(data: LoginRequest):
    token = login(data.username, data.password)
    return {"access_token": token, "token_type": "bearer"}


def _target(path: str) -> str:
    if path.startswith(ORDER_PREFIXES):
        return ORDER_SERVICE
    return GOODS_SERVICE


async def _proxy(path: str, request: Request) -> Response:
    url = f"{_target('/' + path)}/{path}"
    params = dict(request.query_params)
    body = await request.body()
    headers = {
        k: v for k, v in request.headers.items()
        if k.lower() not in ("host", "content-length", "authorization")
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.request(
            method=request.method,
            url=url,
            params=params,
            content=body,
            headers=headers,
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )


@app.api_route("/admin/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy_admin(path: str, request: Request, _: str = Depends(verify_token)):
    return await _proxy(f"admin/{path}", request)


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy_public(path: str, request: Request):
    return await _proxy(path, request)