import uvicorn

from application.app import app_settings, init_app

app = init_app()

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=app_settings.SERVER_HOST,
        port=app_settings.SERVER_PORT,
        reload=app_settings.RELOAD,
        use_colors=app_settings.DEBUG,
    )
