from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    VIRUS_TOTAL_API_Key = os.getenv("VIRUS_TOTAL_API_Key")
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    @property
    def virus_total_api_key(self) -> str:
        if self.VIRUS_TOTAL_API_Key is None:
            raise AttributeError("Переменная окружения VIRUS_TOTAL_API_Key не задана")
        return self.VIRUS_TOTAL_API_Key

    @property
    def tg_token(self) -> str:
        if self.TELEGRAM_TOKEN is None:
            raise AttributeError("Переменная окружения TELEGRAM_TOKEN не задана")
        return self.TELEGRAM_TOKEN

    @property
    def tg_chat_id(self) -> str:
        if self.TELEGRAM_CHAT_ID is None:
            raise AttributeError("Переменная окружения TELEGRAM_CHAT_ID не задана")
        return self.TELEGRAM_CHAT_ID
