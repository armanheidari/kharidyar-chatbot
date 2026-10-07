items = ['سیب', 'پرتقال', 'شیر', 'نان', 'تخم مرغ', 'پنیر', 'مرغ', 'گوشت', 'ماهی', 'برنج', 'پاستا', 'کاهو', 'سیب زمینی', 'خیار', 'هویج', 'گوجه فرنگی', 'پیاز', 'سیر', 'روغن زیتون', 'کره', "آبمیوه"]

units = ['کیلوگرم', 'لیتر', 'عدد', 'شانه', 'بطری', 'تا']

days = ["شنبه", "یک شنبه", "دوشنبه", "سه شنبه", "چهارشنبه", "پنج شنبه", "جمعه"]

numbers = ["یک", "دو", "سه", "چهار", "پنج", "شیش", "هفت", "هشت", "نه", "ده"]

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
    "تغییرات برنامه ریزی داشتم",
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
    "پاک",
    "خط",
]

templates_buying = [
    "من نیاز به {quantity} {unit} از {item} دارم .",
    "می توانم {quantity} {unit} از {item} را رزرو کنم ؟",
    "{item} میخواستم .",
    "میشه برام {quantity} {unit} {item} ثبت سفارش کنی .",
    "{quantity} {unit} از {item} آیا موجود است ؟",
    "نیاز به {quantity} {unit} از {item} دارم .",
    " به موارد زیر نیاز دارم {quantity} {unit} از {item} .",
    "{quantity} {unit} {item} میخواستم .",
    "{item} دارید ؟",
    "{item} برام بفرستید .",
    "{unit} {quantity} {item} برام کنار بگذارید",
    "به {quantity} {unit} از {item} علاقه مندم .",
    "{quantity} {unit} از {item} میخواستم .",
    "میل شدیدی به {item} دارم لطفاً {quantity} {unit} برای من بفرستید .",
    "آیا {quantity} {unit} از {item} دارید ؟",
    "{quantity} {unit} از {item} میخواستم موجود دارید ؟",
    "من می خواهم {quantity} {unit} از {item} را دریافت کنم .",
    "آیا می توانم {quantity} {unit} از {item} را داشته باشم ؟",
    "لطفاً {quantity} {unit} از {item} را به من بدهید .",
    "به {quantity} {unit} از {item} نیاز دارم .",
    "{item} {quantity} {unit} میخوام ثبت سفارش کنم .",
    "{item} {quantity} {unit} میخواستم بخرم .",
    "{item} {quantity} {unit} رو به سبد خریدم بیافزونید .",
    "{quantity}",
    "{quantity} {unit}",
]

templates_scheduling = [
    "سفارش شماره {order_id} را برای {date} آماده کنید .",
    "می توانید سفارش شماره {order_id} را در {time} تحویل دهید ؟",
    "سفارشم رو {time} بفرستید .",
    "سفارشم رو {day} بفرستید . ",
    "سفارش شماره {order_id} رو توی تاریخ {date} ارسال کنید.",
    "لطفا سفارش من رو تا روز {day} ارسال کنید.",
    "میشه خریدم رو روز {day} تا {time} بفرستید؟",
    "لطفاً سفارش شماره {order_id} را برای تاریخ {date} {time} آماده کنید .",
    "سفارشم را قبل از {time} روز {day} تحویل دهید ",
    "سفارشمو {time} بفرستید .",
    "کالاهایم را برای {time} روز {day} برنامه ریزی کنید .",
    "سفارشم را در تاریخ {date} بفرستید",
    "سفارشم رو تا {time} بفرستید.",
    "سفارش {order_id} را در تاریخ {date} ارسال کنید.",
    "سفارشم رو روز {day} {time} ارسال کنید.",
    "سفارش من را روز {day} {time} بفرستید.",
    "{order_id}",
    
]

templates_discount = [
    "به مناسبت {event} محصول {item} تخفیف داره؟",
    "برای {item} در {event} تخفیفی ارائه می دهید؟",
    "برای خرید {quantity} {unit} از {item} تخفیفی وجود دارد؟",
    "فروش ویژه {item} در {event} دارید؟",
    "برای مراسم {event} تخفیفی دارید؟",
    "محصول {item} تخفیف داره؟",
]

templates_returning = [
    "درخواست {returning_noun} سفارش {order_id} رو دارم .",
    "می خواهم سفارش {order_id} رو {returning_verb} ",
    "باید سفارش {order_id} رو {returning_verb} ",
    "میخواهم سفارشم با شماره {order_id} رو {returning_verb}",
    "{order_id}",
    "سفارش {order_id} را {returning_verb}",
    "سفارش {order_id} را برایم {returning_noun} کنید.",
]

templates_editing = [
    "می خواهم {item} را از سبد خریدم {deleting_noun} کنم و به جای آن {replacement_item} اضافه نمایم.",
    "به جای {item} من {replacement_item} میخواستم",
    "محصول {item} رو با {replacement_item} عوض کن.",
    "مقدار {item} را به {new_quantity} {unit} تغییر بده.",
    "مقدار {item} رو {new_quantity} کن لطفا.",
    "{item} رو {deleting_noun} کن برام.",
    "من {new_quantity} {unit} {replacement_item} به جای {quantity} {unit} {item} میخواهم",
    "جای {quantity} {unit} {item} رو با {new_quantity} {unit} {replacement_item} عوض کن",
    "میشه بهم به جای {quantity} {unit} {item}، {new_quantity} {unit} {replacement_item} بدی؟",
    "به جای {quantity} {unit} {item} به من {new_quantity} {unit} بده",
    "به جای {quantity} {unit} {item} من {new_quantity} {unit} {replacement_item} میخوام.",
    "{quantity} {unit} {replacement_item} را به جای {item} برام بفرست.",
    "از محصول {item} به جای {quantity} {unit} لطفا {new_quantity} {unit} بفرستید.",
    "{item} را از سبد خریدم {deleting_noun} کن.",
    "به جای {quantity} {unit} {item} لطفا {new_quantity} {unit} {replacement_item} بهم بده",
    "محصول {item} را از سفارشم {deleting_noun} کن",
    "{item} را با {replacement_item} در سبد خریدم عوض کن.",
    "به جای {item} {replacement_item} را در سبد خریدم قرار بده.",
    "میخواهم {item} را از سفارشم {deleting_noun} کنم.",
    "{item} را از سبد خریدم {deleting_noun} کن",
    "{item} رو از سفارشم {deleting_noun} کن",
    "پشیمون شدم {item} رو از سفارشم {deleting_noun} کن",
    "به جای {quantity} {unit} {item} لطفا {new_quantity} {unit} {replacement_item} را بهم بدهید",
    "مقدار {item} رو {new_quantity} {unit} کنید",
    "مقدار محصول {item} را از {quantity} {unit} به {new_quantity} {unit} تغییر بدهید.",
    "اشتباه شد به جای {quantity} {unit} {item} من {new_quantity} {unit} می خواستم.",
    "به جای {quantity} {unit} {item} لطفا {new_quantity} {unit} {replacement_item} بدهید.",
    "مقدار کالای {item} را از {quantity} {unit} به {new_quantity} {unit} اصلاح کنید.",
    "{item} را نمیخواستم",
    "{item} را {deleting_noun} کن",
    "میشه {item} رو از سفارشم {deleting_noun} کنی؟",
    "میشه به جای {item} بهم {replacement_item} بدی؟",
    "میشه از {item} {new_quantity} {unit} بفرستی؟",
    "میشه به جای {item} بهم {new_quantity} {unit} {replacement_item} بدی؟",
    "{item} رو از سبد خریدم {deleting_noun}",
    "{replacement_item} رو به جای {item} بهم بده",
    "{replacement_item} به جای {item} قرار بده",
]

templates_tracking = [
    "وضعیت سفارش شماره {order_id} چیست؟",
    "آیا سفارش شماره {order_id} ارسال شده است؟",
    "میشه سفارش {order_id} را پیگیری کنید.",
    "خریدم رو با شماره پیگیری {order_id} را رهگیری کنید.",
    "بررسی کنید ببینید سفارش {order_id} کجاست؟",
    "{item} که {number} پیش خریدم کجاست؟",
    "سفارش شماره {order_id} را پیگیری کنید.",
    "سفارش شماره {order_id} کجاست؟",
    "{order_id}",
    "سفارشم کجاست؟ شماره سفارشم {order_id} است.",
    "سفارش {order_id} رو بررسی میکنی ببینی کجاست؟",
    "خرید شماره {order_id} رو برام پیگیری کن.",
    "خرید {order_id} را رهگیری کنید.",
]

templates_inquiring = [
    "آیا محصول {item} در حال حاضر در انبار موجود است؟",
    "درباره محصول {item} بهم اطلاعات بده.",
    "قیمت {item} چفدر است؟",
    "آیا {item} در رنگ های دیگری نیز موجود است؟",
    "{item} از کدام کشور وارد می شود؟",
    "آیا محصول {item} دارای گارانتی است؟",
    "آیا {item} را می توان با {item} ترکیب کرد؟",
    "{item} رو موجود دارید؟ ",
    "قیمت {quantity} {unit} {item} چقدر میشود؟",
    "سوالاتی راجع به کالای {item} دارم.",
    "میشه قیمت {item} رو بدونم؟",
    "کیفیت {item} چجوری هست؟",
    "چجوریه؟ {item}",
    "یکم از کالا {item} بهم بگو",
    "موجودی {item} هاتون چقدر است؟",
    "میخواستم بدونم آیا {quantity} {unit} {item} موجود هست؟",
    "کالای {item} گارانتی دارد؟",
    "قیمت {item} چقدر است؟",
]

templates_deleting = [
    "خرید با شماره {order_id} را {deleting_noun} کن.",
    "سفارشم را {deleting_noun} کنید {number} پیش ثبت کرده بودم.",
    "لطفاً فرایند {deleting_noun} سفارش {order_id} را آغاز کنید.",
    "قصد دارم خریدم را {deleting_noun} کنم.",
    "سفارش {number} پیش را {deleting_noun} کن.",
    "سفارش {order_id} را {deleting_noun} کن.",
    "میخواستم که سفارشم با شماره {order_id} را {deleting_noun} کنم.",
    "سفارش شماره {order_id} را {deleting_noun}",
    "لطفاً سفارش من با شماره {order_id} را {deleting_noun} کنید.",
    "سفارش شماره {order_id} را {deleting_noun}",
    "میشه سفارشم را {deleting_noun} کنی؟",
    "خرید شماره {order_id} را {deleting_noun} بکن.",
    "میخوام سفارش {order_id} را {deleting_noun} کنم.",
    "{order_id} را {deleting_noun} کن.",
    "{order_id},"
]