import sys
from pathlib import Path
import re
import logging
import pdb

root_path = Path(__file__).parent.parent
sys.path.append(str(root_path))
sys.path.append(str(root_path / 'LLM Chatbot'))

from NLU.main import config_nlu
from NLU.nlu import NLU
from Cart.cart import Cart
from llm_main import ChatbotAgent
from copy import deepcopy

from Database.database import Database
# LLM Chatbot
# from llm_main import ChatbotAgent

db: Database = Database()

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('APP')

special_words_yes = [
    "بله",
    "اره",
    "یس",
    "اوهوم"
]

special_words_no = [
    "خیر",
    "نخیر",
    "نه",
    "نو",
    "نمیکنم"
]

class ControlFlow:
    def __init__(self, user_id):
        self.nlu = NLU(config=config_nlu)
        self.user_id = user_id
        self.cart = Cart(customer_id=user_id)
        self.chatbot_agent = ChatbotAgent()
        self.intent_list = []
        self.flag_dict = {}
        self.conversation_mode = False
        
        self.multiple_buying_slots = []
        self.buying_slot = {}
        self.editing_slot = {}
        self.returning_slot = {}
        self.add_res = {}
        
        self.finishing_flag = False
        self.editing_flag = False
        self.flag_returning = False
        
        self.websocket_handler_list = []
        
    def produce_response(self, query):
        logger.warning('produce_response is called')
        if self.finishing_flag:
            logger.warning('finishing flag is called')
            response = self.instruction_tree(
                intention="finishing",
                slots={},
                query=query,
                secondary_intention=None
            )
            return response
        
        if self.flag_returning:
            logger.warning('returning flag is called')
            response = self.instruction_tree(
                intention="returning",
                slots={"order_id": self.returning_slot["order_id"]},
                query=query,
                secondary_intention=None
            )
            return response
        

        
        required_slots = self.get_required_slots()
        if required_slots != []:
            logger.warning('this query may be related to the previous query, required slots: %s, last intention: %s', required_slots, self.intent_list[-1])
            last_intention = self.intent_list[-1]
            query_detail = self.nlu.inference(query, predefined_intent=last_intention)
            slots = query_detail["slots"]

            if slots is not None and required_slots[0] in slots.keys():
                logger.warning('this query is related to the previous query, slots: %s', slots)
                self.intent_list.append(last_intention)
                response = self.instruction_tree(last_intention, slots, query)
                return response
            
        if len(self.multiple_buying_slots) != 0:
            logger.warning('multiple buying is called')
            response = self.instruction_tree(
                intention="buying",
                slots=self.multiple_buying_slots.pop(0),
                query=query,
                secondary_intention=None
            )
            return response

        logger.warning('this query is not related to the previous one')
        query_detail = self.nlu.inference(query)
        intention = query_detail["intent"]
        secondary_intention = query_detail["secondary_intent"]
        slots = query_detail["slots"]
        sentiment = query_detail["sentiment"]
        self.intent_list.append(intention)
        
        if sentiment == -1 and intention != "editting":
            logger.warning('sentiment changed the intention to customer-service')
            self.conversation_mode = True
            intention = "customer-service"
    
        response = self.instruction_tree(intention, slots, query, secondary_intention)
        return response
        
    def instruction_tree(self, intention, slots, query, secondary_intention=None):
        if self.conversation_mode:
            intention = "customer-service"
        logger.warning('instruction_tree is called with the (intent: %s, slots: %s)', intention, slots)

        if intention == "buying":
            logger.debug('buying intention is called')
            
            if "item" in slots.keys() and len(slots["item"].split(" ")) > 1:
                # ? Multiple Buying
                logging.warning("Multiple buying is here")
                items = slots["item"].split(" ")
                
                if "quantity" in slots.keys():
                    quantities = slots["quantity"].split(" ")
                else:
                    quantities = []
                    
                if "unit" in slots.keys():
                    units = slots["unit"].split(" ")
                else:
                    units = []
                
                if len(quantities) == 0:
                    logging.warning("q = 0, u = ?")
                    for i in items:
                        self.multiple_buying_slots.append(
                            {"item": i}
                        )
                elif len(quantities) == 1:
                    if len(units) == 0:
                        logging.warning("q = 1, u = 0")
                        for i in items:
                            self.multiple_buying_slots.append(
                                {"item": i, "quantity": slots["quantity"]}
                            )
                    elif len(units) == 1:
                        logging.warning("q = 1, u = 1")
                        for i in items:
                            self.multiple_buying_slots.append(
                                {"item": i, "quantity": slots["quantity"], "unit": slots["unit"]}
                            )
                    else:
                        if len(units) != len(items):
                            return self.http_response_returner({
                                    'status': 'message',
                                    'message': ["واحدهای وارد شده با تعداد کالا‌ها مطابقت ندارند."]
                                    })
                        
                        logging.warning("q = 1, u = n")
                        for i, u in zip(items, units):
                            self.multiple_buying_slots.append(
                                {"item": i, "unit": u}
                            )
                else:
                    if len(quantities) != len(items):
                        return self.http_response_returner({
                        'status': 'message',
                        'message': ["مقادیر وارد شده با تعداد کالا‌ها مطابقت ندارند."]
                        })
                        
                    if len(units) == 0:
                        logging.warning("q = n, u = 0")
                        for i, q in zip(items, quantities):
                            self.multiple_buying_slots.append(
                                {"item": i, "quantity": q}
                            )
                    elif len(units) == 1:
                        logging.warning("q = n, u = 1")
                        for i, q in zip(items, quantities):
                            self.multiple_buying_slots.append(
                                {"item": i, "quantity": q, "unit": slots["unit"]}
                            )
                    else:
                        if len(units) != len(items):
                            return self.http_response_returner({
                            'status': 'message',
                            'message': ["واحدهای وارد شده با تعداد کالا‌ها مطابقت ندارند."]
                            })
                        
                        logging.warning("q = n, u = n")
                        for i, q, u in zip(items, quantities, units):
                            self.multiple_buying_slots.append(
                                {"item": i, "quantity": q, "unit": u}
                            )
                
                results = []
                current_buying = deepcopy(self.multiple_buying_slots)
                # pdb.set_trace()
                for _ in current_buying:
                    results.append(self.produce_response(query))
                logging.warning(f"results = {results}")
                
                for d in results[1:]:
                    d["message"] = ""
                
                return {
                    "status": "multiple_cart",
                    "all_res": results
                }
                
            else:
                slots.update(self.buying_slot) # - History Added
                if len(slots) == 0:
                    logger.warning('we will ask for the buying list')
                    return self.http_response_returner({
                        'status': 'message',
                        'message': ['لطفا لیست خرید خود را برای من ارسال کنید.']
                    })
                elif "item" in slots.keys() and "quantity" not in slots.keys():
                    logger.warning('user did not specify quantity in its query')
                    unit = None
                    for i in self.cart.units_dict.keys():
                        if slots["item"] in self.cart.units_dict[i]:
                            unit = i
                            break

                    if unit == None:
                        logger.warning('database did not find the item')
                        return self.http_response_returner( {
                            'status': 'message',
                            'message': [f"{slots['item']} موجود نمی‌باشد"]
                        })
                        
                    logger.warning('we will ask for the quantity of the asked item')
                    self.flag_dict["quantity"] = 1
                    self.buying_slot = slots
                    return self.http_response_returner( {
                        'status': 'message',
                        'message': [f"چند {unit} {slots['item']} نیاز دارید؟"]
                    })
                elif "item" not in slots.keys() and "quantity" in slots.keys() and "unit" in slots.keys():
                    logger.warning('user did not specify item in its query')
                    logger.warning('we will ask for the item')
                    self.flag_dict["item"] = 1
                    self.buying_slot = slots
                    return self.http_response_returner( {
                        'status': 'message',
                        'message': [f"چه محصولی می‌خواهید؟"]
                    })
                    
                
                self.clear_temps()
                try:
                    if self.editing_flag:
                        logger.warning('editing flag is true, so this query is a editing query')
                        self.add_res = self.cart.add_to_cart(slots)
                        return self.instruction_tree(
                            intention="editting",
                            slots=self.editing_slot,
                            query="",
                            secondary_intention=None
                        ) 
                    else:
                        logger.warning('item successfuly added to the cart')
                        return self.http_response_returner(self.cart.add_to_cart(slots))
                except Exception as e:
                    logger.warning('error raised when attempting to add item into the cart')
                    return self.http_response_returner( {
                        "status": "message",
                        "message": [str(e)]
                    })
                
        elif intention == "editting":
            if len(slots) == 0:
                return self.http_response_returner( {
                    'status': 'message',
                    'message': ['لطفا تغییرات خود را به من اعلام کنید.']
                })
            if "replacement_item" in slots.keys() and "quantity" not in slots.keys():
                self.editing_flag = True
                self.editing_slot = {"item": slots["item"]}
                self.intent_list.append("buying")
                return self.instruction_tree(
                    intention="buying",
                    slots={"item": slots["replacement_item"]},
                    query=query,
                    secondary_intention=None)

            try:
                if len(self.add_res) != 0:
                    res = self.cart.edit_cart(slots)
                    res["content"] = self.add_res["content"]
                    self.clear_editing_temps()
                    return self.http_response_returner(res)
                
                self.clear_editing_temps()
                return self.http_response_returner(self.cart.edit_cart(slots))
            except Exception as e:
                return self.http_response_returner( {
                    "status": "message",
                    "message": [str(e)]  
                })
        
        elif intention == "finishing":
            
            if not self.finishing_flag:
                if self.cart.get_total_price() == 0:
                    return self.http_response_returner( {
                        "status": "message",
                        "message": ["سبد خرید شما خالی است."],
                    })
                    
                self.finishing_flag = True
                return self.http_response_returner( {
                    "status": "message",
                    "message": ["آیا سفارش خود را تایید می کنید؟"],
                })
            else:                
                if query in special_words_yes:
                    order_id = self.cart.finish_order()
                    self.finishing_flag = False
                    return self.http_response_returner( {
                        "status": "order_complete",
                        "message": [f"سفارش شما با موفقیت ثبت شد!", f"شماره پیگیری سفارش: {order_id}", "امیدوارم بازهم ازما خرید کنید!"],
                    })
                elif query in special_words_no:
                    self.finishing_flag = False
                    return self.http_response_returner( {
                        "status": "message",
                        "message": ["نهایی‌سازی سفارش با موفقیت لغو شد."]
                    })
                else:
                    self.finishing_flag = False
                    return self.produce_response(query)
        
        elif intention == "deleting":
            if slots is None or "order_id" not in slots.keys():
                self.flag_dict["order_id"] = 1
                return self.http_response_returner( {
                    'status': 'message',
                    'message': ["لطفا شماره سفارش خود را برای من ارسال کنید."]
                })
                
            self.clear_temps()
            
            try:
                order_id = int(slots["order_id"])
                return self.http_response_returner(self.cart.db.delete_order(
                    order_id=order_id,
                    customer_id=self.user_id
                ))
            except Exception as e:
                return self.http_response_returner( {
                    "status": "message",
                    "message": [str(e)]
                })
        
        elif intention == "returning":
            if slots is None or "order_id" not in slots.keys():
                self.flag_dict["order_id"] = 1
                return self.http_response_returner( {
                    'status': 'message',
                    'message': ["لطفا شماره سفارش خود را برای من ارسال کنید."]
                })
                
            self.clear_temps()
            try:
                order_id = int(slots["order_id"])
                return self.http_response_returner(self.cart.db.refund_order(
                    order_id=order_id
                ))
            except Exception as e:
                return self.http_response_returner( {
                    "status": "message",
                    "message": [str(e)]
                })
        
        elif intention == "tracking":
            if slots is None or "order_id" not in slots.keys():
                self.flag_dict["order_id"] = 1
                return self.http_response_returner( {
                    'status': 'message',
                    'message': ["لطفا شماره سفارش خود را برای من ارسال کنید."]
                })
                
            self.clear_temps()
            
            try:
                order_id = int(slots["order_id"])
                return self.http_response_returner(self.cart.db.order_tracking(
                    order_id=order_id,
                    customer_id=self.user_id
                ))
            except Exception as e:
                return self.http_response_returner( {
                    "status": "message",
                    "message": [str(e)]
                })
        
        elif intention == "inquiring" or intention == "chitchat":
            logger.warning('inquiring/chitchat intention is called')
            if slots is not None and "item" in slots.keys():
                context = self.cart.db.get_product_description(slots["item"])
                return self.http_response_returner(
                    {
                        'status': 'message',
                        'message': [intention, query, context]
                    },
                    type=False
                )
            else:
                if secondary_intention == "returning" or secondary_intention == "deleting" or secondary_intention == "discount": 
                    if secondary_intention == "discount":
                        secondary_intention = "tracking"
                    logger.warning('secondary intention matched. set order_id flag to 1')
                    self.intent_list.append(secondary_intention)
                    self.flag_dict["order_id"] = 1
                else:
                    logger.warning('secondary intention did not match.')
                return self.http_response_returner(
                    {
                        'status': 'message',
                        'message': [intention, query]
                    },
                    type=False
                )
        
        elif intention == "customer-service":
            logger.warning('customer-service intention is called')
            response = self.chatbot_agent.get_response(intention, query)
            if isinstance(response, str):
                self.conversation_mode = False
                if self.intent_list[-1] == "chitchat":
                    logger.warning('the conversation mode is off. this is the last query. with out of context query')
                    return self.http_response_returner(
                        {
                            "status": "message",
                            "message": [response]
                        }
                    )
                else:
                    logger.warning('the conversation mode is off. this is the last query. with continue query, secondary_intention: %s', secondary_intention)
                    return self.instruction_tree(
                        intention=self.intent_list[-1],
                        query=query,
                        slots=slots,
                        secondary_intention=secondary_intention
                    )
            if isinstance(response, tuple):
                self.conversation_mode = False
                order_id, reason = self.get_report_query_parameters(response[0])
                res, state = self.cart.db.save_report(order_id=order_id, report=reason)
                logger.warning('the conversation mode is off. this is the last query. returned: %s, state: %s', response[1], state)
                if response[1] == False or state == False:
                    logger.warning('the order should not be returned')
                    return self.http_response_returner(
                        {
                            "status": "message",
                            "message": [res]
                        }
                    )
                else:
                    logger.warning('the order should be returned')
                    self.flag_returning = True
                    self.returning_slot["order_id"] = order_id
                    return self.http_response_returner(
                        {
                            "status": "message",
                            "message": [res, "آیا میخواهید سفارش شما را عودت دهیم؟"]
                        }
                    ) 
                    
            logger.warning('the conversation mode is on. the queries are related to the privious ones')
            self.conversation_mode = True
            return self.http_response_returner(
                {
                    'status': 'message',
                    'message': [intention, query]
                },
                type=False
            )
                
    def get_required_slots(self):
        required_slots = []
        for slot in self.flag_dict:
            if self.flag_dict[slot] == 1:
                required_slots.append(slot)
        return required_slots
    
    def clear_temps(self):
        logger.warning('clear_temps is called')
        self.flag_dict = {}
        self.buying_slot = {}
        self.flag_returning = False
    
    def clear_editing_temps(self):
        logger.warning('clear_editing_temps is called')
        self.editing_flag = False
        self.editing_slot = {}
        self.add_res = {}
                    
    def http_response_returner(self, response, type=True):
        self.websocket_handler_list.append(
            (type, response["message"])
        )
        response["message"] = ["please open ws"]
        return response
    
    def streamer(self):
        number_of_events = len(self.websocket_handler_list)
        while number_of_events != 0:
            delay, msgs = self.websocket_handler_list.pop(0)
            number_of_messages = len(msgs)
            number_of_events -= 1
            if delay:   
                for msg in msgs:
                    number_of_messages -= 1
                    for chunck in msg.split(" "):
                        yield f"{chunck} ", delay
                    if number_of_messages != 0:
                        yield "$$$", True
                    db.save_chat(1, msg, author='ai')
            else:
                temp_msg = ""
                if number_of_messages == 3:
                    for chunk in self.chatbot_agent.get_response(msgs[0], msgs[1], context=msgs[2]):
                        try:
                            temp_msg += f"{chunk.content}"
                            yield f"{chunk.content}", delay
                        except:
                            temp_msg += f"{chunk}"
                            yield f"{chunk}", delay
                        
                elif number_of_messages == 2:
                    for chunk in self.chatbot_agent.get_response(msgs[0], msgs[1]):
                        try:
                            temp_msg += f"{chunk.content}"
                            yield f"{chunk.content}", delay
                        except:
                            temp_msg += f"{chunk}"
                            yield f"{chunk}", delay
                
                db.save_chat(1, temp_msg, author='ai')
                            
            if number_of_events != 0:
                yield "$$$", delay
                    

    def get_report_query_parameters(self, query: str):
        order_id_pattern = r'شماره سفارش\s*:\s*(?P<order_id>\d+)'
        reason_pattern = r'دلیل نارضایتی\s*:\s*(?P<reason>[\w\s\.]*)'
        try:
            order_id = re.search(order_id_pattern, query).group("order_id")
        except:
            order_id = None
        
        try:
            reason = re.search(reason_pattern, query).group("reason")
        except:
            reason = None
            
        return order_id, reason
    
if __name__ == "__main__":
    cf = ControlFlow(user_id=1)
    while True:
        user_input = input("You: ")
        output = cf.produce_response(user_input)
        print(f"Bot: {output}")
    