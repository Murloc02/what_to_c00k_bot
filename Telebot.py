from telebot import TeleBot, types
from PIL import Image
import os
import msg_saver
from gpt import Dialog
from models import load_model


TOKEN = '6916704263:AAHlJMy6_2ip8BhtXfSL-XlZcTKFyC4fe8U'
bot = TeleBot(TOKEN)
gpt_dialog = Dialog()
image_model = load_model()
IS_RUNNING = False


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    start_message(message.from_user.id)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global IS_RUNNING
    print_user(message)
    user_id = message.from_user.id
    if IS_RUNNING:
        bot.send_message(user_id, 'В данный момент бот занят, отправьте сообщение позже', reply_markup=create_markup()) 
        return
    IS_RUNNING = True
    user_messages = msg_saver.get_messages(user_id)

    if message.text == 'Новое блюдо':
        if user_messages is not None:  # очистка предыдущих сообщений
            gpt_dialog.messages = user_messages
            gpt_dialog.clear_messages()
            msg_saver.save_messages(user_id, user_messages)
        start_message(user_id)
        IS_RUNNING = False
        return

    if user_messages is None or len(user_messages) == 1:  # Первое сообщение не уточняющее

        ans = gpt_dialog.ask('Придумай блюдо и рецепт к нему из ингредиентов: ' + message.text)
        print(ans)
        bot.send_message(user_id, ans, reply_markup=create_markup())
        prompt = gpt_dialog.ask_once('Какое краткое название блюда на английском языке: ' + ans)
        print(prompt)
        msq_wait = bot.send_message(user_id, 'Изображение генерируется, ожидайте... \n'
                                             'Если прошло более 2 минут - повторите запрос.')
        image = generate_image(prompt)
        bot.send_photo(user_id, photo=image)
        bot.delete_message(user_id, msq_wait.id)

    else:  # Уточняющее сообщение
        ans = gpt_dialog.ask(message.text)
        print(ans)
        bot.send_message(user_id, ans, reply_markup=create_markup())

    msg_saver.save_messages(user_id, gpt_dialog.messages)
    IS_RUNNING = False


def print_user(message):
    print(f'{message.from_user.full_name} [@{message.from_user.username}]: {message.text}')


def create_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_new = types.KeyboardButton('Новое блюдо')
    markup.add(btn_new)
    return markup


def start_message(user_id):
    bot.send_message(user_id,
                     "Напишите свой список ингредиентов и бот предложит вам приготовить "
                     "из них блюдо и сгенерирует фото.\n"
                     "Рецепт можно улучшать, задавая боту дополнительные уточнения.\n"
                     "Чтобы начать новое блюдо с изображением, отправьте 'Новое блюдо'",
                     reply_markup=create_markup())


def generate_image(text):
    image = image_model.generate_image(
        text=text,
        seed=-1,
        grid_size=1,
        is_seamless=True
    )
    save_image(image, 'image.png')
    return image


def save_image(image: Image.Image, path: str):
    if os.path.isdir(path):
        path = os.path.join(path, 'generated.png')
    elif not path.endswith('.png'):
        path += '.png'
    print("saving image to", path)
    image.save(path)
    return image


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
