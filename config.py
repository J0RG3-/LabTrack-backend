from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    PROJECT_NAME = "LabTrack"
    BACKEND_CORS_ORIGINS = os.getenv("CORS_ORIGINS", "").split(",")
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    SECRET_KEY = os.getenv("JWT_SECRET")

settings = Settings()
