from langchain_redis import chat_message_history
import os

def get_chat_history(sessiion_id: str):
    return chat_message_history.RedisChatMessageHistory(
        session_id=sessiion_id,
        redis_url=os.getenv("REDIS_URL", "redis://localhost:6379")
    )
