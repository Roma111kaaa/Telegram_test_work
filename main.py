from telebot import TeleBot
from PIL import Image, ImageDraw, ImageFont, ImageStat
from datetime import datetime
from random import choice

bot = TeleBot("6166554842:AAG55HbY8aleogYpM8t5IRCFolcuQffThFE")


list_of_captions = [
    "Какая цаца", "вчи українську", "зробити обрізання", "хнп(ходи на пісюн)", "афтар, вбий себе з розбігу"
]


@bot.message_handler(commands=["start", "help"])
def greeting(message):
    try:
        photo = bot.get_user_profile_photos(message.from_user.id).photos[0][-1].file_id
    except IndexError:
        bot.send_message(message.chat.id, f"Приветствую тебя, {message.first_name}!")
    else:
        downloaded_pic = bot.download_file(bot.get_file(photo).file_path)
        file_path = "downloaded_pictures/{}_{}.jpg".format(datetime.now().strftime('%Y-%m-%d_%H.%M'),
                                                           message.from_user.id)
        with open(file_path, "wb") as file:
            file.write(downloaded_pic)
        add_caption_to_photo(file_path)
        with open(file_path, "rb") as img:
            bot.send_photo(message.chat.id, img, caption=f"Держи свое фото, {message.from_user.first_name}!")


def add_caption_to_photo(patch):
    image = Image.open(patch)
    draw = ImageDraw.Draw(image)
    caption_text = choice(list_of_captions)
    size = 100
    font = ImageFont.truetype("fonts/Lobster-Regular.ttf", size)
    while draw.textbbox((0, 0), caption_text, font)[2] >= image.width:
        size -= 5
        font = ImageFont.truetype("fonts/Lobster-Regular.ttf", size)
    text_size = draw.textbbox((0, 0), caption_text, font)
    color = "white"
    stat = ImageStat.Stat(image)
    if sum(stat.mean) / 3 > 128:
        color = "black"
    draw.text(((image.width - text_size[2]) // 2, image.height - 150), caption_text, font=font, fill=color)
    image.save(patch)


bot.infinity_polling()