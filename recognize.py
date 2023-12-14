# -*- coding: utf-8 -*-
import telegram
from telegram.ext import Updater, MessageHandler, Filters
from PIL import Image
import io
import requests
import pytesseract
from langdetect import detect

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте! Загрузите картинку с текстом.")

def process_image(update, context):
    photo_file = update.message.photo[-1].get_file()   
    image_buffer = io.BytesIO()
    photo_file.download(out=image_buffer)    
    text = pytesseract.image_to_string(Image.open(image_buffer), lang="heb+eng+rus")
    #text = pytesseract.image_to_string(Image.open(image_buffer), lang="heb+eng+rus")
    print(text)   
    update.message.reply_text(text)
    lang = {'he': 'Иврит', 'aa': 'Афарский', 'ab': 'Абхазский', 'af': 'Африкаанс', 'am': 'Амхарский', 'an': 'Арагонский', 'ar': 'Арабский', 'as': 'Ассамский', 'ay': 'Аймарский', 'az': 'Азербайджанский', 'ba': 'Башкирский', 'be': 'Белорусский', 'bg': 'Болгарский', 'bh': 'Бихарский', 'bi': 'Бислама', 'bn': 'Бенгальский', 'bo': 'Тибетский', 'br': 'Бретонский', 'ca': 'Каталонский', 'co': 'Корсиканский', 'cs': 'Чешский', 'cy': 'Валлийский (Уэльский)', 'da': 'Датский', 'de': 'Немецкий', 'dz': 'Бхутани', 'el': 'Греческий', 'en': 'Английский', 'eo': 'Эсперанто', 'es': 'Испанский', 'et': 'Эстонский', 'eu': 'Баскский', 'fa': 'Фарси', 'fi': 'Финский', 'fj': 'Фиджи', 'fo': 'Фарерский', 'fr': 'Французский', 'fy': 'Фризский', 'ga': 'Ирландский', 'gd': 'Гэльский (Шотландский )', 'gl': 'Галисийский', 'gn': 'Гуарани', 'gu': 'Гуджарати', 'gv': 'Гэльский (язык жителей острова Мэн)', 'ha': 'Хауса', 'he, iw': 'Еврейский', 'hi': 'Хинди', 'hr': 'Хорватский', 'ht': 'Гаитянский Креольский', 'hu': 'Венгерский', 'hy': 'Армянский', 'ia': 'Интерлингва', 'id, in': 'Индонезийский', 'ie': 'Интерлингва', 'ii': 'Сычуань И', 'ik': 'Инупиак', 'io': 'Идо', 'is': 'Исландский', 'it': 'Итальянский', 'iu': 'Инуктитут', 'ja': 'Японский', 'jv': 'Яванский', 'ka': 'Грузинский', 'kk': 'Казахский', 'kl': 'Гренландский', 'km': 'Камбоджийский', 'kn': 'Каннада', 'ko': 'Корейский', 'ks': 'Кашмирский (Кашмири)', 'ku': 'Курдский', 'ky': 'Киргизский', 'la': 'Латинский', 'li': 'Лимбургский (Лимбургер)', 'ln': 'Лингала', 'lo': 'Лаосский', 'lt': 'Литовский', 'lv': 'Латвийский (Латышский )', 'mg': 'Малагасийский', 'mi': 'Маорийский', 'mk': 'Македонский', 'ml': 'Малаялам', 'mn': 'Монгольский', 'mo': 'Молдавский', 'mr': 'Маратхский', 'ms': 'Малайский', 'mt': 'Мальтийский', 'my': 'Бирманский', 'na': 'Науруанский', 'ne': 'Непальский', 'nl': 'Нидерландский', 'no': 'Норвежский', 'oc': 'Окситанский', 'om': 'Оромо (Афан, Галла)', 'or': 'Ория', 'pa': 'Пенджабский (Панджабский)', 'pl': 'Польский', 'ps': 'Пушту (Пушто)', 'pt': 'Португальский', 'qu': 'Кечуа', 'rm': 'Ретороманский', 'rn': 'Кирунди (Рунди)', 'ro': 'Румынский', 'ru': 'Русский', 'rw': 'Киняруанда (Руанда)', 'sa': 'Санскритский', 'sd': 'Синдхи', 'sg': 'Сангро', 'sh': 'Сербо-Хорватский', 'si': 'Сингальский (Сингалезский)', 'sk': 'Словацкий', 'sl': 'Словенский', 'sm': 'Самоанский', 'sn': 'Шона', 'so': 'Сомалийский', 'sq': 'Албанский', 'sr': 'Сербский', 'ss': 'Свати', 'st': 'Северный сото', 'su': 'Сунданский', 'sv': 'Шведский', 'sw': 'Суахили', 'ta': 'Тамильский', 'te': 'Телугу', 'tg': 'Таджикский', 'th': 'Тайский', 'ti': 'Тигринья', 'tk': 'Туркменский', 'tl': 'Тагальский', 'tn': 'Тсвана (Сетсвана)', 'to': 'Тонга (Тонганский)', 'tr': 'Турецкий', 'ts': 'Тсонга', 'tt': 'Татарский', 'tw': 'Чви (Тви)', 'ug': 'Уйгурский', 'uk': 'Украинский', 'ur': 'Урду', 'uz': 'Узбекский', 'vi': 'Вьетнамский', 'vo': 'Волапюк', 'wa': 'Валлон', 'wo': 'Волоф', 'xh': 'Коса', 'yi, ji': 'Идиш', 'yo': 'Йоруба', 'zh': 'Китайский (Традиционный)', 'zu': 'Зулусский'}
    language = detect(text)
    sp = lang.get(language)
    num_chars = len(text)
    num_words = len(text.split())   
    update.message.reply_text(f"Язык текста: {sp}\n"
        f"Количество символов с пробелами: {num_chars}\n"
        f"Количество слов: {num_words}")

updater = Updater("5887462820:AAGpt6apQec4winnedsmeC2ce7i9hdjECdI", use_context=True)

dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.command, start))
dispatcher.add_handler(MessageHandler(Filters.photo & ~Filters.command, process_image))
# dispatcher.add_handler(MessageHandler(Filters.photo & (~ Filters.command, process_image)))
#context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте! Загрузите картинку с текстом.")
updater.start_polling()
updater.idle()