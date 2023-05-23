from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import paho.mqtt.client as paho
import time
##import argparse

###########################################
# MQTT process
# def onMessage(client, userdata, message):
#     alldata.update({str(message.topic).split('/')[-1]: str(message.payload.decode('utf-8'))})

# client = paho.Client();
# mqtt_status = client.connect('openhabian', 1883, 60);
# client.on_message = onMessage

# client.subscribe('Climate/BME1/Temperature');
# client.subscribe('Climate/BME1/Humidity');
# client.subscribe('Climate/BME1/Pressure');

alldata = {};
###########################################

print('Enter the bot api');
TOKEN_API = input();
bot = Bot(token=TOKEN_API);
dp = Dispatcher(bot);

# Keyboard
kb = ReplyKeyboardMarkup(resize_keyboard=True); # object of the keyboard
b1 = KeyboardButton('/help');
b2 = KeyboardButton('/description');
b3 = KeyboardButton('/pic');
b4 = KeyboardButton('/location');
b5 = KeyboardButton('/control');
kb.add(b1, b2, b3); # stroka 1
kb.add(b4, b5); # stroka 2


# Inline Keyboard
temp = 0;
ikb = InlineKeyboardMarkup();
ib1 = InlineKeyboardButton(text='LED ON',
                           callback_data = 'ON');
ib2 = InlineKeyboardButton(text='LED OFF',
                           callback_data = 'OFF');
ib3 = InlineKeyboardButton(text='Close Keyboard',
                           callback_data = 'CLOSE_KEYBOARD');
ikb.add(ib1,ib2); # stroka 1
ikb.add(ib3); # stroka 2

# HELP
HELP_COMMAND = """
/help - pomosh'
/start - nachat' rabotu
/description - opisanie
/pic - картинка
/LED - LED control
/control - golosovanie
"""
##/statistics - pokazat' statisticu

# Pictures and stickers
photo_shrek = 'https://avatars.mds.yandex.net/i?id=677428243219e92eb7a779fc19f61a94ace048d7-4798081-images-thumbs&n=13';
photo_durka = "https://avatars.mds.yandex.net/i?id=262dd7154489299dd9df912aeec77dde-5869346-images-thumbs&n=13";
black_boss = 'CAACAgIAAxkBAAEHUDtjxuywoGKMxo8cseKhFlXdnKCHkwACfgMAAm2wQgNxGZa191aW9C0E';
pasha_technic = 'CAACAgIAAxkBAAIBSWPvsuszCoqnvLnZlU2uRSQcvnPYAAIVAAN3S24d3WaIgOInaaUuBA';


""" Command processing """
# Start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text = 'Well<b>cam</b>',
                           parse_mode='HTML',
                           reply_markup=kb);

# Commands
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text = HELP_COMMAND);
    
@dp.message_handler(commands=['description'])
async def description_command(message: types.Message):
    await bot.send_sticker(chat_id=message.chat.id,
                         sticker = pasha_technic);
    await bot.send_message(chat_id=message.chat.id,
                           text = 'I can control greenhouse');

@dp.message_handler(commands=['pic'])
async def send_pic(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id,
                         photo = photo_durka,
                         caption = "Za toboy viehali");

@dp.message_handler(commands=['LED'])
async def vote_command(message: types.Message):
    await bot.send_message(chat_id = message.chat.id,
                           text = 'Control',
                           reply_markup = ikb);
                     
@dp.message_handler(commands=['give'])
async def sticker(message: types.Message):
    await bot.send_sticker(message.from_user.id, sticker=black_boss);

@dp.message_handler(commands=['control'])
async def vote_command(message: types.Message):
    global alldata
    if( alldata == {} ):
        await bot.send_message(chat_id = message.chat.id,
                           text = f"No data, try after few sec");
    else:
        text_array = '';
        for topic_name in alldata.keys():
            text_array = text_array+topic_name+': '+str(alldata[topic_name])+'\n';

        await bot.send_message(chat_id = message.chat.id,
                               text = text_array);
    await message.delete();


# Callback processing
@dp.callback_query_handler()
async def vote_callback(callback: types.CallbackQuery):
    if callback.data == 'CLOSE_KEYBOARD':
        await callback.message.delete();
    if callback.data == 'ON':
#         client.publish('Climate/LED', 1);
        await callback.answer(text='LED IS ON')
        #await callback.message.edit_text(f"Temperature Control \n Current temperature: {temp}",
        #                                 reply_markup = ikb);
    if callback.data == 'OFF':
#         client.publish('Climate/LED', 0);
        await callback.answer(text="LED IS OFF")
        #await callback.message.edit_text(f"Temperature Control \n Current temperature: {temp}",
        #                                 reply_markup = ikb);
    
# Other commands
@dp.message_handler(content_types=['sticker'])
async def get_sticker_id(message: types.Message):
    await message.answer(message.sticker.file_id);
 



if __name__ == '__main__':
#     client.loop_start();
    executor.start_polling(dispatcher=dp,
                           skip_updates=True);
    
    



