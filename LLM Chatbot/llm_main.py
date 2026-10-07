from prompts import qa_prompt, chitchat_prompt, product_prompt, decide_enough_prompt, result_prompt, customer_service_prompt_2, decide_return_prompt, decide_context_prompt
from generative_model import GenerativeModel
from retrival_model import RetrievalModel
from chatbot import Agent
from pickle import load
from pathlib import Path
from typing import Generator


parent_path = Path(__file__).parent
root_path = parent_path.parent

class ChatbotAgent():
    def __init__(self, auto_create_engine: bool = True) -> None:
        self.flag = False
        self.load_chatbot_configuration()
        if auto_create_engine:
            self.create_agent()
    
    def load_chatbot_configuration(self):
        self.prompts = {
            "chitchat": chitchat_prompt,
            "rag": qa_prompt,
            "product": product_prompt,
            "customer-service": customer_service_prompt_2,
            "result": result_prompt,
            "decide_enough": decide_enough_prompt,
            "decide_return": decide_return_prompt,
            "decide_context": decide_context_prompt
        }

        self.retrieval_model = RetrievalModel(file_path=str(parent_path / "kharidyar-catalogue.txt"))
        self.retrieval_config = {
            "model_name": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            "chunk_overlap": 50, 
            "tokens_per_chunk": 128,
            "n_neighbors": 4,
            "metric": "cosine",
            "thresholds": 0.8
        }
        self.retrieval_model.compile(config=self.retrieval_config)
        self.retrieval_model.fit()

        self.generative_model = GenerativeModel()
        self.generative_config = {
            "model_name": "meta-llama/Llama-3-70b-chat-hf",
            "temperature": 0, 
            # "max_new_tokens": 250
        }
        self.generative_model.compile(
            retrieval_model=self.retrieval_model, 
            config=self.generative_config,
            prompts=self.prompts
        )

    def create_agent(self):
        self.agent = Agent(
            generative_model=self.generative_model, 
            retrieval_model=self.retrieval_model
        )
    
    def get_agent(self):
        if self.agent:
            return self.agent
        else:
            raise Exception('Agent doesn\'t create!')
    
    def get_response(self, intent: str, user_input: str, context: str = None):
        if self.agent:
            return self.generative_model.invoke(user_input, intent, context)
        else:
            raise Exception('Agent doesn\'t create!')
        

if __name__ == "__main__":
    chatbot = ChatbotAgent()
    chatbot.create_agent()
    while True:
        user_input = input('You: ')
        if user_input == 'exit':
            exit(0)
        else:
            for i in chatbot.get_response(user_input=user_input, intent="customer-service", ):
                try:
                    print(i.content, end="")
                except:
                    print(i, end="")
        print("\n")
