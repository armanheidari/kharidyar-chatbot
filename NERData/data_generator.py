import numpy as np
import pandas as pd
from typing import List, Dict
import random

items = ['سیب', 'پرتقال', 'شیر', 'نان', 'تخم مرغ', 'پنیر', 'مرغ', 'گوشت', 'ماهی', 'برنج', 'پاستا', 'کاهو', 'سیب زمینی', 'خیار', 'هویج', 'گوجه فرنگی', 'پیاز', 'سیر', 'روغن زیتون', 'کره', "آبمیوه"]

units = ['کیلوگرم', 'لیتر', 'عدد', 'شانه', 'بطری' ]

days = ["شنبه", "یک شنبه", "دوشنبه", "سه شنبه", "چهارشنبه", "پنج شنبه", "جمعه"]

events = ["سال نو", "تعطیلات تابستانی", "عید", "کریسمس", "هالووین", "تخفیفات زمستانی"]

returning_reasons = [
    "کیفیت بسیار پایین کالاهای ارسالی", 
    "تاریخ مصرف محصولات گذشته بود", "نظرم عوض شد", 
    "دوست نداشتم این محصول رو", 
    "جنس هایی فرستادید خراب بودند", 
    "بسته بندی ارسال بسیار بد بود", 
    "کالاها رو اشتباهی ارسال کردید", 
    "محصولات ارسالی با سفارشی که داشتم مغایرت داره", 
    "محصولات قدیمی و خراب و داغون هستند", 
    "از خریدم پشیمون شدم",
    "اشتباه خرید کردم",
    "تاریخ مصرف کالای ارسالی گذشته است",
    "کالاها آسیب دیده به دست بنده رسیده است"
]

returning_verbs = [
    "بازگردانم",
    "مرجوع کنم",
    "برگشت بزنم",
    "برگردونم",
    "پس بدهم",
    "برگردانم",
    "عودت بدهم",
    "تعویض کنم",
    "پس بفرستم",
    "مرجوعی ثبت کنم"
]

returning_nouns = [
    "مرجوع",
    "برگشت",
    "عودت",
    "تعویض",
    "عوض"
]

conditions = [
    "رژیمی بودن و مخصوص ورزشکاران",
    "طبیعی بودن و بدون داشتن مواد شیمیایی",
    "چربی 0 درصد داشتن",
    "افراد دیابیتی",
    "کاهش وزن و تناسب اندام",
    "نداشتن مواد مضر غیر طبیعی"
]

seasons = ["بهار", "پاییز", "تابستان", "زمستان"]

certifications = ["BRC", "SQF", "FSSC", "IFS"]

deleting_reasons = [
    "به دردم نمیخوره",
    "اشتباه ثبت کردم",
    "جای دیگری قیمت بهتری پیدا کردم",
    "اندازه اشتباهی انتخاب کردم",
    "دیگر به آن احتیاجی ندارم",
    "آدرس اشتباهی وارد کردم",
    "تغییرات برنامه‌ریزی داشتم",
    "پشیمان شدن از خرید",
    "محصول مورد نظر را در جای دیگری یافتم",
    "موجودی مالی به اندازه کافی ندارم",
    "توانایی مالی به اندازه کافی ندارم",
    "از مکان دیگری میخواهم خرید کنم"
]

deleting_verbs = [
    "لغو کنم",
    "حذف کنم",
    "کنسل کنم",
    "دیلیت کنم",
    "پاک کنم",
    "خط بزنم"
]

deleting_nouns = [
    "لغو",
    "حذف",
    "دیلیت",
    "کنسل",
    "پاک"
]

templates = [
    "من برای کباب کردن نیاز به {quantity} {unit} از {item} دارم .",
    "می‌توانم {quantity} {unit} از {item} را برای خرید هفتگی‌ام رزرو کنم ؟",
    "شب مهمونی داریم {item} میخواستم .",
    "میشه برام {quantity} {unit} {item} ثبت سفارش کنی .",
    "شنیده‌ام بهترین {item} شهر را دارید لطفاً {quantity} {unit} برای من بگذارید .",
    "دستور پخت من نیاز به {quantity} {unit} از {item} دارد آیا موجود است ؟",
    "من به {item} محلی علاقه‌مندم می‌توانم {quantity} {unit} از آن‌ها را بگیرم ؟",
    "من رژیم دارم و نیاز به {quantity} {unit} از {item} کم‌چرب دارم .",
    "نوبت من است که شام بپزم به موارد زیر نیاز دارم{quantity} {unit}  از{item} .",
    "من میزبان یک مهمانی بزرگ هستم و به {quantity} {unit} از {item} نیاز دارم .",
    "می‌توانید یک شراب خوب پیشنهاد کنید ؟ به {quantity} {unit} برای یک مناسبت خاص نیاز دارم .",
    "برای درست کردن سالاد شیرازی {quantity} {unit} {item} میخواستم .",
    "برای بچه کوچیکم مقداری خوراکی می خواستم {item} دارید ؟",
    "پودر لباسشویی ام تموم شده{item} برام بفرستید .",
    "من می‌خواهم اسموتی درست کنم و به {quantity} {unit} از {item} مخلوط نیاز دارم .",
    " بچه‌های من {item} شما را دوست دارند می‌توانید {quantity} {unit} برای من کنار بگذارید ؟",
    "من می‌خواهم یک دستور پخت جدید را امتحان کنم که به {quantity} {unit} از {item} نیاز دارد .",
    "تعریف {item} مغازه شما خیلی پیچیده است لطفا {quantity} {unit} برام بفرستید .",
    "یا تخفیفی برای خرید عمده دارید ؟ به {quantity} {unit} از {item} علاقه‌مندم .",
    "من به دنبال گزینه‌های گیاه‌خواری هستم به ویژه {quantity} {unit} از{item} .",
    "نیاز دارم انبار آشپزخانه‌ام را با {quantity} {unit} از {item} پر کنم .",
    "کنجکاوم که از مجموعه {item} شما چه چیزی دارید می‌توانم {quantity} {unit} امتحان کنم ؟",
    "مسئول میان‌وعده‌های مهمانی اداره هستم به {quantity} {unit} از {item} میخواستم .",
    "میل شدیدی به {item} دارم لطفاً {quantity} {unit} برای من بسته‌بندی کنید و بفرستید .",
    "من معلم آشپزی هستم آیا {quantity} {unit} از {item} دارید ؟",
    "می‌خواهم یک وعده غذایی قورمه سبزی آماده کنم به {quantity} {unit} از {item} درجه یک نیاز دارم .",
    "{quantity} {unit} از{item}  میخواستم موجود دارید ؟",
    "من می خواهم {quantity} {unit} از {item} را دریافت کنم .",
    "آیا می توانم {quantity} {unit} از {item} را داشته باشم ؟",
    "من می خواهم مقداری از {item} {quantity} {unit} را انتخاب کنم .",
    "آیا می توانید برای من {unit} {quantity} از {item} را بسته بندی کنید و برای من بفرستید ؟",
    "من به دنبال {item} هستم آیا آنها را در {unit} حمل می کنید ؟",
    "لطفاً {quantity} {unit} از {item} را به من بدهید .",
    "به {quantity} {unit} از {item} نیاز دارم .",
    "آیا {item} شما تازه است ؟ من {quantity} {unit} می خواهم .",
    "من به {item} به ویژه {quantity} {unit} نیاز دارم .",
    "{item} {quantity} {unit} میخوام ثبت سفارش کنم .",
    "{item} {quantity} {unit} میخواستم بخرم .",
    "{item} رو به سبد خریدم اضافه کنید .",
    "{item} {quantity} {unit} رو به سبد خریدم بیافزونید .",
    "می‌خواستم {item} را به سبد خریدم اضافه کنم اما به نظر می‌رسد در لیست نیست لطفا اضافه کنید اون رو .",
    "یادم رفت لطفا {item} هم به سبد خریدم اضافه کن .",
    "می‌خواهم {item} را که فراموش کرده بودم به سبد خریدم اضافه کنم آیا هنوز ممکن است ؟",
    "می‌خواهم {item} را که فراموش کرده‌ام به سبد خرید اضافه کنم .",
    "یک سری کالا برای خرید داشتم .",
    "خریدی داشتم .",
    "میخواستم یک سری جنس بخرم از مغازه شما .",
    "یک سفارش داشتم .",
    "می‌خواهم سفارش شماره {order_id} را برای تحویل در روز {day} تنظیم کنم .",
    "آیا می‌توانم سفارش شماره {order_id} را برای تحویل در ساعت{time} رزرو کنم ؟",
    "لطفاً سفارش شماره {order_id} را برای تاریخ {date} آماده کنید .",
    "می‌توانید سفارش شماره {order_id} را در ساعت {time} تحویل دهید ؟",
    "من این هفته فقط {day} خونه هستم لطفا سفارشم را در آن زمان ارسال کنید .",
    "میخواستم سفارشم رو ساعت {time} بفرستید .",
    "می‌خواهم زمان تحویل سفارش شماره {order_id} را برای {date} تنظیم کنید .",
    "آیا امکان تحویل سفارش شماره {order_id} در روز {day} وجود دارد ؟",
    "من علاقه‌مند به برنامه‌ریزی تحویل سفارش شماره {order_id} برای تاریخ {date} هستم .",
    "لطفاً سفارش شماره {order_id} را برای تاریخ {date} ساعت {time} آماده کنید .",
    "آیا می‌توانید سفارشم را قبل از ساعت{time} روز {day} تحویل دهید ؟",
    "برای جشنی که قراره برگزار کنیم باید حتما سفارشم روز {day} ارسال بشود .",
    "منتظر تحویل سفارش شماره {order_id} در اولین ساعت {day} هستم .",
    "برای مهمانی لطفاً سفارش شماره {order_id} را در {date} تحویل دهید .",
    "آیا امکان دارد سفارش شماره {order_id} را در {date} تحویل بگیرم ؟",
    "سفارشم را برای روز {day} ارسال کنید چون وقت دیگر خونه نیستم .",
    "میخواستم خریدم ساعت {time} فرستاده بشود .",
    "سفارشمو ساعت {time} بفرستید .",
    "کالاهایم را برای ساعت {time} روز {day} برنامه ریزی کنید .",
    "می‌خواهم {item} که در تاریخ {date} خریداری کردم را {returning_verb} .",
    "آیا می‌توانم {item} را که {number} روز پیش خریده‌ام {returning_verb} ؟",
    "سفارش شماره {order_id} را به دلیل {returning_reason} می‌خواهم {returning_verb} .",
    "{item} که در {time} خریداری شده بود معیوب است و می‌خواهم آن را {returning_verb} .",
    "متوجه شدم محصول {item} مورد نظرم نیست چگونه می‌توانم آن را {returning_verb}  ؟",
    "{item} را به اشتباه خریداری کرده‌ام آیا می‌توانم آن را {returning_verb} ؟",
    "به دلیل {returning_reason}, می‌خواهم {item} خریداری شده مورخ {date} را {returning_verb} .",
    "{item} که {number} روز پیش تحویل گرفته‌ام نیاز به تعویض دارد و دوست داشتم که برای من آن ها را {returning_noun} بدهید .",
    "آیا امکان مرجوع کردن {item} بعد از {number} استفاده هنوز وجود دارد ؟ من کالاهایم را چند روزه که دریافت کردم ولی به دلیل {returning_reason} میخواهم پس بدهم .",
    "من قصد دارم {item} خریداری شده در {date} را به دلیل {returning_reason} {returning_verb} .",
    "می‌خواهم سفارش شماره {order_id} که محصول {item} را در تاریخ {date} خریداری کردم را {returning_verb} .",
    "سفارش شماره {order_id} که {number} روز پیش برای محصول {item} ثبت شده بود را می‌خواهم {returning_verb} چون {returning_reason} .",
    "به دلیل {returning_reason} تصمیم دارم سفارش شماره {order_id} را {returning_verb} .",
    "{item} مربوط به سفارش شماره {order_id} که در روز {day} خریداری شده نیاز به تعویض دارد .",
    "سفارش شماره {order_id} را به اشتباه خریداری کرده‌ام چگونه می‌توانم آن را {returning_verb} ؟",
    "می‌خواهم {item} خریداری شده با سفارش شماره {order_id} در {date} را به دلیل {returning_reason} {returning_verb} .",
    "سفارش شماره {order_id} برای {item} که {number} روز پیش تحویل گرفته‌ام می‌خواهم {returning_verb} .",
    "آیا امکان پس دادن {item} با سفارش شماره {order_id} پس از {number} استفاده هنوز وجود دارد ؟",
    "من قصد دارم {item} مربوط به سفارش شماره {order_id} را که در {date} خریداری شده را {returning_verb} .",
    "سفارش شماره {order_id} برای {item} که در {day} خریداری شده بود مطابق انتظار نبود می‌خواهم {returning_verb} .",
    "لطفا سفارشم رو {returning_noun} بزنید . به دلیل {returning_reason}",
    "میشه سفارشم رو {returning_noun} کنید ؟ چون از خریدم پشیمان شدم .",
    "لطفا سفارش من را برگردونید. من این کالاها {returning_reason} رو نمیخوام .",
    "میخواستم سفارشم رو {returning_noun} بزنم به دلیل {returning_reason}",
    "میشه سفارشم رو {returning_noun} کنید ؟ چون {returning_reason}",
    "سفارشم به دستم رسید الان اما به خاطر {returning_reason} میخواهم سفارشم رو {returning_noun} بزنید .",
    "خریدم رو {returning_noun} بزنید .",
    "خریدم رو {returning_noun} کنید .",
    "کالایی که به دستم رسیده معیوب است میخواستم که {returning_verb}",
    "کالاهایی که ارسال شده است بسیار آسیب دیده اند لطفا {returning_noun} کنید .",
    "درخواست {returning_noun} سفارش شماره {order_id} رو دارم .",
    "میخواستم درخواست بازپرداخت سفارشم را بکنم چون {returning_reason}",
    "میخواستم که خریدم را {returning_verb} کنم و روند بازپرداخت سفارشم را شروع کنم.",
]

class Generator:
    def __init__(self, template: List[str],  entries: Dict, seed: int = 20) -> None:
        random.seed(seed)
        self.template = template
        self.entries = entries
        
    def generate(self, total_number: int) -> List[List[str]]:
        dataset = []
        for _ in range(total_number):
            dataset.extend(list(self.__fill_templates(self.template)))
        return dataset
    
    def __generate_random_entries(self):
        templates_keys = self.entries.keys()
        templates_values = [random.choice(i) for i in self.entries.values()]
        entries_dict = dict(zip(templates_keys, templates_values))
        entries_dict["date"] = f"{random.randint(1400, 1403)}/{random.randint(1, 12)}/{random.randint(1, 30)}"
        return entries_dict
    
    def __fill_templates(self, template):
        entries_dict = self.__generate_random_entries()
        chosen_sentence = random.choice(template).split()
        ne_dict = {
            "{item}": ("B-ITM", "I-ITM"),
            "{replacement_item}": ("B-ITM", "I-ITM"),
            "{unit}": ("B-UNT", "I-UNT"),
            "{day}": ("B-DAY", "I-DAY"),
            "{time}": ("B-NUM", "I-NUM"),
            "{number}": ("B-NUM", "I-NUM"),
            "{order_id}": ("B-NUM", "I-NUM"),
            "{quantity}": ("B-NUM", "I-NUM"),
            "{new_quantity}": ("B-NUM", "I-NUM"),
        }
        
        candidate = set(
            ["در", "سفارش", "روز", "ساعت", "تاریخ", "شماره", "برای", "مورخ"]
        )

        i = 0
        while i < len(chosen_sentence):
            if chosen_sentence[i] in candidate:
                
                if chosen_sentence[i + 1] in ne_dict.keys():
                    yield chosen_sentence[i].format(**entries_dict), ne_dict[chosen_sentence[i + 1]][0]
                    yield chosen_sentence[i + 1].format(**entries_dict), ne_dict[chosen_sentence[i + 1]][1]
                    i += 1
                    
                elif chosen_sentence[i + 2] in ne_dict.keys():
                    yield chosen_sentence[i].format(**entries_dict), ne_dict[chosen_sentence[i + 2]][0]
                    yield chosen_sentence[i + 1].format(**entries_dict), ne_dict[chosen_sentence[i + 2]][1]
                    yield chosen_sentence[i + 2].format(**entries_dict), ne_dict[chosen_sentence[i + 2]][1]
                    i += 2
                
                else:
                    yield chosen_sentence[i], "O"
                    
            elif chosen_sentence[i] in ne_dict.keys():
                yield chosen_sentence[i].format(**entries_dict), ne_dict[chosen_sentence[i]][0]
                
            else:
                for wo in chosen_sentence[i].format(**entries_dict).split():
                    yield wo, "O"
                    
            i += 1
    
entries = {
    "item": items,
    "replacement_item": items,
    "unit": units,
    "day": days,
    "event": events,
    "season": seasons,
    "certification": certifications,
    "time": range(1, 12),
    "returning_reason": returning_reasons,
    "returning_verb": returning_verbs,
    "returning_noun": returning_nouns,
    "deleting_reason": deleting_reasons,
    "deleting_verb": deleting_verbs,
    "deleting_noun": deleting_nouns,
    "number": range(1, 15),
    "order_id": range(1, 2341),
    "quantity": range(1, 15),
    "new_quantity": range(1, 15),
    "season": seasons,
    "condition": conditions
}

test = Generator(templates, entries)

hi = test.generate(1000)