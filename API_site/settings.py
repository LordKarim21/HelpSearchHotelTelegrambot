import os

from dotenv import load_dotenv
from pydantic import BaseSettings, SecretStr, StrictStr

load_dotenv()


class SiteSettings(BaseSettings):
    app_key: SecretStr = os.getenv("SITE_API", None)
    host_key: StrictStr = os.getenv("HOST_API", None)
