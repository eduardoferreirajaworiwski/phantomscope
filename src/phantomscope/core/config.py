from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="PHANTOMSCOPE_", extra="ignore")

    env: str = "dev"
    log_level: str = "INFO"
    offline_mode: bool = True
    database_url: str = "sqlite:///./phantomscope.db"
    http_timeout: float = 10.0
    http_retries: int = 2
    user_agent: str = "PhantomScope/0.1 (+defensive-osint-demo)"
    crtsh_base_url: str = "https://crt.sh/"
    rdap_base_url: str = "https://rdap.org/domain/"
    openai_api_key: str | None = Field(default=None)
    openai_model: str = "gpt-4.1-mini"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

