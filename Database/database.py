import mysql.connector
import json
import re
import os
from typing import Any, Dict
from pathlib import Path
from datetime import datetime


class SingletonMeta(type):
    
    _instances = {}
    
    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
        

class Database(metaclass=SingletonMeta):
    def __init__(self, host: str = "localhost", user: str = "root", password: str = "12345678", database: str = "kharidyar", port: str = "24000") -> None:
        
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        
        self.cursor = self.connection.cursor()
        self.units_dict = None
        
    def reconnect(self) -> None:
        try:
            self.connection.reconnect()
        except Exception as e:
            raise Exception(
                f"Connection Error! - detail: {e}"
            )
            
    def get_units(self) -> Dict:
        if self.units_dict == None:
            query = f'''
                SELECT name, unit
                FROM product_unit pu
                JOIN products p ON p.product_id = pu.product_id;
            '''
            
            self.cursor.execute(query)
            res = self.cursor.fetchall()
            units_dict = {}
            for product, units in res:
                for u in units.split("|"):
                    try:
                        units_dict[u].add(product)
                    except:
                        units_dict[u] = {product}
            
            self.units_dict = units_dict
        
        return self.units_dict
    
    def check_inventory(self, item: str, quantity: int) -> bool:
        query = f'''
            SELECT name
            FROM inventory i
            JOIN products p ON p.product_id = i.product_id
            WHERE name = '{item}' AND
            count >= {quantity};
        '''
        
        self.cursor.execute(query)
        res = self.cursor.fetchone()
        return (False if res == None else True)
    
    def check_order_id(self, customer_id, order_id):
        query = f'''
            SELECT *
            FROM orders
            WHERE order_id = '{order_id}' and customer_id = '{customer_id}';
            '''
        self.cursor.execute(query)
        res = self.cursor.fetchone()
        
        if res == None:
            raise ValueError("شما همچین سفارشی ثبت نکرده اید!")
    
    def order_tracking(self, customer_id, order_id): 
        self.check_order_id(customer_id, order_id)
        
        query = f'''
            SELECT status
            FROM orders
            WHERE order_id = '{order_id}';
            '''
        self.cursor.execute(query)
        result = self.cursor.fetchone()[0]
        
        res = "وضعیت سفارش شما مشخص نشده است. لطفا با پشتیبانی تماس بگیرید."
        if result == "progress":
            res = "سفارش شما در حال بررسی می باشد. لطفا شکیبا باشید." 
        elif result == "delivered":
            res = "سفارش شما از طرف ما ارسال شده است."
        elif result == "completed":
            res = "سفارش شما تحویل داده شده است. چنانچه مشکلی دارید و یا سفارش را تحویل نگرفته اید با کارشناس پشتیبانی تماس بگیرید."
        elif result == "returned":
            res = "سفارش شما مرجوع شده است."
        
        return {
                "status": "message",
                "message": [res]
            }
    
    def cancel_refunding(self, customer_id, order_id):
        self.check_order_id(customer_id, order_id)
    
        query = f'''
            SELECT updated_time
            FROM orders
            WHERE status = 'returned';
            '''
        self.cursor.execute(query)
        res = self.cursor.fetchone()
        
        if res == None:
            raise ValueError("سفارش شما در وضعیت مرجوعی نیست.")
        
        time_left = (datetime.now() - res[0]).seconds
        if time_left <= 4 * 3600:
            query = f'''
                UPDATE orders
                SET `status` = "progress"
                WHERE order_id = '{order_id}'
            '''
            self.cursor.execute(query)
            self.connection.commit()
            
            return {
                "status": "message",
                "message": ["درخواست مرجوعی شما لغو شد."]
            }
        
        else:
            return {
                "status": "message",
                "message": ["نمی توانیم سفارش شما را لغو کنیم."]
            }
    
    def refund_order(self, order_id):
        query = f'''
            SELECT customer_id, status
            FROM orders o
            WHERE order_id = {order_id};
        '''
        
        self.cursor.execute(query)
        res = self.cursor.fetchone()
        if res is None:
            raise Exception('سفارش مورد نظر موجود نمی باشد.')
        else:
            if res[1] != 'completed':
                raise Exception('سفارش شما هنوز در مرحله پردازش می باشد و درخواست مرجوعی در حال حاضر موجود نمی باشد.')
            else:
                self.cursor.reset()
                query = f'''
                    UPDATE orders o
                    SET updated_time = '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}',
                        status = 'returned'
                    WHERE order_id = {order_id};
                '''
                self.cursor.execute(query)
                self.connection.commit()
                self.cursor.reset()
                
                return {
                    "status": "message",
                    "message": ['درخواست مرجوعی شما با موفقیت انجام شد.']
                }
    
    def get_product_description(self, name: str):
        query = f'''
            SELECT description, count, price
            FROM products p
                LEFT JOIN products_description pd on p.product_id = pd.product_id
                LEFT JOIN inventory i on p.product_id = i.product_id
            WHERE name='{name}';
        '''

        self.cursor.execute(query)
        res = self.cursor.fetchone()
        
        if res is None:
            return "کالای مورد نظر موجود نمی‌باشد."
        else:
            return f"توضیحات: {res[0]} . موجودی: {res[1]} . قیمت واحد: {res[2]}"
            
    def get_all_prices(self) -> Dict:
        query = '''
            SELECT name, price
            FROM products
        '''
        
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        
        prices = {
            x[0]:float(re.search(r'\d+\.\d{2}', str(x[1]))[0]) for x in res
        }
        
        return prices
    
    def add_cart_to_database(self, path: Path, customer_id: int, total_price: float) -> int:
        try:
            with open(path, mode="r", encoding="UTF-8") as f:
                cart = json.load(f)
        except:
            raise Exception(
                "سبد خرید مورد نظر موجود نمی‌باشد."
            )
        if len(cart) == 0:
            raise Exception(
                "سبد خرید شما خالی است."
            )
        
        data = []
        
        for order in cart:
            query = f'''
                SELECT product_id
                FROM products
                WHERE name='{order[1]}';
            '''
            
            self.cursor.execute(query)
            res = self.cursor.fetchone()
            self.cursor.reset()
            
            data.append([res[0], order[0]])
        
        query = f'''
            INSERT INTO orders (customer_id, total_price, status)
            VALUES ('{customer_id}', {total_price}, 'progress');
        '''
        
        self.cursor.execute(query)
        o_id = self.cursor._last_insert_id
        
        for item in data:
            query = f'''
                INSERT INTO order_products (order_id, product_id, amount)
                VALUES ({o_id}, {item[0]}, {item[1]});
            '''
            self.cursor.execute(query)
            self.cursor.reset()
            query = f'''
                UPDATE inventory i
                SET count = count - {item[1]}
                WHERE product_id = {item[0]};
            '''
            self.cursor.execute(query)
        
        os.remove(path)
        self.connection.commit()
        self.cursor.reset()
        
        return o_id
    
    def delete_order(self, order_id, customer_id):
        query = f'''
            SELECT order_id, customer_id, total_price, status, updated_time
            FROM orders o
            WHERE order_id = {order_id};
        '''
        self.cursor.execute(query)
        res = self.cursor.fetchone()
        if res is None:
            raise Exception('سفارش مورد نظر موجود نمی باشد.')
        elif (datetime.now() - res[-1]).seconds >= 28800:
            raise Exception('بیشتر از 8 ساعت از زمان ثبت سفارش شما گذشته است و نمی توانید آن را حذف کنید.')
        elif res[1] != customer_id:
            raise Exception('این سفارش متعلق به شما نمی باشد.')
        elif res[3] == 'delivered':
            raise Exception('سفارش شما از مرکز ارسال خارج شده است و نمی توانید آن را حذف کنید. چنانچه هنوز هم تمایل به حذف سفارش خود دارید می توانید بعد از دریافت سفارش، طبق قوانین مرجوعی سفارشات، آن را برگردانید. با تشکر.')
        elif res[3] == 'completed':
            raise Exception('این سفارش تحویل مشتری داده شده است و نمی توانید آن را حذف کنید.')
        else:
            self.cursor.reset()
            query = f'''
                CALL delete_products_for_order({order_id});
            '''
            self.cursor.execute(query)
            self.cursor.reset()
            
            query = f'''
                DELETE FROM orders
                WHERE order_id = 13;
            '''
            self.cursor.execute(query)
            self.cursor.reset()
            
            return {
                "status": "message",
                "message": ['سفارش شما با موفقیت حذف شد.']
            }
        
    def get_chat_history(self, customer_id: int, chat_id: int = None):
        query = f'''
            SELECT author, input_text, input_timestamp, metadata 
            FROM chat_history ch
            WHERE ch.user_id = {customer_id}
        '''
        if chat_id:
            query += f'''
                AND ch.chat_id = {chat_id}
            '''

        query += f''';'''
        
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        self.cursor.reset()

        return res

    def save_chat(self, customer_id: int, input: str, author: str, timestamp: datetime=None):
        query = f'''
            INSERT INTO chat_history(chat_id, user_id, author, input_text, input_timestamp)
            VALUES (
                1,
                {customer_id},
                "{author}",
                "{input}",
                STR_TO_DATE("{timestamp if timestamp else datetime.now().strftime("%Y-%m-%d %H:%M:%S")}", "%Y-%m-%d %H:%i:%S")
            )
        '''
        self.cursor.execute(query)
        self.connection.commit()
        self.cursor.reset()

    def save_report(self, order_id: int, report: str, user_id: int = 1):
        order_id = int(order_id)
        try:
            query = f'''
                INSERT INTO report (user_id, order_id, report)
                VALUES ({user_id}, {order_id}, '{report}');
            '''
            self.cursor.execute(query)
            self.connection.commit()
            res = "فروشگاه خریدیار از مشکل پیش آمده برای شما کاربر گرامی بسیار متاسف است. گزارش شما ثبت شد و به زودی کارشناسان ما با شما تماس خواهند گرفت.", True
        except mysql.connector.errors.IntegrityError as e:
            print(e)
            self.connection.rollback()
            res = "این سفارش برای شما ثبت نشده است و یا متعلق به شما نیست!", False
        except Exception as e:
            print(e)
            res = "متاسفانه مشکلی در سرور پیش آمده است و نمی توانیم پاسخ گوی شما باشیم. به زودی مشکل پیش آمده را حل خواهیم کرد. از صبر و شکیبایی شما سپاسگزاریم.", True
        finally:
            self.cursor.reset()

        return res

if __name__ == '__main__':
    db: Database = Database()
    
    # print(db.get_product_description("مرغ"))

    # db.save_chat(customer_id=1, input="fff", author="ai")

    # db.save_report(10, "ستایتاسستایتتسایستاتس")

    # db.cancel_refunding(1, 1)
    
    # try:
    #     db.get_all_prices()
    # except Exception as e:
    #     print(e)
    
    # try:
    #     db.check_order_id(1, 12)
    # except Exception as e:
    #     print(e)
    
    # try:
    #     db.check_order_id(1, 10)
    # except Exception as e:
    #     print(e)

    # try:
    #     db.order_tracking(1, 12)
    # except Exception as e:
    #     print(e)
    
    # try:
    #     db.get_product_description('دلستر')
    # except Exception as e:
    #     print(e)

    # try:
    #     db.get_product_description('موز')
    # except Exception as e:
    #     print(e)

    # try:
    #     db.order_tracking(10, 1)
    # except Exception as e:
    #     print(e)

    # try:
    #     db.cancel_refunding(1, 1)
    # except Exception as e:
    #     print(e)
