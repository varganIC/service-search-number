import os

from dotenv import load_dotenv

load_dotenv()


class SettingsBase:
    def __init__(self, prefix: str):
        self.host = os.getenv(f"{prefix}_HOST")
        self.port = int(os.getenv(f"{prefix}_PORT"))


class RedisSettings(SettingsBase):
    _prefix: str = "REDIS"

    def __init__(self):
        super().__init__(self._prefix)
        self.db = int(os.getenv(f"{self._prefix}_DB"))


class AppSettings(SettingsBase):
    _prefix: str = "APP"

    def __init__(self):
        super().__init__(self._prefix)


class Settings:
    def __init__(self):
        self.redis = RedisSettings()
        self.app = AppSettings()


settings = Settings()
