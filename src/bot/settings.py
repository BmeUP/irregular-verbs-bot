from pydantic import BaseSettings


class BotSettings(BaseSettings):
    bot_token: str = ""


settings = BotSettings()
print("=========================")
print(settings.bot_token)