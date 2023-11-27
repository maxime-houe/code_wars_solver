import logging

from fastapi import FastAPI

from config import get_settings, get_browser, configure_log
from kata import kata_router
from user import user_router, login, logout

app = FastAPI(title=get_settings().project_name, version=get_settings().version)
app.include_router(kata_router)
app.include_router(user_router)


@app.on_event("startup")
async def startup():
    configure_log()
    logging.info("▶️ Starting up...")
    get_browser().maximize_window()
    await login()
    logging.info("✅ Startup OK")


@app.on_event("shutdown")
async def shutdown():
    logging.info("▶️ Shutdown...")
    await logout()
    get_browser().quit()
    logging.info("✅ Shutdown OK")


@app.get("/health", status_code=200)
async def health():
    return {"status": "ok"}
