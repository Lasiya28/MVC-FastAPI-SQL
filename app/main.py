from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .controllers import auth, post

"""Create database tables"""
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI MVC Back End Design")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""Add middleware to check request body size"""


@app.middleware("http")
async def check_request_body_size(request: Request, call_next):
    # Only check POST requests
    if request.method == "POST" and request.url.path == "/posts":
        try:
            # Get request body
            body = await request.body()
            # Check if body size exceeds 1 MB
            if len(body) > 1048576:  # 1 MB in bytes
                return Response(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    content={
                        "detail": "Request body too large, maximum allowed size is 1 MB"},
                )
        except Exception:
            pass
    response = await call_next(request)
    return response

# Include routers
app.include_router(auth.router)
app.include_router(post.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI/MySQL MVC based backend. Go to http://127.0.0.1:8000/docs for Swagger"}
