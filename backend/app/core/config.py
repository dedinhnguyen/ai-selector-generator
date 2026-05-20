from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Provider: "ollama", "google", "deepseek", "groq"
    LLM_PROVIDER: str = "groq"
    
    # Ollama Config
    LLM_MODEL: str = "llama3.1"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    
    # Google Gemini Config
    GOOGLE_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-2.5-flash-lite"

    # Grok Config (Standard OpenAI API compatible)
    GROK_API_KEY: Optional[str] = None
    GROK_BASE_URL: str = "https://api.x.com"
    GROK_MODEL: str = "grok-4.1-fast"

    # groq config
    GROQ_API_KEY: Optional[str] = None
    GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # DeepSeek Config (Standard OpenAI API compatible)
    DEEPSEEK_API_KEY: Optional[str] = None
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com"
    DEEPSEEK_MODEL: str = "deepseek-chat"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
