from pathlib import Path
from typing import Dict
import json
import sys

sys.path.append(str(Path(__file__).parent.parent))
from Database.database import Database


# ## HELPER FUNCTIONS ##
# P22_map = {'۱' : '1', '۲' : '2', '۳' : '3', '۴' : '4', '۵' : '5', '۶' : '6', '۷' : '7', '۸' : '8', '۹' : '9', '۰' : '0' }

# # تبدیل اعداد انگلیسی به فارسی در رشته ورودی
# def convert_number_to_english(strIn : str):
#     ans = ""
#     for ch in strIn:
#         if ch in P22_map:
#             ans += P22_map[ch]  
#         else:
#             raise ValueError("عدد وارد شده صحیح نمی‌باشد.")
#     return ans

charachters_to_numbers = {
    "یک": 1, "دو": 2, "سه": 3, "چهار": 4, "پنج": 5, "شیش": 6, "هفت": 7, "هشت": 8, "نه": 9, "ده": 10
}

class Cart:
    def __init__(self, customer_id: int, path: str = None) -> None:
        self.customer_id = customer_id
        
        if path == None:
            self.path = Path(__file__).parent.parent / "Temp" / f"Cart_{self.customer_id}.json"
        else:
            self.path = Path(path) / "Temp" / f"Cart_{self.customer_id}.json"
            
        self.db : Database = Database()
        self.units_dict = self.db.get_units()
        self.prices_dict = self.db.get_all_prices()
        self.discount = 0.0
        self.total_price = 0.0
        
    def set_discount(self, discount: float) -> None:
        self.discount = discount
        
    def get_total_price(self) -> float:
        return self.total_price
            
    def add_to_cart(self, info: Dict) -> Dict:
        
        def key_check(key, error_key):
            try:
                return info[key]
            except:
                raise KeyError(
                    f"{error_key} مورد نظر مشخص نشده است."
                )
        
        item = key_check("item", "کالای")
        quantity = key_check("quantity", "تعداد")
        if quantity in charachters_to_numbers.keys():
            quantity = charachters_to_numbers[quantity]
        else:
            try:
                quantity = int(quantity)
            except:
                ValueError(f"عدد وارد شده برای {info['item']} صحیح نمی‌باشد.")
        
        if list(filter(lambda x: item in x, self.units_dict.values())) == []:
            raise ValueError(f"{info['item']} موجود نمی‌باشد")
        
        
        try:
            # - Unit Provided
            unit = info["unit"]
            
            try:
                compatible_products = self.units_dict[unit]
            except:
                raise ValueError(f"واحد داده شده برای {item} معتبر نمی‌باشد")

            if item not in compatible_products:
                raise ValueError(f"عدم مطابقت واحد ({unit}) و کالا ({item})")
        
        except ValueError as e:
            raise e    
        
        except KeyError:
            # - No Units
            for i in self.units_dict.keys():
                if item in self.units_dict[i]:
                    unit = i
                    break
            pass
        
        cumulative_cart = self.read_cumulative_cart()
        try:
            previous_quantity = cumulative_cart[item]
        except:
            previous_quantity = 0
        
        if not self.db.check_inventory(item, previous_quantity + quantity):
            raise ValueError(
                f"{item} به تعداد کافی موجود نمی‌باشد."
            )
        
        with open(self.path, mode="a+", encoding="UTF-8") as f:
            f.seek(0)
            try:
                cart = json.load(f)
            except:
                cart = []
            f.seek(0)
            f.truncate()
            json.dump(
                cart + [[quantity, item]], f, ensure_ascii=False, indent=4
            )
        
        self.total_price += (quantity * self.prices_dict[item]) * (1 - self.discount) 
            
        return {
            "status": "cart",
            "message": [f"{item} به سبد خرید اضافه شد."],
            "content": [[quantity, unit, item]],
            "current_price": self.total_price
        }
    
    def remove_from_cart(self, item: str) -> int:
        try:
            with open(self.path, mode="r", encoding="UTF-8") as f:
                cart_json = json.load(f)
        except:
            raise Exception(
                "سبد خرید شما خالی است."
            )
        if len(cart_json) == 0:    
            raise Exception(
                "سبد خرید شما خالی است."
            )
            
        index = 0
        removed = False
        for i in range(len(cart_json)):
            if item == cart_json[i][1]:
                self.total_price -= (int(cart_json[i][0]) * self.prices_dict[item]) * (1 - self.discount) 
                cart_json.__delitem__(i)
                index = i
                removed = True
                break
        
        if removed == False:
            raise Exception(
                "شما همچین کالایی برای تغییر ندارید."
            )
        
        with open(self.path, 'w', encoding='UTF-8') as f:
            json.dump(cart_json, f, ensure_ascii=False, indent=4)
        
        return index
    
    def edit_cart(self, info: Dict) -> Dict:
        replace, change = False, False
        
        index = self.remove_from_cart(info["item"])
        
        try:
            # - Replace Item
            rep_item = info["replacement_item"]
            replace = True
            
        except:
            # - Change Quantity
            try:
                _ = info["new_quantity"]
                change = True
            except:
                pass
                
        res_dict = {"content": ""}
        if replace:
            res_dict = self.add_to_cart({"item": rep_item, "quantity": info["quantity"]})
        elif change:
            res_dict = self.add_to_cart({"item": info["item"], "quantity": info["new_quantity"]})
            
        return {
            "status": "edit_cart",
            "message": ["تغییرات با موفقیت اعمال شد.", "لطفا ادامه لیست خرید خود را وارد کنید."],
            "content": res_dict["content"],
            "deleted": index,
            "current_price": self.total_price
        }
        
    def read_cumulative_cart(self) -> Dict: 
        with open(self.path, mode="r", encoding="UTF-8") as f:
            cart_json = json.load(f)

        cumulative_cart = {}
        for quantity, item in cart_json:
            try:
                cumulative_cart[item] += quantity
            except:
                cumulative_cart[item] = quantity
        
        return cumulative_cart
        
    def finish_order(self):
        return self.db.add_cart_to_database(self.path, self.customer_id, self.total_price)
    
if __name__ == "__main__":
    
    test_cart = Cart(customer_id=1002)
    
    try:
        test_cart.add_to_cart(
            {
                "item": "مرغ",
                "quantity": "5",
                "unit": "کیلو"
            }
        )
        test_cart.add_to_cart(
            {
                "item": "سیب",
                "quantity": "5",
                "unit": "کیلو"
            }
        )
        test_cart.remove_from_cart("مرغ")
        print(test_cart.finish_order())
    except Exception as e:
        print(e)