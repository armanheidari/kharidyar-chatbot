from datetime import datetime
import pandas as pd
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from pathlib import Path
import sys


root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))

from Database.database import Database

db: Database = Database()

class Agent:
    def __init__(self, generative_model, retrieval_model):
        self.retrieval_model = retrieval_model
        self.generative_model = generative_model
        self.flag = False
        
    def build_memory(self, user_history: pd.DataFrame) -> ChatMessageHistory:
        chat_history = ChatMessageHistory()
        if user_history.empty:
            return chat_history
        
        user_history = user_history.sort_values('timestamp')
        user_history.apply(lambda row: self.memory_factory(row, chat_history), axis=1)
        return chat_history
    
    def memory_factory(self, row, chat_history: ChatMessageHistory):
        if row['author'] == 'human':
            chat_history.add_user_message(row['content'])
            
        elif row['author'] == 'ai':
            chat_history.add_ai_message(row['content'])
            
    def call(self, query, intention, user_id, context=None):
        ts_request = datetime.now().replace(microsecond=0)
        history_db = pd.read_csv(str(root_path / 'LLM Chatbot/chat_history.csv'))
        user_history = history_db[history_db['user_id'] == user_id]
        
        chat_history = self.build_memory(user_history=user_history)
        
        memory = ConversationBufferMemory(
            chat_memory=chat_history,
            memory_key='chat_history',
            input_key='user_input',
            return_messages=True
        )
        return self.generative_model.invoke(query, intention, context)
        
        # TODO: 
        # ts_response = datetime.now().replace(microsecond=0)

        # db.save_chat(user_id, query, 'human', ts_request)
        # db.save_chat(user_id, output, 'ai', ts_response)
        # new_memory = pd.DataFrame(
        #     {
        #         'timestamp': [ts_request, ts_response],
        #         'user_id': [user_id, user_id],
        #         'author': ['human', 'ai'],
        #         'content': [query, output]
        #     } 
        # )
        
        # history_db = pd.concat([history_db, new_memory]).reset_index(drop=True)
        # history_db.to_csv('chat_history.csv', index=False)
        
        # return output