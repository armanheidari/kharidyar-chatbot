from langchain.memory import ChatMessageHistory
from langchain_core.messages import AIMessage

class CustomizedChatMessageHistory(ChatMessageHistory):
    def add_message(self, message):
        if isinstance(message, AIMessage):
            message = AIMessage(content=message.content)
        super().add_message(message)
        

chat_history = CustomizedChatMessageHistory(
    memory_key="chat_history",
    max_len=50,
    return_messages=True
)