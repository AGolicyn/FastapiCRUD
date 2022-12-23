from fastapi import APIRouter

from sql_app.api.ap1_v1.endpoints import item_api, user_api

api_router = APIRouter()
api_router.include_router(item_api.router)
api_router.include_router(user_api.router)