import os

class Settings:
    GOOGLE_APPLICATION_CREDENTIALS: str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    project_root: str = "/app"                # root of /app in the container
    latex_service: str = "latex_compiler"  # Docker Compose service name

    class Config:
        env_file = ".env"

settings = Settings()
