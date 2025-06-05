import telebot
import sqlite3
import random
import qrcode
import time
import hashlib
import random
import PIL


from telebot import types
last_command_times = {}
last_command_pass = {}
last_command_qr = {}
last_command_start = {}
bot = telebot.TeleBot('')
global adm1
global adm2
adm1 = '5875c9fe75c6b448c2ad09f2506b4b184808fa742ee9c7b81bab4cd27abd4bef12d8519d28f2619817c9b5e3b69f6c81b3be75d591bd3033cdfcdfbaa5cbb8f7'
adm2 = 'a842054956abbf82a04d1cd9bdb80ae6c44c077ea0ec0d85031da738532be97ee43abc300f1e5149ccc8fe068f1d4336444a8c4d12523593f785faaf9f146d29'
global text_reclam
text_reclam = "Тут могла быть ваша реклама всего за <b>700руб/месяц</b>.\n<b>Покупка рекламы: @telllineone</b>"
global kb_y
kb_back = types.ReplyKeyboardMarkup(resize_keyboard=True)
kb_back.add('Назад')

global testvar
testvar = types.InlineKeyboardMarkup()
test1 = types.InlineKeyboardButton('Купить рекламу', url="t.me/telllineone")
testvar.add(test1)

def generate_password(simvols_pas, characters):
    return ''.join(random.choice(characters) for i in range(simvols_pas))


@bot.message_handler(commands=['start'])
def start(message):
 try:
  user_id = message.chat.id
  if user_id in last_command_start and time.time() - last_command_start[user_id] < 3:
   pass
  else:
    last_command_start[user_id] = time.time()

    #РЕГИСТРАЦИЯ в БД
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    user_id = message.from_user.id
    cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                        id INTEGER PRIMARY KEY
                    )''')
    cursor.execute('INSERT OR IGNORE INTO user (id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()
    #ОБРАБОТКА НАЧАЛА
    kb_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb_start.add('Генератор паролей')
    kb_start.add('Создание QR кода')
    kb_start.add('Случайное число')
    bot.send_message(message.chat.id, '<b>Реклама необходима для бесплатной работы бота</b>', parse_mode = 'html')
    bot.send_message(message.chat.id, 'Телеграм бот <b>Мультитул</b> умеет:\nГенерировать ключ-пароль любых размеров\nСоздавать QR код из текста\nНаходить случайное значение диапазона чисел', reply_markup=kb_start, parse_mode='html')
    bot.send_message(message.chat.id, text_reclam, reply_markup=testvar, parse_mode='html')
 except:
    print('ERROR#1')

    
@bot.message_handler(commands=['sendall'])
def send_all_users(message):
  hash = hashlib.sha512(str(message.chat.id).encode()).hexdigest()
  if hash == adm1 or hash == adm2:
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    bot.send_message(message.chat.id, 'Введите текст для рассылки( не забудь <b> ТЕКСТ </b>)')
    bot.register_next_step_handler(message, send_message_to_all, cursor, conn)
  else:
     return

def send_message_to_all(message, cursor, conn):
 try:
  hash = hashlib.sha512(str(message.chat.id).encode()).hexdigest()
  if hash == adm1 or hash == adm2:
   if message.text == '-' or message.text == 'No':
      bot.send_message(message.chat.id, 'Рассылка отменена')
      return
   else:
    if len(message.text) < 100:
      a = 0
      b = 0
      text = message.text
      conn = sqlite3.connect('database.db')
      cursor = conn.cursor()
      cursor.execute('SELECT id FROM user')
      users = cursor.fetchall()
      for user in users:
        try:
          bot.send_message(user[0], text, parse_mode='html')
          a += 1
        except:
          b += 1
          cursor.execute(f"DELETE FROM user WHERE id = {(user[0])}")
      conn.commit()
      bot.send_message(message.chat.id, f'Рассылка отправлена <b>{a}</b> раз, не отправлена <b>{b}</b> раз', parse_mode='html')
      a = None
      b = None
      conn.close()
    else:
      bot.send_message(message.chat.id, 'Рассылка должна быть <b>меньше 100 символов</b>', parse_mode='html')
      return
  else:
     return
 except:
   print('ERROR_SENDALL')

@bot.message_handler(commands=['sendfile'])
def send_file(message):
  hash = hashlib.sha512(str(message.chat.id).encode()).hexdigest()
  if hash == adm1 or hash == adm2:
      conn = sqlite3.connect('database.db')
      cursor = conn.cursor()
      cursor.execute('SELECT id FROM user')
      users = cursor.fetchall()
      a = 0
      b = 0
      for user in users:
        try:
          bot.send_message(message.chat.id, user[0], parse_mode='html')
          a += 1
        except:
          b += 1
      bot.send_message(message.chat.id, f'Отправлено: {a}, ошибка {b} раз')
      a = None
      b = None

@bot.message_handler(content_types=['text'])
def startmenu(message):
 user_id = message.chat.id
 if user_id in last_command_times and time.time() - last_command_times[user_id] < 1:
  pass
 else:
  last_command_times[user_id] = time.time()
  try:
   if message.text == 'Назад':
    bot.delete_message
    kb_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb_start.add('Генератор паролей')
    kb_start.add('Создание QR кода')
    kb_start.add('Случайное число')
    bot.send_message(message.chat.id, '<b>Реклама важна для бесплатной работы бота</b>', parse_mode='html', reply_markup=kb_start)
    #bot.send_message(message.chat.id, 'Телеграм бот <b>MultiTool</b> умеет:\nГенерировать ключ-пароль любых размеров\nСоздавать QR код из текста\nНаходить случайное значение диапазона чисел', reply_markup=kb_start, parse_mode='html')
    bot.send_message(message.chat.id, text_reclam , reply_markup=testvar, parse_mode='html')
     
   if message.text == 'Генератор паролей':
    kb_simb_or = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb_simb_or.add('Символы и цифры')
    kb_simb_or.add('Символы')
    kb_simb_or.add('Цифры')
    kb_simb_or.add('Ничего')
    bot.send_message(message.chat.id, 'Выберете что использовать для создания пароля <b>кроме</b> букв', reply_markup=kb_simb_or, parse_mode='html')
    bot.register_next_step_handler(message, change_sost)
  
   if message.text == 'Создание QR кода':
    bot.send_message(message.chat.id, 'Введите текст <b>на английском</b> для преобразования его в <b>QR код</b>', reply_markup=kb_back, parse_mode='html')
    bot.register_next_step_handler(message, generate_qr)

   if message.text == 'Безопасность':
    bot.send_message(message.chat.id, '<b>Мы не сохраняем личную информацию о пользователях</b>\n\n Никакие материалы используемые при работе с ботом не сохраняются. Только база данных пользователей для рассылки, <b>это необходимо</b>\nРезультаты генерации паролей так же не храняться у нас и являються случайно созданными\nЧтобы нельзя было отследить ваш выбор пароля, бот отправляет несколько разных вариантов\nТекст QR кода и сама картинка также не храняться у нас\n\n<b>Огромная просьба не блокировать бота из за рекламы, благодаря ней он существует!\nАдминистратор бота: @telllineone</b>', reply_markup=kb_back, parse_mode='html')
    #bot.send_message(message.chat.id, text_reclam, reply_markup=testvar, parse_mode='html')

   if message.text == 'Случайное число':
    bot.send_message(message.chat.id, 'Введите <b>первое число</b>, от которого будет искаться случайное', reply_markup=kb_back, parse_mode='html')
    bot.register_next_step_handler(message, rand_x)
   if message.text == 'Заказать рекламу':
    bot.send_message(message.chat.id, 'Для покупки рекламы напишите администратору <b>@telllineone</b>', parse_mode='html')
  except:
    print('ERROR#2')
def rand_x(message):
  try:
    x_rand = message.text
    if x_rand == 'Назад':
      bot.send_message(message.chat.id, 'Действие отменено, нажмите <b>назад</b>', parse_mode='html')
    else:
      bot.send_message(message.chat.id, 'Введите <b>второе число</b>, до которого будет искаться случайное', reply_markup=kb_back, parse_mode='html')
      bot.register_next_step_handler(message, rand_y, x_rand)
  except:
    print('ERROR#3')

def rand_y(message, x_rand):
  testvar = types.InlineKeyboardMarkup()
  test1 = types.InlineKeyboardButton('Купить рекламу', url="t.me/telllineone")
  testvar.add(test1)
  try:
      if int(message.text) - int(x_rand) > 1001:
        bot.send_message(message.chat.id, 'Слишком большая разница между числами(<b>максимально 1000</b>)',reply_markup=kb_back, parse_mode='html')

        return
      else:
        kb_to_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb_to_start.add('Назад', 'Заказать рекламу')
        kb_to_start.add('Безопасность')
        if int(message.text)>int(x_rand):
          random_number = random.randint(int(x_rand), int(message.text))
          bot.send_message(message.chat.id, text_reclam, reply_markup=testvar, parse_mode='html')
          bot.send_message(message.chat.id, f'Ваше случайное число: <b>{random_number}</b>',reply_markup=kb_to_start ,parse_mode='html')
          x_rand = None
          message.text = None
        else:
            bot.send_message(message.chat.id, 'Второе число должно быть <b>больше</b> первого\n<b>Введите первое число заново</b>', reply_markup=kb_back, parse_mode='html')
            x_rand = None
            bot.register_next_step_handler(message, rand_x)
  except:
          bot.send_message(message.chat.id, 'Вы вввели некорректные значения\n<b>Введите первое число заново</b>', reply_markup=kb_back, parse_mode='html')
          x_rand = None
          bot.register_next_step_handler(message, rand_x)

def change_simbols(message, characters):
 try:
  if message.text == 'Назад':
   bot.send_message(message.chat.id, 'Действие отменено, нажмите <b>назад</b>', parse_mode='html')
   return
  else:
   user_id = message.chat.id
   qr_pass = user_id in last_command_pass and time.time() - last_command_pass[user_id]
   if user_id in last_command_pass and time.time() - last_command_pass[user_id] < 20:
    bot.send_message(message.chat.id, f'Чтобы создать пароль подождите еще <b>{20 - (round(qr_pass))}</b> секунд', parse_mode='html')
    bot.register_next_step_handler(message, change_simbols, characters)
   else:   
    try:
     simvols_pas = int(message.text)
     if 0<simvols_pas<101:
      last_command_pass[user_id] = time.time()
      kb_to_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
      kb_to_start.add('Назад', 'Заказать рекламу')
      kb_to_start.add('Безопасность')
      passwords = [generate_password(simvols_pas, characters) for _ in range(5)]
      for password in passwords:
        bot.send_message(message.chat.id, f'<code>{password}</code>', reply_markup=kb_to_start, parse_mode='html')
      bot.send_message(message.chat.id, text_reclam, reply_markup=testvar, parse_mode='html')
      password = None
      passwords = None
      characters = None
     else:
        bot.send_message(message.chat.id, 'Выберите или введите число символов для пароля(<b>от 1 до 100</b>)', parse_mode='html')
        bot.send_message(message.chat.id, text_reclam, reply_markup=testvar, parse_mode='html')
        bot.register_next_step_handler(message, change_simbols, characters)
        return
    except:
     bot.send_message(message.chat.id, 'Выберите или введите число символов для пароля(<b>от 1 до 100</b>)', parse_mode='html')
     bot.send_message(message.chat.id, text_reclam, reply_markup=testvar, parse_mode='html')
     bot.register_next_step_handler(message, change_simbols, characters)
     return
 except:
   print('ERROR#4')
   
def change_sost(message):
  try:
    if message.text == 'Символы и цифры':
          characters = ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!$%&'()*+,-./:;<=>?@[\]^_`{|}~")
    elif message.text == 'Символы':
          characters = ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!%&'()*+,-./:;<=>?@[\]^_`{|}~")
    elif message.text == 'Цифры':
          characters = ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
    elif message.text == 'Ничего':
          characters = ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
    else:
      bot.send_message(message.chat.id, 'Вы не выбрали, поэтому выбор автоматический(<b>Символы и цифры</b>)', parse_mode='html')
      characters = ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!$%&'()*+,-./:;<=>?@[\]^_`{|}~")
    
    kb_generate_pas = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb_generate_pas.add('5', '6', '8')
    kb_generate_pas.add('10', '12', '16')
    kb_generate_pas.add('Назад')
    bot.send_message(message.chat.id, 'Выберете или введите количество символов пароля(<b>до 100</b>)', reply_markup=kb_generate_pas, parse_mode='html')
    bot.register_next_step_handler(message, change_simbols, characters)
  except:
    print('ERROR#5')



def generate_qr(message):
 try:
  if message.text == 'Назад' or message.text == '/start':
    bot.send_message(message.chat.id, 'Действие отменено, нажмите <b>назад</b>', parse_mode='html')
    return
  else:
    testvar = types.InlineKeyboardMarkup()
    test1 = types.InlineKeyboardButton('Купить рекламу', url="t.me/telllineone")
    testvar.add(test1)
    user_id = message.chat.id
    qr_time = user_id in last_command_qr and time.time() - last_command_qr[user_id]
    if user_id in last_command_qr and time.time() - last_command_qr[user_id] < 60:
     bot.send_message(message.chat.id, f'Чтобы создать QR код подождите еще <b>{60 - (round(qr_time))}</b> секунд',reply_markup=kb_back, parse_mode='html')
     bot.register_next_step_handler(message, generate_qr)
    else:
     try:
      if len(message.text) < 301:
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(message.text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        last_command_qr[user_id] = time.time()
        img.save('qrcode.png')
        kb_qr_res = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb_qr_res.add('Назад', 'Купить рекламу')
        kb_qr_res.add('Гарантии безопасности')
        bot.send_photo(message.chat.id, open('qrcode.png', 'rb'), reply_markup=kb_qr_res)
        bot.send_message(message.chat.id, f'Текст QR кода: <b>{message.text}</b>', parse_mode='html')
        message.text = None
        bot.send_message(message.chat.id, text_reclam, reply_markup=testvar, parse_mode='html')
      else:
        bot.send_message(message.chat.id, f'Ошибка. Введите <b>на английском</b> текст(<b>до 300 символов</b>)', reply_markup=kb_back, parse_mode='html')
        bot.send_message(message.chat.id, text_reclam, reply_markup=testvar, parse_mode='html')
        bot.register_next_step_handler(message, generate_qr)
     except:
        bot.send_message(message.chat.id, f'Ошибка. Введите <b>на английском</b> текст(<b>до 300 символов</b>)', reply_markup=kb_back, parse_mode='html')
        bot.send_message(message.chat.id, text_reclam, reply_markup=testvar, parse_mode='html')
        bot.register_next_step_handler(message, generate_qr)

 except:
   print('ERROR#6')
 
try:
  bot.infinity_polling()
except:
  print('ERROR_POLLING')
