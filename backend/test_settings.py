from pydantic_settings import BaseSettings, SettingsConfigDict


class TestSettings(BaseSettings):
    app_name: str

    model_config = SettingsConfigDict(
        env_file=".env.development",
        env_file_encoding="utf-8",
    )


settings = TestSettings()

print(settings.app_name)