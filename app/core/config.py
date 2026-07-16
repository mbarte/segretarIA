from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str="segretarIA"
    app_version: str ="0.1.0"

    database_path: str
    
    ollama_host: str
    ollama_model: str
    ollama_keep_alive: str

    email_provider: str = "imap"
    imap_server: str
    imap_port: int = 993

    email_address: str

    class Config:
        env_file= ".env"

settings= Settings()