import telebot
from telebot import types

from persiantools.jdatetime import JalaliDate
import datetime
import random


bot = telebot.TeleBot("5023321688:AAGgD2IBWxBLN-d7CFZi3LpOtzedIQPp89Q")


@bot.message_handler(commands=['start'])
def wellcom(message):
    bot.reply_to(message, "خوش آمدی "+(message.chat.first_name))
    bot.send_message(message.chat.id, "برای اطلاعات بیشتر /help رو تایپ کن")


gameBox = types.ReplyKeyboardMarkup(row_width=2)
choice1 = types.KeyboardButton("**بازی جدید**")
choice2 = types.KeyboardButton("خروج")
gameBox.add(choice1, choice2)


@bot.message_handler(commands=['game'])
def game_handler(message):
    click = bot.send_message(
        message.chat.id, "برای شروع کلیک کن", reply_markup=gameBox)
    bot.register_next_step_handler(message, clickFunc)


def clickFunc(message):
    if message.text == "**بازی جدید**":
        message_key = bot.send_message(
            message.chat.id, "enter between 0 to 50", reply_markup=gameBox)
        bot.register_next_step_handler(message_key, gameFunc)
        global systemChoice
        systemChoice = random.randint(0, 50)
    elif message.text == "خروج":
        bot.send_message(message.chat.id, "برای راهنمایی بیشتر، /help رو تایپ کن!",
                         reply_markup=telebot.types.ReplyKeyboardRemove(selective=True))
    else:
        bot.reply_to(message=message, text="منظورتو متوجه نشدم!")


def gameFunc(message):
    try:
        if int(message.text) == systemChoice:
            bot.send_message(message.chat.id, "👏")
            bot.send_message(message.chat.id, "تو بردی!! ((-:",
                             reply_markup=telebot.types.ReplyKeyboardRemove(selective=True))

        elif int(message.text) > systemChoice:
            message_new = bot.send_message(message.chat.id, "بیا پایین تر")
            bot.register_next_step_handler(message_new, gameFunc)
        elif int(message.text) < systemChoice:
            message_new = bot.send_message(message.chat.id, "برو بالاتر")
            bot.register_next_step_handler(message_new, gameFunc)
        elif 0 < int(message.text) < 50:
            bot.send_message(message.chat.id, "شمارت که بین 0 تا 50 نبود! /-:")

    except:
        bot.reply_to(message=message, text="منظورتو متوجه نشدم!")


@bot.message_handler(commands=['QRcode'])
def qrcodeFunc(message):
    txtQRcode = bot.send_message(message.chat.id, "متنت رو بفرست :")
    bot.register_next_step_handler(txtQRcode, make_qrcode)


def make_qrcode(message):
    QRcode = qrcode.make(message.text)

    QRcode.save("qc_bot.png")
    pic = open("qc_bot.png", "rb")
    bot.send_photo(message.chat.id, pic)


# @bot.message_handler(commands=['help'])
# def helpFunc(message):
#     bot.reply_to(
#         message, "شما گزینه ی درخواست کمک را انتخاب کردید. درخواست خود را عنوان کنید")

@bot.message_handler(commands=['maxNum'])
def findMaxNumFunc(message):
    interedText = bot.send_message(message.chat.id,"یک لیست از اعداد رو بفرست مثل 0,1,2,3,4 ")
    bot.register_next_step_handler(interedText, maxFunc)
def maxFunc(message):
    try:
        array = list(map(int,message.text.split(",")))
        bot.reply_to(message = message, text="بزرگترین عدد : " + str(max(array)))
    except:
        bot.reply_to(message = message, text="منظورتو متوجه نشدم!")

@bot.message_handler(commands=['maxIndex'])
def argMax_handler(message):
    interedText=bot.send_message(message.chat.id,"یک لیست از اعداد رو بفرست مثل 0,1,2,3,4 ")
    bot.register_next_step_handler(interedText,maxIndex_)

def maxIndex_(message):
    try:
        array=list(map(int,message.text.split(",")))
        m=max(array)
        for i in range(len(array)):
            if array[i] == m:
                bot.reply_to(message=message,text="اندیس بزرگترین عدد : " + str(i))
                break
    except:
        bot.reply_to(message=message,text="منظورتو متوجه نشدم!")

@bot.message_handler(commands=['age'])
def user_age(message):
    message_age = bot.send_message(message.chat.id,'تاریخ تولدت رو با فرمت رو به رو تایپ کن : 1379/6/31')
    bot.register_next_step_handler(message_age,age1)
def age1(message):
    userBirth = message.text.split('/')
    if len(userBirth) == 3:
            birth_day = JalaliDate.now() - JalaliDate(userBirth[0], userBirth[1], userBirth[2])
            bot.reply_to(message, 'سن شما: '+ str( birth_day.days // 365))
    else:
            bot.reply_to(message, ' !!اشتباهه!! ')

@bot.message_handler(commands=['help'])
def Help(message):
    bot.send_message(
        message.chat.id, "/start --> شروع کار ربات \n /game --> بازی کردن با ربات \n /age --> محاسبه ی سن با گرفتن تاریخ تولد شما \n /voice --> تبدیل متن به ویس \n /maxNum --> چاپ کردن بزرگترین عدد \n /maxIndex --> چاپ اندیس بزرگترین عدد \n /qrcode --> تبدیل متن به کیوآرکد")(commands=['max'])

@bot.message_handler(func= lambda message :True)
def other(message):
    bot.reply_to(message=message,text="منظورتو متوجه نشدم!")
    bot.send_message(message.chat.id,"برای اطلاعات بیشتر /help رو تایپ کن")

bot.infinity_polling()
