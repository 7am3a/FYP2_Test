from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
from pydantic import field_validator


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Why this exists:
    - Centralizes all configuration in one place
    - Enables environment-specific configuration
    - Facilitates testing with different configurations
    - Supports deployment flexibility
    """
    
    # Application
    app_name: str = "SecureStego"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Security
    platform_secret_key: str = "dev_secret_key_replace_in_production"  # 64-character hex key for platform signature verification
    
    # Argon2id Parameters (OWASP recommended)
    argon2_time_cost: int = 3
    argon2_memory_cost: int = 65536  # 64 MB in KiB
    argon2_parallelism: int = 4
    argon2_hash_len: int = 32  # 256 bits for AES-256
    argon2_salt_len: int = 16  # 128 bits
    
    # API
    api_prefix: str = "/api"
    cors_origins: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # File Upload Limits
    max_file_size_mb: int = 100
    max_image_size_mb: int = 50
    max_video_size_mb: int = 500
    max_audio_size_mb: int = 100
    max_document_size_mb: int = 50
    
    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = None  # Optional: path to log file, None for stdout only
    
    # Storage
    temp_dir: Optional[str] = None  # Optional: custom temp directory, None for system default
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @field_validator('cors_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """
        Parse CORS origins from environment variable.
        
        Accepts either:
        - A list of strings (default value)
        - A comma-separated string from environment variable
        
        Parameters:
        v: The value to parse (list or string)
        
        Returns:
        List[str]: Parsed list of CORS origins
        """
        if isinstance(v, str):
            # Try JSON first, then fall back to comma-separated
            try:
                import json
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return parsed
            except (json.JSONDecodeError, ValueError):
                pass
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v
        # if isinstance(v, str):
        #     # Split by comma and strip whitespace
        #     return [origin.strip() for origin in v.split(",") if origin.strip()]
        # return v


settings = Settings()
