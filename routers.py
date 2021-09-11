from fastapi import APIRouter
from home_application.api import router as home_router


router = APIRouter()

router.include_router(home_router,prefix='/api')
