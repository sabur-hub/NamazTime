import telebot
from telebot import types
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

bot = telebot.TeleBot('Bot_Token')

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_namaz = types.KeyboardButton('/namaz_today')
    markup.add(btn_namaz)
    bot.send_message(message.chat.id, 'Салом и бот барои фаҳмидани вақти намоз барои шаҳри Душанбе мебошад барои гирифтани маълумот дар бораи вақти намоз тугмачаи поёниро пашх кунед', reply_markup=markup)

@bot.message_handler(commands=['info'])
def help(message):
    bot.send_message(message.chat.id, "Ҳамаи маълумотҳои вақти намоз аз сомонаи http://www.taqvim.tj/ гирифта шудааст.Маълумотхои картаи ёфтани Қибла аз сомонаи https://qiblafinder.withgoogle.com/ гирфта шудааст.\n Муаллиф барномасоз барои хатогиҳо ҷавобгар нест! \n Агар ягон савол боқи монд метавонед ба Муаллифи ин бот муроҷиат кунед @Outic_03")


@bot.message_handler(commands=['namaz_today'])
def namaz_today_message(message):
    bot.send_message(message.chat.id, "Гирифтани вақти намоз камтар вақт мегирад илтимос тучмачаро бисёр пахш накунед")
    url = 'http://www.taqvim.tj/'

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    html_content = driver.page_source

    with open("NamazTime.html", "w+") as f:
        f.write(html_content)

    pattern = re.compile(r'case 0(.*?)break', re.DOTALL)
    matches = pattern.findall(html_content)

    response = ""

    if matches:
        for idx, match in enumerate(matches, start=1):
            extracted_data = match.strip()

            prayer_times_pattern = re.compile(r'var date_(.*?)\s*=\s*"(.*?)".*?var bomdod_from_(.*?)\s*=\s*"(.*?)".*?var bomdod_to_(.*?)\s*=\s*"(.*?)".*?var peshin_from_(.*?)\s*=\s*"(.*?)".*?var peshin_to_(.*?)\s*=\s*"(.*?)".*?var asr_from_(.*?)\s*=\s*"(.*?)".*?var asr_to_(.*?)\s*=\s*"(.*?)".*?var forbidden_time_from_(.*?)\s*=\s*"(.*?)".*?var forbidden_time_to_(.*?)\s*=\s*"(.*?)".*?var shom_from_(.*?)\s*=\s*"(.*?)".*?var shom_to_(.*?)\s*=\s*"(.*?)".*?var khuftan_from_(.*?)\s*=\s*"(.*?)".*?var khuftan_to_(.*?)\s*=\s*"(.*?)"', re.DOTALL)

            prayer_match = prayer_times_pattern.search(extracted_data)

            if prayer_match:
                date = prayer_match.group(2).replace('-', '.')
                bomdod_from = prayer_match.group(4)
                bomdod_to = prayer_match.group(6)
                peshin_from = prayer_match.group(8)
                peshin_to = prayer_match.group(10)
                asr_from = prayer_match.group(12)
                asr_to = prayer_match.group(14)
                forbidden_time_from = prayer_match.group(16)
                forbidden_time_to = prayer_match.group(18)
                shom_from = prayer_match.group(20)
                shom_to = prayer_match.group(22)
                khuftan_from = prayer_match.group(24)
                khuftan_to = prayer_match.group(26)

                response += f"Имрӯз : {date}\n"
                response += f"Бомдод аз : {bomdod_from} То: {bomdod_to}\n"
                response += f"Пешин аз : {peshin_from} To: {peshin_to}\n"
                response += f"Аср аз соати : {asr_from} To: {asr_to}\n"
                response += f"Вақти мамнӯъ аз : {forbidden_time_from} To: {forbidden_time_to}\n"
                response += f"Шом аз : {shom_from} To: {shom_to}\n"
                response += f"Хуфтан аз : {khuftan_from} To: {khuftan_to}\n\n"

    driver.quit()

    if response:
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "Извините, информация не найдена.")

bot.polling()
