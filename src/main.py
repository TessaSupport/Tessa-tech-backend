from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from db.database import create_tables
from utils.config import settings
from authentication import token, auth
from admin import admin_route
from routers import user, ticket

app = FastAPI(
    title="Tessa Customer Support AI Agent API",
    description="This is a FastAPI Backend for the Tessa Application. All Rights Reserved.",
    debug=settings.DEBUG
)

app.include_router(token.router)
app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(user.router, prefix=settings.API_PREFIX)
app.include_router(ticket.router, prefix=settings.API_PREFIX)
app.include_router(admin_route.router, prefix=settings.API_PREFIX)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def health_check():
    return {
        'message': 'Welcome to the Tessa Customer Support AI Agent API',
        'status': 'healthy, API is running',
        'docs': '/docs',
        'redoc': '/redoc'
    }

create_tables()

if __name__ == "__main__":
    uvicorn.run(
        'main:app', 
        host='0.0.0.0', 
        port=8000, 
        reload=settings.ENV == "dev"
    )