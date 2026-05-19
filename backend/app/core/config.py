from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Provider: "ollama", "google", "deepseek"
    LLM_PROVIDER: str = "ollama"
    
    # Ollama Config
    LLM_MODEL: str = "llama3.1"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    
    # Google Gemini Config
    GOOGLE_API_KEY: Optional[str] = "AIzaSyD0RzOuhnk72NZb0hPXqERlXzkNs3u-0PE"
    GEMINI_MODEL: str = "gemini-2.5-flash-lite"
    
    # DeepSeek Config (Standard OpenAI API compatible)
    DEEPSEEK_API_KEY: Optional[str] = None
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com"
    DEEPSEEK_MODEL: str = "deepseek-chat"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
