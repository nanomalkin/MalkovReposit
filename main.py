import logging,time,bd
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN_API
from datetime import datetime,timedelta,timezone
from aiogram.types import  InlineKeyboardMarkup, InlineKeyboardButton, ContentType, Message
from typing import Union
from aiogram.types.input_media import InputMediaPhoto
from random import randrange
from aiogram.dispatcher import filters

# from app.loader import dp

#start help message.replay message.answer massgage.delete
# -1001676074919
HELP_COMMAND = """
/help - список команд
/start - начать работать
/donor - ухх какая команда минус пред
"""
BAN_MAT = {"ПОПА"," еб ","ЖОПА","ПИСЯ","БЛИН","ХУЕСОС","ВАГИНА","КАБАН","ПИЗДА","БЛЯДЬ","ЧЛЕН","Ж О П А","ЕБАЛ","ДУРАК","ДАУН","ДЕБИЛ","ПРИДУРОК","КОНЧЕНН","КАКА","СИСЬКИ","АНУС","ЗАДНИЦА", "ТАРАКАН","РОЖА","ХУЙ","СИСЯ","СИСЮ","КОЗЕЛ","КОЗЁЛ","ЛОХ","БАРАН","СВИНЬЯ","ХУЛИ","ХАТЬФУ"," ФУ ","СОСИ","POPA","ПИСЬК"}
MESS_WARN = ['ПРЕДУПРЖДЕНИЕ!!! 1/7 Так, ты тут не хулигань','ПРЕДУПРЕЖДЕНИЕ!!! 2/7 Ты что? Бандит? Вор в законе?','Пред. 3/7 Не превышай свои полномочия смельчак','Пред. 4/7 У тебя голова на плечах? Тебе же сказали!','ПРЕДУП 5/7 ТЫ УЖЕ НА ГРАНИ','Предупреждение 6/7 АЛО! Не слышишь? Иди поспи!','7/7! Ты норм? Достал, уйди прочь в мут! ']
WARN = 0
PRIVA = ['Приветствие1','Приветствие2','Приветствие3','Приветствие4','Приветствие5','Приветствие6','Приветствие7','Приветствие8','Приветствие9','Приветствие10'];
bot = Bot(TOKEN_API)
dp = Dispatcher(bot)
WWW = "Бот был перезапущен, я ничего не знаю"

def pred_pred_ban(us,mess,id_dir):
    ident = None # Не индетифицировано
    select_user = "SELECT * FROM userest" # Такой вот запрос
    sel_use = bd.execute_read_query(bd.connection, select_user)
    for post in sel_use:
        if post[2]==us:
            ident = us
            pred = post[1]+1
            ID_you = post[0]
            mess_use = post[3]
    if ident == us: # Обновить количество предов и причины
        if pred == 8:
            pred = 1
        update_post_description = f"""
        UPDATE userest
        SET count = {pred}, listing = '{mess_use}, {pred}:«{mess}»'
        WHERE user_ID = {ID_you}
        """
        bd.execute_query(bd.connection, update_post_description)
        return pred
    else: # Добавить нового
        create_users = f"""
        INSERT INTO
        userest (count, user, listing, user_helpless)
        VALUES
        (1, '{us}', '1:«{mess}»', {id_dir})
        """
        bd.execute_query(bd.connection, create_users)
        return 1

def mess_ban(id_dir):
    select_user = "SELECT * FROM userest"
    sel_use = bd.execute_read_query(bd.connection, select_user)
    for post in sel_use:
        if post[4]==str(id_dir):
            return post[3]
    return 'ты всё сломал'
    


# @dp.message_handler()
# async def message_handler(msg: Message):
#     await msg.answer(f"Твой ID: {msg.from_user.id}")

@dp.message_handler(commands=['help'])
async def help_command(message: types):
    await message.reply(text=HELP_COMMAND)

@dp.message_handler(commands=['start'])
async def mess_start(message: types):
    await message.reply(text="https://youtu.be/3lIHzuGsgSA")

@dp.message_handler(commands=['donor'])
async def mess_comm(message: types.Message):
    await message.answer(text="Пред очищен 0/7")
    global WARN 
    WARN = 0


@dp.message_handler(is_forwarded=True)
@dp.message_handler(filters.ForwardedMessageFilter(True))
async def forwarded_example(message: types.Message):
    select_user = "SELECT * FROM userest"
    sel_use = bd.execute_read_query(bd.connection, select_user)
    for post in sel_use:
        if post[4]==str(message.forward_from.id):
            await bot.send_message(message.from_user.id,text = f"Подлец, именуемый @{post[2]} имеет за собой грешки({post[1]}/7): {post[3]}")


#content_types=['photo']
@dp.message_handler()
@dp.edited_message_handler()
async def Matt(message: types.Message):
    print(message)
    for i in BAN_MAT:
        if  i in message.text.upper():
            global WARN
            if message.from_user.username:
                WARN = pred_pred_ban(message.from_user.username,message.text,message.from_user.id)
            else:
                print(message.from_user.first_name)
                WARN = pred_pred_ban(message.from_user.first_name,message.text,message.from_user.id)
            if WARN == 7:
                tt = time.time()
                await bot.restrict_chat_member(message.chat.id, message.from_user.id, types.ChatPermissions(can_send_messages=False), until_date = datetime.fromtimestamp(tt+3600))                
            if message.from_user.username:
                await bot.send_photo(
                    message.chat.id,photo="AgACAgIAAx0CY-bfpwACIvZkGzwhmBLZApSv7UQu4CNDgGppDAACv8YxG2Sj2EgYHHMv2H6OPgEAAwIAA3kAAy8E",
                    caption="@"+message.from_user.username+" "+MESS_WARN[WARN-1]
                    ,reply_markup = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton(text = "А за что?", callback_data=f'{message.from_user.id}'),InlineKeyboardButton(text = "Отмена", callback_data=f'{message.from_user.id+1}'))
                    )
                print(message.message_id)
            else:         
                await bot.send_photo(
                    message.chat.id,photo="AgACAgIAAx0CY-bfpwACIvZkGzwhmBLZApSv7UQu4CNDgGppDAACv8YxG2Sj2EgYHHMv2H6OPgEAAwIAA3kAAy8E",
                    caption=f'<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>'+" "+MESS_WARN[WARN-1],
                    parse_mode=types.ParseMode.HTML
                    ,reply_markup = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton(text = "А за что?", callback_data=f'{message.from_user.id}'),InlineKeyboardButton(text = "Отмена", callback_data=f'{message.from_user.id+1}'))
                )
                print(message.message_id)
            await message.delete()
            break


@dp.message_handler(content_types=['photo'])
@dp.edited_message_handler(content_types=['photo'])
async def Matt_pho(message: types.Message):
    print(message)
    for i in BAN_MAT:
        if  i in message.caption.upper():
            global WARN
            WARN +=  1
            if WARN == 7:
                WARN = 0
                await bot.restrict_chat_member(message.chat.id, message.from_user.id, types.ChatPermissions(can_send_messages=False), until_date = datetime.now())
            if message.from_user.username:
                await bot.send_media(
                    message.chat.id,
                    media=InputMediaPhoto('AgACAgIAAx0CY-bfpwACIvZkGzwhmBLZApSv7UQu4CNDgGppDAACv8YxG2Sj2EgYHHMv2H6OPgEAAwIAA3kAAy8E'),
                    caption='@' + message.from_user.username + ' ' + MESS_WARN[WARN-1],
                    reply_markup=InlineKeyboardMarkup(row_width=3).add(
                        InlineKeyboardButton(text='А за что?', callback_data=f'{message.from_user.id}'),
                        InlineKeyboardButton(text='Отмена', callback_data=f'{message.from_user.id+1}')
                    )
                )
            else:         
                await bot.send_photo(
                    message.chat.id,photo="AgACAgIAAx0CY-bfpwACIvZkGzwhmBLZApSv7UQu4CNDgGppDAACv8YxG2Sj2EgYHHMv2H6OPgEAAwIAA3kAAy8E",
                    caption=f'<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>'+" "+MESS_WARN[WARN-1],
                    parse_mode=types.ParseMode.HTML,
                    reply_markup = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton(text = "А за что?", callback_data=f'{message.from_user.id}'),
                                                                         InlineKeyboardButton(text = "Отмена", callback_data=f'{message.from_user.id+1}'))
                )
            await message.delete()
            break


@dp.message_handler(content_types=[ContentType.NEW_CHAT_MEMBERS]) # Го в чат
async def new_members_handler(message: types):
    new_member = message.new_chat_members[0]
    await message.reply(text=f"Добро пожаловать, {new_member.mention}, {PRIVA[randrange(10)]}")

@dp.callback_query_handler()
async def vote_callback(callback: types.CallbackQuery):
    print(mess_ban(callback.from_user.id))
    admins = await bot.get_chat_administrators(chat_id=callback.message.chat.id)
    for i in range(len(admins)):
        print(admins[i].user.username)
        if callback.from_user.username==admins[i].user.username or callback.from_user.first_name==admins[i].user.username:
            print(f"{callback.from_user.username} и {admins[i].user.username}")
            select_user = "SELECT * FROM userest"
            sel_use = bd.execute_read_query(bd.connection, select_user)
            for post in sel_use:
                if post[4]==callback.data: # отправить в лс 
                    await bot.send_message(callback.from_user.id,text = f"Подлец, именуемый @{post[2]} имеет за собой грешки({post[1]}/7): {post[3]}")
                    return await callback.answer(text=f"Его грех отображён в вашем лс",show_alert=True)
                if str(int(post[4])+1)==callback.data:
                    await bot.edit_message_caption(chat_id=callback.message.chat.id,
                                                   message_id=callback.message.message_id,
                                                   caption='Глубочайше прошу простить глупцА! Как же Я ПОСМЕЛ ДОПУСТИТЬ МЫСЛЬ О НЕВЕРНОСТИ!',
                                                   photo="")
                        #await bot.send_message(callback.from_user.id,text = f"Подлец, именуемый @{post[2]} имеет за собой грешки({post[1]}/7): {post[3]}")
                    # await bot.edit_message_media(chat_id=callback.message.chat.id,
                    #                                message_id=callback.message.message_id,
                    #                                media=types.InputMediaPhoto(media='', caption='Глубочайше прошу простить глупцА! Как же Я ПОСМЕЛ ДОПУСТИТЬ МЫСЛЬ О НЕВЕРНОСТИ!'))

                    return await callback.answer(text=f"Отменено",show_alert=True)
            break
    await callback.answer(text=f"Этот чел написал: 'Только админ может заценить, а ты кто?'",show_alert=True)     

if __name__ == '__main__':
    executor.start_polling(dp)


