from langchain.schema.runnable import RunnablePassthrough
from history import chat_history, CustomizedChatMessageHistory
from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from langchain.output_parsers import BooleanOutputParser
from langchain_together import ChatTogether
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain_core.runnables.history import RunnableWithMessageHistory
import logging 

# create logger
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('LLM')


class GenerativeModel:
    def __init__(self):
        self.flag = False
        self.conversation_memory = chat_history
    
    def compile(self, retrieval_model, config, prompts):
        self.prompts = prompts
        self.retrieval_model = retrieval_model
        self.config = config                
        self.llm = ChatTogether(
            together_api_key="dd21adef0f6418983004927476d61aaf7119e253dce2d98e4754a91c02a15293",
            model=config["model_name"],
        )
        self.__build_chain()
                
    def invoke(self, query, intention, context):
        logger.warning("llm invoke is called with (intention: %s, context: %s)", intention, context)
        if intention == "inquiring" and context == None:
            logger.warning("non-context based inquiring intention is called")
            return self.stream_messages(self.rag_chain, query)
                
        elif intention == "inquiring" and context is not None:
            logger.warning("context based inquiring intention is called")
            product_chain = (
                {
                    "context": lambda x: context, 
                    "question": RunnablePassthrough()
                } 
                | self.prompts["rag"] 
                | self.llm
                | StrOutputParser()
            )
            return self.stream_messages(product_chain, query)

        elif intention == "chitchat":
            logger.warning("chitchat intention is called")
            return self.stream_messages(self.chithcat_chain, query)
                
        elif intention == "customer-service":
            context = self.decide_context_chain.invoke(query)
            if context == False:
                logger.warning("customer-service intention is called with the out of context")
                self.__build_history()
                return "چه کاری می‌توانم برای شما انجام دهم؟"
            branch = self.decide_enough_chain.invoke(query)
            logger.warning("customer-service intention is called with the branch: %s and the context: %s", branch, context)
            if branch == False:
                query_config = {"input": query}, {"configurable": {"session_id": "unsused"}}
                return self.stream_messages(self.history_chain, query_config)
            else:
                return_result = self.decide_return_chain.invoke(query)
                result = self.result_chain.invoke(query)
                self.__build_history()
                return (result, return_result)
        else:
            return 'WITHOUT ANY INTENTATION'
        
    def stream_messages(self, chain, query):
        logger.warning("streaming messages is called")
        if isinstance(query, tuple):
            for token in chain.stream(*query):
                yield token
        else:
            for token in chain.stream(query):
                yield token
    
    def __build_chain(self, initialize=False):
        logger.warning("build chain is called")
        self.rag_chain = (
            {
                "context": self.retrieval_model.invoke, 
                "question": RunnablePassthrough()
            } 
            | self.prompts["rag"] 
            | self.llm
            | StrOutputParser()
        )
        
        self.chithcat_chain = (
            {
                "question": RunnablePassthrough()
            } 
            | self.prompts["chitchat"]
            | self.llm
            | StrOutputParser()
        )
        
        self.decide_enough_chain = (
            {
                "chat_history" : lambda x: self.conversation_memory.messages, 
                "question": RunnablePassthrough()
            }
            | self.prompts["decide_enough"]
            | self.llm
            | BooleanOutputParser()
        )
        
        self.decide_return_chain = (
            {
                "chat_history" : lambda x: self.conversation_memory.messages, 
                "question": RunnablePassthrough()
            }
            | self.prompts["decide_return"]
            | self.llm
            | BooleanOutputParser()
        )
        
        self.decide_context_chain = (
            {
                "chat_history" : lambda x: self.conversation_memory.messages, 
                "question": RunnablePassthrough()
            }
            | self.prompts["decide_context"]
            | self.llm
            | BooleanOutputParser()
        )

        self.result_chain = (
            {
                "chat_history": lambda x: self.conversation_memory.messages, 
                "question": RunnablePassthrough()
            }
            | self.prompts["result"]
            | self.llm
            | StrOutputParser() 
        )
        
        self.history_chain = RunnableWithMessageHistory(
            self.prompts["customer-service"] | self.llm,
            lambda session_id: self.conversation_memory,
            input_messages_key="input",
            history_messages_key="chat_history",
        )
        
    def __build_history(self):
        logger.warning("build history is called")
        self.conversation_memory = CustomizedChatMessageHistory(
            memory_key="chat_history",
            max_len=50,
            return_messages=True
        )