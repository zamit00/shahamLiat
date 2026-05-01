from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


class Settings(BaseSettings):
    url: str = Field(default="https://apmaccess.migdal.co.il/my.policy", alias="URL")
    username: str = Field(default="", alias="USERNAME")
    password: str = Field(default="", alias="PASSWORD")
    headless: bool = Field(default=False, alias="HEADLESS")
    downloads_dir: Path = Field(default=Path("downloads"), alias="DOWNLOADS_DIR")
    storage_dir: Path = Field(default=Path("storage"), alias="STORAGE_DIR")
    otp_wait_seconds: int = Field(default=180, alias="OTP_WAIT_SECONDS")

    model_config = SettingsConfigDict(extra="ignore")


settings = Settings()
