from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, SecretStr


class BoundingBox(BaseModel):
  lamin: float 
  lomin: float
  lamax: float 
  lomax: float

class Config(BaseSettings):
  opensky_base_url: str
  opensky_client_id: str
  opensky_client_secret: SecretStr
  proxy_url: str
  bbox: BoundingBox
  poll_interval_seconds: int = 20
  kafka_bootstrap_servers: str
  kafka_partitions: int = 8
  kafka_topic: str
  max_retries: int = 3
  base_backoff_seconds: int = 15 
  request_timeout_seconds: int = 30


  model_config = SettingsConfigDict(
    env_file=".env", 
    env_file_encoding="utf-8",
    env_nested_delimiter="__",
    extra="ignore"          # Ignores extra variables in .env without breaking
  )


settings = Config()